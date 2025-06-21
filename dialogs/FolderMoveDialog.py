# dialogs/FolderMoveDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QFileDialog
)

class FolderMoveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("移动指定文件夹")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.src_edit = QLineEdit()
        self.txt_edit = QLineEdit()
        self.dst_edit = QLineEdit()

        self.src_edit.setReadOnly(True)
        self.txt_edit.setReadOnly(True)
        self.dst_edit.setReadOnly(True)

        btn_src = QPushButton("选择源目录")
        btn_src.clicked.connect(self.choose_src)
        btn_txt = QPushButton("选择TXT文件")
        btn_txt.clicked.connect(self.choose_txt)
        btn_dst = QPushButton("选择目标目录")
        btn_dst.clicked.connect(self.choose_dst)

        form.addRow("源目录", self.src_edit)
        form.addRow("", btn_src)
        form.addRow("列表文件", self.txt_edit)
        form.addRow("", btn_txt)
        form.addRow("目标目录", self.dst_edit)
        form.addRow("", btn_dst)

        layout.addLayout(form)

        self.ok_btn = QPushButton("执行")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def choose_src(self):
        path = QFileDialog.getExistingDirectory(self, "选择源目录")
        if path:
            self.src_edit.setText(path)

    def choose_txt(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择列表TXT", "", "Text Files (*.txt)")
        if path:
            self.txt_edit.setText(path)

    def choose_dst(self):
        path = QFileDialog.getExistingDirectory(self, "选择目标目录")
        if path:
            self.dst_edit.setText(path)

    def get_params(self):
        return {
            "source_root": self.src_edit.text(),
            "txt_path": self.txt_edit.text(),
            "target_root": self.dst_edit.text()
        }
