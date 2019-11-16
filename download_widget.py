import os

from PyQt5 import QtCore, QtWidgets

from downloader import Downloader
from settings import *


class DownloadWidget(QtWidgets.QWidget):
    def __init__(self, parent, item, link):
        super(DownloadWidget, self).__init__(None)
        self.parent = parent
        self.item = item
        self.link = link

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setAlignment(QtCore.Qt.AlignHCenter)
        self.progressBar.hide()
        widgetText = QtWidgets.QLabel(os.path.basename(link))
        self.widgetButton = QtWidgets.QPushButton("Download")
        self.widgetButton.clicked.connect(self.init_download)
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(self.progressBar)
        widgetLayout.addWidget(
            self.widgetButton, alignment=QtCore.Qt.AlignRight)
        widgetLayout.addStretch()

        widgetLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

    def init_download(self):
        self.thread = Downloader(self, self.link)
        self.thread.progress_changed.connect(self.set_progress_bar)
        self.progressBar.show()
        self.widgetButton.setDisabled(True)
        self.thread.start()
        self.thread.finished.connect(self.destroy)

    def set_progress_bar(self, progress_bar_val, taskbar_val, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(progress_bar_val * 100)

        # if self.taskbar_progress:
        #     self.taskbar_progress.setValue(taskbar_val * 100)

    def destroy(self, status):
        if status == 0:
            self.parent.draw_to_library(
                get_library_folder() / Path(self.link).stem)
            row = self.parent.DownloadsListWidget.row(self.item)
            self.parent.DownloadsListWidget.takeItem(row)
        else:
            pass