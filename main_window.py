# main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QAction, QFileDialog,
    QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG
from worker_pool import run_in_thread

from functions.rect_creator import create_rectangle_gui
from functions.folder_deleter import delete_folders_gui
from functions.folder_mover import move_folders_gui
from functions.csv_merger import batch_merge_csv_gui
from functions.lidar_downsampler import batch_downsample_gui
from functions.ortho_rectify import launch_orthorectify_gui
from functions.archive_extractor import launch_extract_gui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("遥感科研工具集中营")
        self.setMinimumSize(800, 600)

        # 日志输出框
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.setCentralWidget(self.log_output)

        # 菜单栏结构
        self.init_menus()

    def init_menus(self):
        menubar = self.menuBar()

        # 文件操作
        file_menu = menubar.addMenu("文件操作")
        self.add_action(file_menu, "删除指定文件夹", delete_folders_gui)
        self.add_action(file_menu, "移动指定文件夹", move_folders_gui)
        self.add_action(file_menu, "批量解压", launch_extract_gui)

        # 摄影测量
        survey_menu = menubar.addMenu("摄影测量")

        # ├─ SHP
        shp_menu = QMenu("SHP", self)
        survey_menu.addMenu(shp_menu)
        self.add_action(shp_menu, "生成矩形边界", create_rectangle_gui)

        # ├─ DSM生产
        dsm_menu = QMenu("DSM生产", self)
        survey_menu.addMenu(dsm_menu)
        self.add_action(dsm_menu, "激光数据格式转换", batch_merge_csv_gui)
        self.add_action(dsm_menu, "激光点均匀抽稀", batch_downsample_gui)

        # ├─ 图像处理
        image_menu = QMenu("图像处理", self)
        survey_menu.addMenu(image_menu)
        self.add_action(image_menu, "影像正射", launch_orthorectify_gui)

    def add_action(self, menu, label, func):
        action = QAction(label, self)
        action.triggered.connect(lambda: func(self))
        menu.addAction(action)

    def log(self, text: str):
        QMetaObject.invokeMethod(
            self.log_output,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, text)
        )
