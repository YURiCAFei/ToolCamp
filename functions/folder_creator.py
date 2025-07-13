import os
from dialogs.FolderCreatorDialog import FolderCreatorDialog
from worker_pool import run_in_thread

def create_folders_from_source(src_dir, dst_dir, window):
    window.log("===== 新建指定文件夹任务开始 =====")
    window.log(f"📂 输入路径：{src_dir}")
    window.log(f"📁 输出路径：{dst_dir}")

    if not os.path.exists(src_dir):
        window.log("❌ 输入路径不存在")
        return
    os.makedirs(dst_dir, exist_ok=True)

    count = 0
    for name in os.listdir(src_dir):
        sub_path = os.path.join(src_dir, name)
        if os.path.isdir(sub_path):
            new_folder = os.path.join(dst_dir, name)
            os.makedirs(new_folder, exist_ok=True)
            window.log(f"✅ 创建：{new_folder}")
            count += 1

    window.log(f"🎉 共创建 {count} 个文件夹\n")

def create_folders_gui(window):
    dialog = FolderCreatorDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: create_folders_from_source(**params, window=w), window)
