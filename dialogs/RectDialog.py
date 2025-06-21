# dialogs/RectDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt


class RectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("生成矩形边界")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        form = QFormLayout()

        # 输入框
        self.lat1_edit = QLineEdit()
        self.lon1_edit = QLineEdit()
        self.lat2_edit = QLineEdit()
        self.lon2_edit = QLineEdit()
        self.save_path_edit = QLineEdit()
        self.save_path_edit.setReadOnly(True)

        # 浏览按钮
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.choose_save_path)

        # 保存路径一行 = 路径编辑框 + 浏览按钮
        save_layout = QHBoxLayout()
        save_layout.addWidget(self.save_path_edit)
        save_layout.addWidget(browse_btn)

        # 添加表单项
        form.addRow("左上角纬度（lat1）", self.lat1_edit)
        form.addRow("左上角经度（lon1）", self.lon1_edit)
        form.addRow("右下角纬度（lat2）", self.lat2_edit)
        form.addRow("右下角经度（lon2）", self.lon2_edit)
        form.addRow("保存路径", save_layout)

        # 主体布局
        layout.addLayout(form)

        # 执行按钮
        self.ok_btn = QPushButton("执行")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def choose_save_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "选择保存路径", "", "Shapefile (*.shp)")
        if path:
            if not path.lower().endswith(".shp"):
                path += ".shp"
            self.save_path_edit.setText(path)

    def get_params(self):
        try:
            return {
                "lat1": float(self.lat1_edit.text()),
                "lon1": float(self.lon1_edit.text()),
                "lat2": float(self.lat2_edit.text()),
                "lon2": float(self.lon2_edit.text()),
                "save_path": self.save_path_edit.text()
            }
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的数字")
            return None
