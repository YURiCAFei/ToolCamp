from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QFileDialog, QHBoxLayout

class FolderCreatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建指定文件夹")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.src = QLineEdit()
        self.dst = QLineEdit()

        btn_src = QPushButton("选择路径")
        btn_src.clicked.connect(self.select_src)

        btn_dst = QPushButton("选择输出路径")
        btn_dst.clicked.connect(self.select_dst)

        form.addRow("源路径", self._with_btn(self.src, btn_src))
        form.addRow("保存路径", self._with_btn(self.dst, btn_dst))

        self.ok_btn = QPushButton("创建文件夹")
        self.ok_btn.clicked.connect(self.accept)

        layout.addLayout(form)
        layout.addWidget(self.ok_btn)
        self.setLayout(layout)

    def _with_btn(self, lineedit, button):
        layout = QHBoxLayout()
        layout.addWidget(lineedit)
        layout.addWidget(button)
        return layout

    def select_src(self):
        path = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if path:
            self.src.setText(path)

    def select_dst(self):
        path = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if path:
            self.dst.setText(path)

    def get_params(self):
        return {
            "src_dir": self.src.text(),
            "dst_dir": self.dst.text()
        }
