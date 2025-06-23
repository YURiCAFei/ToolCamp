# dialogs/ImageSelectDialog.py
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSpinBox, QHBoxLayout

class ImageSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("影像优选")
        self.resize(400, 200)
        layout = QVBoxLayout()

        self.shp_label = QLabel("✅ 请选择影像边界shp文件夹")
        self.shp_btn = QPushButton("选择文件夹")
        self.shp_btn.clicked.connect(self.select_shp_folder)

        self.target_label = QLabel("✅ 选择目标区域shp")
        self.target_btn = QPushButton("选择shp")
        self.target_btn.clicked.connect(self.select_target_shp)

        self.output_label = QLabel("✅ 保存路径")
        self.output_btn = QPushButton("选择保存文件夹")
        self.output_btn.clicked.connect(self.select_output_folder)

        self.spin = QSpinBox()
        self.spin.setMinimum(1)
        self.spin.setMaximum(100)
        self.spin.setValue(5)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("最大影像数："))
        hlayout.addWidget(self.spin)

        self.start_btn = QPushButton("开始优选")
        self.start_btn.clicked.connect(self.accept)

        layout.addWidget(self.shp_label)
        layout.addWidget(self.shp_btn)
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_btn)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_btn)
        layout.addLayout(hlayout)
        layout.addWidget(self.start_btn)
        self.setLayout(layout)

        self.shp_dir = ""
        self.target_shp = ""
        self.output_dir = ""

    def select_shp_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择影像shp文件夹")
        if folder:
            self.shp_dir = folder
            self.shp_label.setText(f"✅ {folder}")

    def select_target_shp(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择目标shp", "", "Shapefile (*.shp)")
        if path:
            self.target_shp = path
            self.target_label.setText(f"✅ {path}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if folder:
            self.output_dir = folder
            self.output_label.setText(f"✅ {folder}")

    def get_params(self):
        shp_files = [os.path.join(self.shp_dir, f) for f in os.listdir(self.shp_dir) if f.endswith('.shp')]
        return {
            "shp_files": shp_files,
            "target_shp": self.target_shp,
            "destination_folder": self.output_dir,
            "max_images": self.spin.value()
        }
