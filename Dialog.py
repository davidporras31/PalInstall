from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton

class NameSelectionDialog(QDialog):
    def __init__(self, names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Name")
        self.selected:list = []
        self.selected.append(names[0])  # Default selection

        # Layout
        layout = QVBoxLayout(self)

        # Label
        label = QLabel("Please select a name:")
        layout.addWidget(label)

        # List Widget
        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for name in names:
            self.list_widget.addItem(f"{name}")
        layout.addWidget(self.list_widget)

        # Buttons
        button_box = QVBoxLayout()
        select_button = QPushButton("Select")
        select_button.clicked.connect(self.select_name)
        button_box.addWidget(select_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(cancel_button)

        layout.addLayout(button_box)

    def select_name(self):
        self.selected = []
        for item in self.list_widget.selectedItems():
            self.selected.append(item.text())
        self.accept()
