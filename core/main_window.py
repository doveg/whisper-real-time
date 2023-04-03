import _thread

from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItem, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView, QTableView, QHeaderView

from audio import audio_recorder
from audio.audio_recorder import recorder_obj
from audio.whisper_adapter import whisper_obj
from config import constants
from config.constants import init_dir
from ui.stt_ui import Ui_MainWindow
from util import file_util


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_better_ui()
        self.init_button()
        self.init_table()
        self._isRealTime = False
        init_dir()

    def init_better_ui(self):
        self.setWindowIcon(QIcon(constants.path_icon))
        MainWindow.move(self, 540, 0)
        # QShortcut(QKeySequence(self.tr("Space")), self, self.clicked_button_live)
        # QShortcut(QKeySequence(self.tr("Ctrl+Space")), self, self.clicked_button_continue)
        # QShortcut(QKeySequence(self.tr("Ctrl+Q")), self, self.close)
        # sys.stdout = EmittingStream(textWritten=self.outputWritten)
        # sys.stderr = EmittingStream(textWritten=self.outputWritten)

    # def outputWritten(self, text):
    #     self.ui.lineEdit_progress.setText(text)

    def init_button(self):
        # realtime
        self.ui.pushButton_begin.clicked.connect(self.clicked_button_begin)
        self.ui.pushButton_end.clicked.connect(self.clicked_button_end)
        # live
        self.ui.pushButton_live.clicked.connect(self.clicked_button_live)
        self.ui.pushButton_continue.clicked.connect(self.clicked_button_continue)
        self.ui.pushButton_stop.clicked.connect(self.clicked_button_stop)
        self.ui.pushButton_finish.clicked.connect(self.clicked_button_finish)
        # record
        self.ui.pushButton_record.clicked.connect(self.clicked_button_record)
        self.ui.pushButton_submit.clicked.connect(self.clicked_button_submit)
        self.ui.pushButton_play.clicked.connect(self.clicked_button_play)
        self.ui.pushButton_delete.clicked.connect(self.clicked_button_delete)
        # table
        self.ui.tableView.doubleClicked.connect(self.clicked_button_play)

    # realtime
    def clicked_button_begin(self):
        if recorder_obj.check_status(constants.action_begin):
            if recorder_obj.is_start(constants.action_begin):
                _thread.start_new_thread(self.realtime_begin, ())
            else:
                self.ui.lineEdit_status.setText(constants.prompt_fail_begin)
        else:
            self.ui.lineEdit_status.setText(constants.prompt_fail_task)

    def realtime_begin(self):
        self.ui.lineEdit_status.setText(constants.prompt_recording)
        self.ui.lineEdit_realtime.setText(constants.prompt_realtime)
        recorder_obj.start()
        self._isRealTime = True
        while self._isRealTime:
            constants.realtime_delay()
            if self._isRealTime:
                self.realtime()

    def realtime(self):
        if recorder_obj.check_status(constants.action_realtime):
            self.ui.lineEdit_realtime.setText(constants.prompt_transcribing)
            _, result = self.get_whisper_result(constants.type_realtime)
            if result.strip().strip("\n").strip(".") != "":
                self.ui.textEdit_realtime.append(result)
            self.ui.lineEdit_realtime.setText(constants.prompt_realtime)
        else:
            self.ui.lineEdit_status.setText(constants.prompt_fail_task)

    def clicked_button_end(self):
        self._isRealTime = False
        constants.realtime_delay()
        self.ui.lineEdit_realtime.setText(constants.prompt_finished)
        self.ui.lineEdit_status.setText(constants.prompt_transcribing)
        result = self.finish_final(constants.type_final_realtime, constants.action_realtime)
        self.ui.textEdit_transcribe.append(result)
        self.ui.lineEdit_status.setText(constants.prompt_finished)

    # live
    def clicked_button_live(self):
        if recorder_obj.check_status(constants.action_live):
            if recorder_obj.is_start(constants.action_live):
                self.ui.lineEdit_live.setText(constants.prompt_live)
                self.ui.lineEdit_status.setText(constants.prompt_recording)
                recorder_obj.start()
            else:
                self.ui.lineEdit_live.setText(constants.prompt_transcribing)
                _, result = self.get_whisper_result(constants.type_live)
                if result.strip().strip(".") != "":
                    self.ui.textEdit_live.append(result)
                self.ui.lineEdit_live.setText(constants.prompt_live)
        else:
            self.ui.lineEdit_status.setText(constants.prompt_fail_task)

    def clicked_button_stop(self):
        recorder_obj.stop(constants.action_live)
        self.ui.lineEdit_live.setText(constants.prompt_finished)
        self.ui.lineEdit_status.setText(constants.prompt_finished)

    def clicked_button_finish(self):
        self.clicked_button_live()
        self.ui.lineEdit_live.setText(constants.prompt_finished)
        self.ui.lineEdit_status.setText(constants.prompt_transcribing)
        result = self.finish_final(constants.type_final_live, constants.action_live)
        self.ui.textEdit_final.append(result)
        self.ui.lineEdit_status.setText(constants.prompt_finished)

    def clicked_button_continue(self):
        recorder_obj.clear_temp()
        self.ui.lineEdit_live.setText(constants.prompt_continue)

    # record
    def clicked_button_record(self):
        self.ui.lineEdit_recorder.setText(constants.prompt_recording)
        if recorder_obj.check_status(constants.action_record):
            recorder_obj.start()

    def clicked_button_submit(self):
        self.ui.lineEdit_recorder.setText(constants.prompt_transcribing)
        result = self.finish_final(constants.type_record, constants.action_record)
        self.ui.textEdit_realtime.append(result)
        self.ui.lineEdit_recorder.setText(constants.prompt_finished)

    # common
    def finish_final(self, audio_type, action_type):
        file_path, result = self.get_whisper_result(audio_type)
        recorder_obj.stop(action_type)
        file_util.put_cache_data(file_path, result)
        self.init_table()
        return result

    def get_whisper_result(self, audio_type):
        QApplication.processEvents()
        file_path = constants.get_audio_path(audio_type)
        recorder_obj.save_audio(file_path, audio_type)
        if not hasattr(whisper_obj, "_model"):
            self.ui.lineEdit_status.setText(constants.prompt_loading)
            QApplication.processEvents()
            whisper_obj.load_model()
        self.ui.lineEdit_status.clear()
        QApplication.processEvents()
        result = whisper_obj.transcribe(file_path, True)
        return file_path, result

    # list
    def clicked_button_play(self):
        row_number = self.get_row_number()
        audio_text = self.get_column_text(row_number, 1)
        audio_path = self.get_column_text(row_number, 2)
        audio_recorder.audio_play_thread(audio_path)
        self.ui.textEdit_recorder.setText(audio_text)

    def clicked_button_delete(self):
        row_number = self.get_row_number()
        file_util.delete_row(row_number)
        self.init_table()

    # table
    def get_row_number(self):
        current_index = self.ui.tableView.currentIndex()
        row_number = current_index.row()
        if row_number is None:
            return -1
        return row_number

    def get_column_text(self, row_number, column_number):
        column_index = self.ui.tableView.model().index(row_number, column_number)
        data = self.ui.tableView.model().data(column_index)
        return data

    def init_table(self):
        table_data = file_util.get_cache_data()
        model = QtGui.QStandardItemModel(0, 3)
        model.setHorizontalHeaderLabels(["Name", "Content", "Path"])
        for item in table_data:
            model.appendRow([QStandardItem(x) for x in item])
        self.ui.tableView.setModel(model)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setEditTriggers(QTableView.NoEditTriggers)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
