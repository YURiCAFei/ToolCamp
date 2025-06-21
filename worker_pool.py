# worker_pool.py
from PyQt5.QtCore import QThread
import traceback

_active_threads = []  # 全局线程列表，防止线程被垃圾回收

def run_in_thread(task_func, window):
    """在后台线程中运行指定函数，并自动日志输出"""
    class TaskThread(QThread):
        def run(self_inner):
            try:
                task_func(window)
            except Exception as e:
                tb = traceback.format_exc()
                window.log(f"❌ 异常：{e}\n{tb}")
            finally:
                _active_threads.remove(self_inner)  # 清理引用

    thread = TaskThread()
    _active_threads.append(thread)
    thread.start()
