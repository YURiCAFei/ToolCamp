# functions/folder_deleter.py
import os, shutil
from dialogs.FolderDeleteDialog import FolderDeleteDialog
from worker_pool import run_in_thread

def delete_folders_gui(window):
    dialog = FolderDeleteDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: delete_core(**params, window=w), window)

def delete_core(root_path, txt_path, window):
    window.log("\n===== 删除指定文件夹任务开始 =====")
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            folder_names = [line.strip() for line in f if line.strip()]
    except Exception as e:
        window.log(f"❌ 无法读取列表：{e}")
        return

    for folder_name in folder_names:
        folder_path = os.path.join(root_path, folder_name)
        if os.path.isdir(folder_path):
            try:
                shutil.rmtree(folder_path)
                window.log(f"✅ 已删除：{folder_path}")
            except Exception as e:
                window.log(f"❌ 删除失败 {folder_path}：{e}")
        else:
            window.log(f"⚠️ 未找到：{folder_path}")
    window.log("✅ 删除指定文件夹任务完成")
