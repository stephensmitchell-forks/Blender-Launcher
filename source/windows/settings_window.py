from modules.settings import (downloads_pages, favorite_pages,
                              get_command_line_arguments,
                              get_default_downloads_page,
                              get_default_library_page,
                              get_enable_download_notifications,
                              get_enable_high_dpi_scaling,
                              get_enable_new_builds_notifications,
                              get_launch_minimized_to_tray,
                              get_launch_when_system_starts,
                              get_library_folder, get_mark_as_favorite,
                              get_platform, get_taskbar_icon_color,
                              library_pages, set_command_line_arguments,
                              set_default_downloads_page,
                              set_default_library_page,
                              set_enable_download_notifications,
                              set_enable_high_dpi_scaling,
                              set_enable_new_builds_notifications,
                              set_launch_minimized_to_tray,
                              set_launch_when_system_starts,
                              set_library_folder, set_mark_as_favorite,
                              set_taskbar_icon_color, taskbar_icon_colors)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QWidget)
from ui.settings_window_ui import Ui_SettingsWindow

from windows.base_window import BaseWindow


class SettingsWindow(QMainWindow, BaseWindow, Ui_SettingsWindow):
    def __init__(self, parent):
        super().__init__()
        self.setWindowFlag(Qt.SubWindow)

        self.parent = parent
        self.setupUi(self)

        self.setWindowTitle("Settings")

        self.HeaderLayout = QHBoxLayout()
        self.HeaderLayout.setContentsMargins(36, 1, 1, 0)
        self.HeaderLayout.setSpacing(0)
        self.CentralLayout.addLayout(self.HeaderLayout)

        self.CloseButton = \
            QPushButton(QIcon(":resources/icons/close.svg"), "")
        self.CloseButton.setIconSize(QSize(20, 20))
        self.CloseButton.setFixedSize(36, 32)
        self.CloseButton.setProperty("HeaderButton", True)
        self.CloseButton.setProperty("CloseButton", True)
        self.CloseButton.clicked.connect(self.close)
        self.HeaderLabel = QLabel("Settings")
        self.HeaderLabel.setAlignment(Qt.AlignCenter)

        self.HeaderLayout.addWidget(self.HeaderLabel, 1)
        self.HeaderLayout.addWidget(self.CloseButton, 0, Qt.AlignRight)

        # Library Folder
        self.LibraryFolderLineEdit = QLineEdit()
        self.LibraryFolderLineEdit.setText(str(get_library_folder()))
        self.LibraryFolderLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        self.LibraryFolderLineEdit.setReadOnly(True)
        self.LibraryFolderLineEdit.setCursorPosition(0)

        self.SetLibraryFolderButton = \
            QPushButton(QIcon(":resources/icons/folder.svg"), "")
        self.SetLibraryFolderButton.clicked.connect(self.set_library_folder)

        self.LibraryFolderLayout = QHBoxLayout()
        self.LibraryFolderLayout.setContentsMargins(6, 0, 6, 0)
        self.LibraryFolderLayout.setSpacing(0)

        self.LibraryFolderLayout.addWidget(self.LibraryFolderLineEdit)
        self.LibraryFolderLayout.addWidget(self.SetLibraryFolderButton)

        # Launch When System Starts
        self.LaunchWhenSystemStartsCheckBox = QCheckBox()
        self.LaunchWhenSystemStartsCheckBox.setChecked(
            get_launch_when_system_starts())
        self.LaunchWhenSystemStartsCheckBox.clicked.connect(
            self.toggle_launch_when_system_starts)

        # Launch Minimized To Tray
        self.LaunchMinimizedToTrayCheckBox = QCheckBox()
        self.LaunchMinimizedToTrayCheckBox.setChecked(
            get_launch_minimized_to_tray())
        self.LaunchMinimizedToTrayCheckBox.clicked.connect(
            self.toggle_launch_minimized_to_tray)

        # High Dpi Scaling
        self.EnableHighDpiScalingCheckBox = QCheckBox()
        self.EnableHighDpiScalingCheckBox.clicked.connect(
            self.toggle_enable_high_dpi_scaling)
        self.EnableHighDpiScalingCheckBox.setChecked(
            get_enable_high_dpi_scaling())

        # Taskbar Icon Color
        self.TaskbarIconColorComboBox = QComboBox()
        self.TaskbarIconColorComboBox.addItems(taskbar_icon_colors.keys())
        self.TaskbarIconColorComboBox.setCurrentIndex(
            get_taskbar_icon_color())
        self.TaskbarIconColorComboBox.activated[str].connect(
            self.change_taskbar_icon_color)

        # Default Library Page
        self.DefaultLibraryPageComboBox = QComboBox()
        self.DefaultLibraryPageComboBox.addItems(library_pages.keys())
        self.DefaultLibraryPageComboBox.setCurrentIndex(
            get_default_library_page())
        self.DefaultLibraryPageComboBox.activated[str].connect(
            self.change_default_library_page)

        # Default Downloads Page
        self.DefaultDownloadsPageComboBox = QComboBox()
        self.DefaultDownloadsPageComboBox.addItems(downloads_pages.keys())
        self.DefaultDownloadsPageComboBox.setCurrentIndex(
            get_default_downloads_page())
        self.DefaultDownloadsPageComboBox.activated[str].connect(
            self.change_default_downloads_page)

        # Notifications
        self.EnableNewBuildsNotifications = QCheckBox()
        self.EnableNewBuildsNotifications.clicked.connect(
            self.toggle_enable_new_builds_notifications)
        self.EnableNewBuildsNotifications.setChecked(
            get_enable_new_builds_notifications())

        self.EnableDownloadNotifications = QCheckBox()
        self.EnableDownloadNotifications.clicked.connect(
            self.toggle_enable_download_notifications)
        self.EnableDownloadNotifications.setChecked(
            get_enable_download_notifications())

        # Mark As Favorite
        self.MarkAsFavorite = QComboBox()
        self.MarkAsFavorite.addItems(favorite_pages.keys())
        self.MarkAsFavorite.setCurrentIndex(
            get_mark_as_favorite())
        self.MarkAsFavorite.activated[str].connect(
            self.change_mark_as_favorite)

        # Command Line Arguments
        self.CommandLineArguments = QLineEdit()
        self.CommandLineArguments.setText(str(get_command_line_arguments()))
        self.CommandLineArguments.setContextMenuPolicy(Qt.NoContextMenu)
        self.CommandLineArguments.setCursorPosition(0)
        self.CommandLineArguments.editingFinished.connect(
            self.update_command_line_arguments)

        # Layout
        SettingsLayoutContainer = QWidget(self)
        SettingsLayoutContainer.setProperty('FormLayout', True)
        SettingsLayout = QFormLayout(SettingsLayoutContainer)
        SettingsLayout.setContentsMargins(1, 0, 1, 6)
        SettingsLayout.setSpacing(6)
        SettingsLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        SettingsLayout.setFieldGrowthPolicy(
            QFormLayout.AllNonFixedFieldsGrow)
        SettingsLayout.setLabelAlignment(Qt.AlignLeft)
        self.CentralLayout.addWidget(SettingsLayoutContainer)

        SettingsLayout.addRow(self._QLabel("Library Folder:"))
        SettingsLayout.addRow(self.LibraryFolderLayout)

        SettingsLayout.addRow(self._QLabel("System:"))
        layout = self._QFormLayout()
        layout.addRow(
            "Taskbar Icon Color", self.TaskbarIconColorComboBox)

        if get_platform() == 'Windows':
            layout.addRow("Launch When System Starts",
                          self.LaunchWhenSystemStartsCheckBox)

        layout.addRow("Launch Minimized To Tray",
                      self.LaunchMinimizedToTrayCheckBox)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel("Interface:"))
        layout = self._QFormLayout()
        layout.addRow(
            "Default Library Page", self.DefaultLibraryPageComboBox)
        layout.addRow(
            "Default Downloads Page", self.DefaultDownloadsPageComboBox)
        SettingsLayout.addRow(layout)
        layout.addRow("Mark New Build As Favorite", self.MarkAsFavorite)
        layout.addRow("Enable High DPI Scaling",
                      self.EnableHighDpiScalingCheckBox)

        SettingsLayout.addRow(self._QLabel("Notifications:"))
        layout = self._QFormLayout()
        layout.addRow("When New Builds Are Available",
                      self.EnableNewBuildsNotifications)
        layout.addRow("When Downloading Is Finished",
                      self.EnableDownloadNotifications)
        SettingsLayout.addRow(layout)

        SettingsLayout.addRow(self._QLabel(
            "Blender Command Line Arguments:"))
        layout = self._QFormLayout()
        layout.addRow(self.CommandLineArguments)
        SettingsLayout.addRow(layout)

        self.resize(self.sizeHint())
        self.show()

    def _QLabel(self, text):
        label = QLabel(text)
        label.setIndent(6)
        label.setProperty('Header', True)
        return label

    def _QFormLayout(self):
        layout = QFormLayout()
        layout.setContentsMargins(6, 0, 6, 0)
        layout.setSpacing(6)
        return layout

    def set_library_folder(self):
        library_folder = str(get_library_folder())
        new_library_folder = QFileDialog.getExistingDirectory(
            self, "Select Library Folder", library_folder,
            options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)

        if new_library_folder and (library_folder != new_library_folder):
            self.LibraryFolderLineEdit.setText(new_library_folder)
            set_library_folder(new_library_folder)
            self.parent.draw_library(clear=True)

    def toggle_launch_when_system_starts(self, is_checked):
        set_launch_when_system_starts(is_checked)

    def toggle_launch_minimized_to_tray(self, is_checked):
        set_launch_minimized_to_tray(is_checked)

    def toggle_enable_high_dpi_scaling(self, is_checked):
        set_enable_high_dpi_scaling(is_checked)

    def change_default_library_page(self, page):
        set_default_library_page(page)

    def change_default_downloads_page(self, page):
        set_default_downloads_page(page)

    def change_mark_as_favorite(self, page):
        set_mark_as_favorite(page)

    def change_taskbar_icon_color(self, color):
        set_taskbar_icon_color(color)

    def toggle_enable_download_notifications(self, is_checked):
        set_enable_download_notifications(is_checked)

    def toggle_enable_new_builds_notifications(self, is_checked):
        set_enable_new_builds_notifications(is_checked)

    def update_command_line_arguments(self):
        args = self.CommandLineArguments.text()
        set_command_line_arguments(args)
