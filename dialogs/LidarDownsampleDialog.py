# dialogs/LidarDownsampleDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QFileDialog, QDoubleSpinBox, QHBoxLayout
)

class LidarDownsampleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("激光点均匀抽稀")
        self.setMinimumWidth(450)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.input_edit = QLineEdit()
        self.output_edit = QLineEdit()
        self.input_edit.setReadOnly(True)
        self.output_edit.setReadOnly(True)

        self.ratio_spin = QDoubleSpinBox()
        self.ratio_spin.setRange(0.01, 1.0)
        self.ratio_spin.setDecimals(2)
        self.ratio_spin.setSingleStep(0.05)
        self.ratio_spin.setValue(0.2)

        btn_input = QPushButton("选择输入目录")
        btn_input.clicked.connect(self.choose_input)
        btn_output = QPushButton("选择保存目录")
        btn_output.clicked.connect(self.choose_output)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(btn_input)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(btn_output)

        form.addRow("输入目录", input_layout)
        form.addRow("保存目录", output_layout)
        form.addRow("抽样比例 (0.01 - 1.0)", self.ratio_spin)

        layout.addLayout(form)

        self.ok_btn = QPushButton("执行")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def choose_input(self):
        path = QFileDialog.getExistingDirectory(self, "选择输入目录")
        if path:
            self.input_edit.setText(path)

    def choose_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择保存目录")
        if path:
            self.output_edit.setText(path)

    def get_params(self):
        return {
            "input_dir": self.input_edit.text(),
            "output_dir": self.output_edit.text(),
            "ratio": self.ratio_spin.value()
        }
