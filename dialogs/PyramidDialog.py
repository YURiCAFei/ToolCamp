# dialogs/PyramidDialog.py
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QCheckBox, QHBoxLayout
)

class PyramidDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("构建影像金字塔")
        self.resize(400, 200)
        layout = QVBoxLayout()

        # 输入文件夹选择
        self.input_label = QLabel("✅ 请选择影像文件夹")
        self.input_btn = QPushButton("选择文件夹")
        self.input_btn.clicked.connect(self.select_input_folder)

        # 类型选择
        self.embed_box = QCheckBox("内嵌金字塔（写入影像）")
        self.ovr_box = QCheckBox(".ovr 外部文件")
        self.rrd_box = QCheckBox(".rrd 外部文件")

        self.embed_box.setChecked(True)  # 默认选中

        # 启动按钮
        self.start_btn = QPushButton("开始构建")
        self.start_btn.clicked.connect(self.accept)

        # 布局
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_btn)
        layout.addWidget(QLabel("请选择金字塔类型（可多选）："))
        layout.addWidget(self.embed_box)
        layout.addWidget(self.ovr_box)
        layout.addWidget(self.rrd_box)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)
        self.input_dir = ""

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择影像文件夹")
        if folder:
            self.input_dir = folder
            self.input_label.setText(f"✅ {folder}")

    def get_params(self):
        return {
            "input_dir": self.input_dir,
            "types": {
                "embed": self.embed_box.isChecked(),
                "ovr": self.ovr_box.isChecked(),
                "rrd": self.rrd_box.isChecked()
            }
        }
