# dialogs/ShpMergeDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QFileDialog, QHBoxLayout
)

class ShpMergeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SHP合并")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.input_dir = QLineEdit()
        self.output_dir = QLineEdit()

        btn_input = QPushButton("选择输入目录")
        btn_input.clicked.connect(self.select_input)

        btn_output = QPushButton("选择保存目录")
        btn_output.clicked.connect(self.select_output)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_dir)
        input_layout.addWidget(btn_input)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_dir)
        output_layout.addWidget(btn_output)

        form.addRow("包含子文件夹的目录", input_layout)
        form.addRow("合并输出目录", output_layout)

        layout.addLayout(form)
        self.ok_btn = QPushButton("执行合并")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def select_input(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输入路径")
        if folder:
            self.input_dir.setText(folder)

    def select_output(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出路径")
        if folder:
            self.output_dir.setText(folder)

    def get_params(self):
        return {
            "input_dir": self.input_dir.text(),
            "output_dir": self.output_dir.text()
        }
