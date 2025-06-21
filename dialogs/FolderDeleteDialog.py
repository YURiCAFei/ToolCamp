# dialogs/FolderDeleteDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QFileDialog
)

class FolderDeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("删除指定文件夹")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.root_edit = QLineEdit()
        self.txt_edit = QLineEdit()
        self.root_edit.setReadOnly(True)
        self.txt_edit.setReadOnly(True)

        root_btn = QPushButton("选择源目录")
        root_btn.clicked.connect(self.choose_root)
        txt_btn = QPushButton("选择TXT列表")
        txt_btn.clicked.connect(self.choose_txt)

        form.addRow("源目录", self.root_edit)
        form.addRow("", root_btn)
        form.addRow("列表文件", self.txt_edit)
        form.addRow("", txt_btn)

        layout.addLayout(form)

        self.ok_btn = QPushButton("执行")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def choose_root(self):
        path = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if path:
            self.root_edit.setText(path)

    def choose_txt(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择TXT文件", "", "Text Files (*.txt)")
        if path:
            self.txt_edit.setText(path)

    def get_params(self):
        return {
            "root_path": self.root_edit.text(),
            "txt_path": self.txt_edit.text()
        }
