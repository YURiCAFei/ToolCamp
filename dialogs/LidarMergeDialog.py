# dialogs/LidarMergeDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QFileDialog, QHBoxLayout
)

class LidarMergeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("激光点分组合并")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.lidar_dir = QLineEdit()
        self.group_file = QLineEdit()
        self.save_dir = QLineEdit()

        btn_lidar = QPushButton("选择点云目录")
        btn_lidar.clicked.connect(self.select_lidar_dir)

        btn_group = QPushButton("选择分组说明文件")
        btn_group.clicked.connect(self.select_group_file)

        btn_save = QPushButton("选择保存路径")
        btn_save.clicked.connect(self.select_save_dir)

        layout.addLayout(form)
        form.addRow("点云目录", self._with_button(self.lidar_dir, btn_lidar))
        form.addRow("分组txt", self._with_button(self.group_file, btn_group))
        form.addRow("保存路径", self._with_button(self.save_dir, btn_save))

        self.ok_btn = QPushButton("开始合并")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def _with_button(self, lineedit, button):
        box = QHBoxLayout()
        box.addWidget(lineedit)
        box.addWidget(button)
        return box

    def select_lidar_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择点云主目录")
        if folder:
            self.lidar_dir.setText(folder)

    def select_group_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择分组txt", "", "Text Files (*.txt)")
        if path:
            self.group_file.setText(path)

    def select_save_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出路径")
        if folder:
            self.save_dir.setText(folder)

    def get_params(self):
        return {
            "lidar_dir": self.lidar_dir.text(),
            "group_txt_path": self.group_file.text(),
            "save_dir": self.save_dir.text()
        }
