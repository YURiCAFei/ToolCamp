# functions/folder_mover.py
import os, shutil
from dialogs.FolderMoveDialog import FolderMoveDialog
from worker_pool import run_in_thread

def move_folders_gui(window):
    dialog = FolderMoveDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: move_core(**params, window=w), window)

def move_core(source_root, txt_path, target_root, window):
    window.log("\n===== 移动指定文件夹任务开始 =====")
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            folder_names = [line.strip() for line in f if line.strip()]
    except Exception as e:
        window.log(f"❌ 无法读取列表：{e}")
        return

    for name in folder_names:
        src = os.path.join(source_root, name)
        dst = os.path.join(target_root, name)
        if os.path.isdir(src):
            try:
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.move(src, dst)
                window.log(f"✅ 移动：{src} → {dst}")
            except Exception as e:
                window.log(f"❌ 移动失败：{src} → {e}")
        else:
            window.log(f"⚠️ 未找到：{src}")

    window.log("✅ 移动指定文件夹任务完成")
