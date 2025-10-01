import sys
import Installer
import json
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QProgressBar
)


last_paths_file = "./PalInstall.json"

class PalInstallUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PalInstall")

        # get saved last paths
        if not os.path.isfile(last_paths_file):
            with open(last_paths_file, "w") as f:
                json.dump({"game_path": "", "collection_path": ""}, f)
        with open(last_paths_file, "r") as f:
            paths = json.load(f)

        # Game file selection
        self.game_file_label = QLabel("Game Path:")
        self.game_file_edit = QLineEdit()
        self.game_file_edit.setText(paths.get("game_path", ""))
        self.game_file_btn = QPushButton("Browse")
        self.game_file_btn.clicked.connect(self.select_game_file)

        game_file_layout = QHBoxLayout()
        game_file_layout.addWidget(self.game_file_edit)
        game_file_layout.addWidget(self.game_file_btn)

        # Collection path selection
        self.collection_path_label = QLabel("Collection Path:")
        self.collection_path_edit = QLineEdit()
        self.collection_path_edit.setText(paths.get("collection_path", ""))
        self.collection_path_btn = QPushButton("Browse")
        self.collection_path_btn.clicked.connect(self.select_collection_path)

        collection_path_layout = QHBoxLayout()
        collection_path_layout.addWidget(self.collection_path_edit)
        collection_path_layout.addWidget(self.collection_path_btn)

        # Install and Purge buttons
        self.install_btn = QPushButton("Install")
        self.install_btn.clicked.connect(self.install)
        self.purge_btn = QPushButton("Purge")
        self.purge_btn.clicked.connect(lambda: Installer.purgeCollection(self))

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.install_btn)
        buttons_layout.addWidget(self.purge_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.game_file_label)
        layout.addLayout(game_file_layout)
        layout.addWidget(self.collection_path_label)
        layout.addLayout(collection_path_layout)
        layout.addWidget(self.progress_bar)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def select_game_file(self):
        file_name = QFileDialog.getExistingDirectory(self, "Select Game File")
        if file_name:
            self.game_file_edit.setText(file_name)

    def select_collection_path(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select Collection Path")
        if dir_name:
            self.collection_path_edit.setText(dir_name)
    def install(self):
        Installer.installCollection(self)
        # save last paths
        paths = {
            "game_path": self.game_file_edit.text(),
            "collection_path": self.collection_path_edit.text()
        }
        with open(last_paths_file, "w") as f:
            json.dump(paths, f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PalInstallUI()
    window.show()
    sys.exit(app.exec_())