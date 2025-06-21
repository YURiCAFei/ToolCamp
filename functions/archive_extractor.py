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
        out_folder = os.path.join(output_dir, strip_archive_suffix(fname))
        os.makedirs(out_folder, exist_ok=True)

        try:
            suffix = fname.lower()
            if suffix.endswith(".zip"):
                with zipfile.ZipFile(input_path, 'r') as zf:
                    zf.extractall(out_folder)
            elif suffix.endswith(".rar"):
                with rarfile.RarFile(input_path) as rf:
                    rf.extractall(out_folder)
            elif suffix.endswith((".tar", ".tar.gz", ".tgz", ".gz", ".bz2")):
                with tarfile.open(input_path) as tf:
                    tf.extractall(out_folder)
            else:
                continue
            window.log(f"✅ 解压完成：{fname}")
        except Exception as e:
            window.log(f"❌ 解压失败：{fname}，错误：{e}")

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
