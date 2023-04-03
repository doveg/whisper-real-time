from PyQt5 import QtCore
from PyQt5.QtCore import QEventLoop, QTimer


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()
