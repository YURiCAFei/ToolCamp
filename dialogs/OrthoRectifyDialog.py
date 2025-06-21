# dialogs/OrthoRectifyDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QFileDialog,
    QDoubleSpinBox, QHBoxLayout
)

class OrthoRectifyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("影像正射")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        form = QFormLayout()

        # 输入框定义
        self.input_dir = QLineEdit()
        self.rpc_suffix = "_rpc.txt"  # 固定匹配规则
        self.dem_dir = QLineEdit()
        self.output_dir = QLineEdit()
        self.resolution_m = QDoubleSpinBox()
        self.resolution_m.setRange(0.1, 100.0)
        self.resolution_m.setValue(1.0)
        self.resolution_m.setDecimals(2)

        # 浏览按钮
        self.input_btn = QPushButton("选择影像文件夹")
        self.input_btn.clicked.connect(self.choose_input)

        self.dem_btn = QPushButton("选择DEM文件夹")
        self.dem_btn.clicked.connect(self.choose_dem)

        self.output_btn = QPushButton("选择输出路径")
        self.output_btn.clicked.connect(self.choose_output)

        # 路径栏布局
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_dir)
        input_layout.addWidget(self.input_btn)

        dem_layout = QHBoxLayout()
        dem_layout.addWidget(self.dem_dir)
        dem_layout.addWidget(self.dem_btn)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_dir)
        output_layout.addWidget(self.output_btn)

        form.addRow("影像文件夹", input_layout)
        form.addRow("DEM文件夹", dem_layout)
        form.addRow("保存路径", output_layout)
        form.addRow("分辨率（米）", self.resolution_m)

        layout.addLayout(form)

        # 执行按钮
        self.ok_btn = QPushButton("执行")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def choose_input(self):
        path = QFileDialog.getExistingDirectory(self, "选择影像输入文件夹")
        if path:
            self.input_dir.setText(path)

    def choose_dem(self):
        path = QFileDialog.getExistingDirectory(self, "选择DEM文件夹")
        if path:
            self.dem_dir.setText(path)

    def choose_output(self):
        path = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if path:
            self.output_dir.setText(path)

    def get_params(self):
        return {
            "input_folder": self.input_dir.text(),
            "dem_folder": self.dem_dir.text(),
            "output_folder": self.output_dir.text(),
            "resolution_m": self.resolution_m.value()
        }
