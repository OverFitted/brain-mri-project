import os
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import QThread
from PyQt5 import uic
from ui import Ui_MainWindow
from ui_functions import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.paths = []
        self.value = 0

        # Open file manager
        self.ui.file_browser_button.clicked.connect(lambda: UIFunctions.file_browser_button(self))

        # Upload image sequence
        self.ui.pushButton_go.clicked.connect(lambda: UIFunctions.upload_file(self))

        # Choose sequence using drop-down list
        self.ui.sequences_chooser.currentIndexChanged.connect(lambda: UIFunctions.change_sequence(self, self.ui.sequences_chooser.currentIndex()))

        # Choose image in sequence using slider
        self.ui.horizontalSlider.valueChanged.connect(lambda: UIFunctions.update_image(self, self.ui.horizontalSlider.value()))

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
