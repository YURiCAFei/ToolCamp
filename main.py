# main.py
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
import sys
import os

os.environ['PROJ_LIB'] = '/home/yuki/anaconda3/envs/photogoblin-clean/share/proj'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
