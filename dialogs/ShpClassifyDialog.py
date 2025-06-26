# dialogs/ShpClassifyDialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QFileDialog, QHBoxLayout
)

class ShpClassifyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SHP分类")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.image_dir = QLineEdit()
        self.shp_dir = QLineEdit()
        self.output_dir = QLineEdit()

        btn_img = QPushButton("选择影像主目录")
        btn_img.clicked.connect(self.select_image_dir)

        btn_shp = QPushButton("选择SHP主目录")
        btn_shp.clicked.connect(self.select_shp_dir)

        btn_output = QPushButton("选择输出目录")
        btn_output.clicked.connect(self.select_output_dir)

        layout.addLayout(form)

        self._add_form_row(form, "影像路径", self.image_dir, btn_img)
        self._add_form_row(form, "SHP路径", self.shp_dir, btn_shp)
        self._add_form_row(form, "输出路径", self.output_dir, btn_output)

        self.ok_btn = QPushButton("开始分类")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def _add_form_row(self, form, label, line_edit, button):
        layout = QHBoxLayout()
        layout.addWidget(line_edit)
        layout.addWidget(button)
        form.addRow(label, layout)
        return layout

    def select_image_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择影像主目录")
        if folder:
            self.image_dir.setText(folder)

    def select_shp_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择SHP主目录")
        if folder:
            self.shp_dir.setText(folder)

    def select_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出路径")
        if folder:
            self.output_dir.setText(folder)

    def get_params(self):
        return {
            "image_dir": self.image_dir.text(),
            "shp_dir": self.shp_dir.text(),
            "output_dir": self.output_dir.text()
        }
