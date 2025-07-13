# main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QAction, QFileDialog,
    QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG

from functions.rect_creator import create_rectangle_gui
from functions.folder_deleter import delete_folders_gui
from functions.folder_mover import move_folders_gui
from functions.csv_merger import batch_merge_csv_gui
from functions.lidar_downsampler import batch_downsample_gui
from functions.ortho_rectify import launch_orthorectify_gui
from functions.archive_extractor import launch_extract_gui
from functions.image_selector import select_images_gui
from functions.pyramid_builder import build_pyramids_gui
from functions.image_boundary_extractor import image_boundary_gui
from functions.shp_merger import merge_shp_gui
from functions.shp_classifier import classify_shp_gui
from functions.dsm_resampler import resample_dsm_gui
from functions.merge_lidar_by_group import merge_lidar_gui
from functions.folder_creator import create_folders_gui


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
        self.add_action(file_menu, "新建指定文件夹", create_folders_gui)
        self.add_action(file_menu, "批量解压", launch_extract_gui)

        # 摄影测量
        survey_menu = menubar.addMenu("摄影测量")

        # ├─ SHP
        shp_menu = QMenu("SHP", self)
        survey_menu.addMenu(shp_menu)

        # 子菜单
        shp_gen_menu = QMenu("SHP生成", self)
        shp_menu.addMenu(shp_gen_menu)
        self.add_action(shp_gen_menu, "生成矩形边界", create_rectangle_gui)
        self.add_action(shp_gen_menu, "影像边界SHP提取", image_boundary_gui)
        self.add_action(shp_gen_menu, "SHP合并", merge_shp_gui)

        # 子菜单：SHP处理与分析
        shp_proc_menu = QMenu("SHP处理与分析", self)
        shp_menu.addMenu(shp_proc_menu)
        self.add_action(shp_proc_menu, "影像优选", select_images_gui)
        self.add_action(shp_proc_menu, "SHP分类", classify_shp_gui)
        
        # ├─ DSM生产
        dsm_menu = QMenu("DSM生产", self)
        survey_menu.addMenu(dsm_menu)
        self.add_action(dsm_menu, "激光数据格式转换", batch_merge_csv_gui)
        self.add_action(dsm_menu, "激光点均匀抽稀", batch_downsample_gui)
        self.add_action(dsm_menu, "激光点分组合并", merge_lidar_gui)
        self.add_action(dsm_menu, "DSM重采样", resample_dsm_gui)

        # ├─ 图像处理
        image_menu = QMenu("图像处理", self)
        survey_menu.addMenu(image_menu)
        self.add_action(image_menu, "影像正射", launch_orthorectify_gui)
        self.add_action(image_menu, "构建影像金字塔", build_pyramids_gui)

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
