import io
import os
import re
import shutil
import zipfile

from utils.dcm2imgseq import *
from glob import glob
from main import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from requests import post
from time import sleep


class UIFunctions(QMainWindow):
    def change_sequence(self, value):
        """
        Changes the image sequence to be displayed.

        Args:
            value (int): index of selected sequence
        """
        self.sequence = self.sequences[value]
        self.paths = sorted([os.path.basename(file) for file in glob(os.path.join(IMAGE_FOLDER, self.sequence, "*.jpg"))], key=lambda x: int("".join([s for s in list(x) if s.isdigit()])))
        self.value = 0
        self.ui.horizontalSlider.setValue(0)
        self.ui.horizontalSlider.setRange(0, len(self.paths) - 1)
        UIFunctions.update_image(self, self.value)

    def file_browser_button(self):
        """
        Open file explorer
        """
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
            if not fname.split(".")[1] in ["bmp", "gif", "jpg", "jpeg", "png", "pbm", "pgm", "ppm", "xbm", "xpm", "zip"]:
                self.ui.error_label.setText("Invalid file format")
            else:
                self.ui.bottom_lineEdit.setText("")
                self.ui.file_lineEdit.setText("")
                self.ui.error_label.setText("")
                self.ui.label_for_image.setText("")
                self.ui.file_lineEdit.setText(fname)

                self.sequences = dcm2imgseq(fname)
                self.sequence = self.sequences[0]
                self.ui.sequences_chooser.clear()
                self.ui.sequences_chooser.addItems(self.sequences)
        except FileNotFoundError as e:
            self.ui.error_label.setText("File not found")
        except Exception as e:
            self.ui.error_label.setText("Unknown error")
            print(e)

    def upload_file(self):
        """
        Upload a file from UI to server
        """
        try:
            shutil.make_archive(*ARCHIVE_FILENAME.split("."), os.path.join(IMAGE_FOLDER, self.sequence))
            fname = self.ui.file_lineEdit.text()
            files = {'upload_file': open(ARCHIVE_FILENAME, 'rb')}
            res = post(SERVER_URL, files=files)

            for file in glob(os.path.join(IMAGE_FOLDER, self.sequence, "*.jpg")):
                os.remove(file)

            for file in glob(os.path.join(IMAGE_FOLDER, self.sequence, "*.txt")):
                os.remove(file)

            with open("result.zip", "wb") as save_file:
                save_file.write(res.content)

            newfname = "result.zip"

            with zipfile.ZipFile("result.zip", 'r') as zip_ref:
                zip_ref.extractall(os.path.join(IMAGE_FOLDER, self.sequence))

            UIFunctions.update_image(self, self.value)

        except (FileNotFoundError, FileExistsError):
            self.ui.error_label.setText("File not found")
        except Exception as e:
            if not self.ui.file_lineEdit.text():
                self.ui.error_label.setText("File not found")
                print(e)
            else:
                self.ui.error_label.setText("Unknown error")
                print(e)

    def update_image(self, value):
        """
        Update image using slider.

        Args:
            value (int): slider value
        """
        self.value = value
        if self.paths:
            new_image_path = os.path.join(IMAGE_FOLDER, self.sequence, self.paths[value])
            pixmap = QPixmap(new_image_path)
            self.ui.label_for_image.setPixmap(pixmap.scaled(512, 512))
            try:
                with io.open(new_image_path.replace("jpg", "txt"), encoding="UTF-8") as file:
                    text = file.read()
                self.ui.bottom_lineEdit.setText(text)
            except Exception as e:
                str(e)
