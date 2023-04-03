import sys

import qdarkstyle
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from core import main_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = main_window.MainWindow()
    win.show()
    sys.exit(app.exec_())
