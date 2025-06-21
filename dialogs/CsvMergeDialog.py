# dialogs/CsvMergeDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QFileDialog, QHBoxLayout
)

class CsvMergeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("激光数据格式转换")
        self.setMinimumWidth(450)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.parent_folder_edit = QLineEdit()
        self.output_folder_edit = QLineEdit()
        self.parent_folder_edit.setReadOnly(True)
        self.output_folder_edit.setReadOnly(True)

        btn_input = QPushButton("选择数据根目录")
        btn_input.clicked.connect(self.choose_input)
        btn_output = QPushButton("选择保存路径")
        btn_output.clicked.connect(self.choose_output)

        # 同一行显示输入路径 + 按钮
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.parent_folder_edit)
        input_layout.addWidget(btn_input)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_folder_edit)
        output_layout.addWidget(btn_output)

        form.addRow("CSV根目录", input_layout)
        form.addRow("保存目录", output_layout)

        layout.addLayout(form)

        self.ok_btn = QPushButton("执行")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def choose_input(self):
        path = QFileDialog.getExistingDirectory(self, "选择父目录")
        if path:
            self.parent_folder_edit.setText(path)

    def choose_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择保存目录")
        if path:
            self.output_folder_edit.setText(path)

    def get_params(self):
        return {
            "parent_folder": self.parent_folder_edit.text(),
            "output_dir": self.output_folder_edit.text()
        }
