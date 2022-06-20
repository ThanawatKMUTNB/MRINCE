import sys
import os

import pandas as pd
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Phase 2')

        self.show()

if __name__ == '__main__':
    app = qtw.QApplication([])
    main_win = MainWindow()
    app.exec_()