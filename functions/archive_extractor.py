# functions/archive_extractor.py
import os
import zipfile
import tarfile
import rarfile

from dialogs.ArchiveExtractDialog import ArchiveExtractDialog
from worker_pool import run_in_thread

def launch_extract_gui(window):
    dialog = ArchiveExtractDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: extract_core(**params, window=w), window)

def extract_core(input_dir, output_dir, window):
    import shutil
    window.log("\n===== 批量解压任务开始 =====")
    window.log(f"📂 输入目录：{input_dir}")
    window.log(f"💾 保存目录：{output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    archive_files = [f for f in files if is_supported_archive(f)]
    if not archive_files:
        window.log("⚠️ 没有找到支持的压缩包")
        return

    for fname in archive_files:
        input_path = os.path.join(input_dir, fname)
        name_wo_ext = strip_archive_suffix(fname)
        temp_extract_path = os.path.join(output_dir, f"__tmp_{name_wo_ext}")

        # 💥 如果之前有残留，强制删除
        if os.path.exists(temp_extract_path):
            shutil.rmtree(temp_extract_path)
        os.makedirs(temp_extract_path, exist_ok=True)

        try:
            suffix = fname.lower()
            if suffix.endswith(".zip"):
                with zipfile.ZipFile(input_path, 'r') as zf:
                    zf.extractall(temp_extract_path)
            elif suffix.endswith(".rar"):
                with rarfile.RarFile(input_path) as rf:
                    rf.extractall(temp_extract_path)
            elif suffix.endswith((".tar", ".tar.gz", ".tgz", ".gz", ".bz2")):
                with tarfile.open(input_path) as tf:
                    tf.extractall(temp_extract_path)
            else:
                continue

            contents = os.listdir(temp_extract_path)
            if len(contents) == 1:
                only_item = contents[0]
                only_item_path = os.path.join(temp_extract_path, only_item)
                if os.path.isdir(only_item_path):
                    final_path = os.path.join(output_dir, only_item)
                    if os.path.exists(final_path):
                        shutil.rmtree(final_path)
                    shutil.move(only_item_path, final_path)
                    os.rmdir(temp_extract_path)
                    window.log(f"✅ 解压完成（扁平化）：{fname}")
                    continue

            final_path = os.path.join(output_dir, name_wo_ext)
            if os.path.exists(final_path):
                shutil.rmtree(final_path)
            shutil.move(temp_extract_path, final_path)
            window.log(f"✅ 解压完成：{fname}")

        except Exception as e:
            window.log(f"❌ 解压失败：{fname}，错误：{e}")
            try:
                shutil.rmtree(temp_extract_path)
            except:
                pass

    window.log("✅ 批量解压任务完成")

def is_supported_archive(filename):
    lname = filename.lower()
    return (
        lname.endswith(".zip")
        or lname.endswith(".rar")
        or lname.endswith(".tar")
        or lname.endswith(".tar.gz")
        or lname.endswith(".tar.bz2")
        or lname.endswith(".tar.xz")
        or lname.endswith(".tgz")
        or lname.endswith(".gz")
        or lname.endswith(".bz2")
    ) and not lname.endswith(".7z")

def strip_archive_suffix(filename):
    lname = filename.lower()
    for ext in [".tar.gz", ".tar.bz2", ".tar.xz", ".tar", ".tgz", ".zip", ".rar", ".gz", ".bz2"]:
        if lname.endswith(ext):
            return filename[: -len(ext)]
    return os.path.splitext(filename)[0]
