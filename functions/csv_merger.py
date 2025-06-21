# functions/csv_merger.py
import os, glob, csv
from dialogs.CsvMergeDialog import CsvMergeDialog
from worker_pool import run_in_thread

def batch_merge_csv_gui(window):
    dialog = CsvMergeDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: merge_core(**params, window=w), window)


def merge_core(parent_folder, output_dir, window):
    window.log("\n===== 激光数据格式转换任务开始 =====")
    os.makedirs(output_dir, exist_ok=True)

    subfolders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder)
                  if os.path.isdir(os.path.join(parent_folder, d))]

    for folder in subfolders:
        output_file = os.path.join(output_dir, f"{os.path.basename(folder)}_merged.txt")
        try:
            _merge_csv(folder, output_file)
            window.log(f"🟢 合并完成：{output_file}")
        except Exception as e:
            window.log(f"❌ 处理失败 {folder}：{e}")

    window.log("✅ 激光数据格式转换任务完成")


def _merge_csv(folder_path, output_file):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    all_points = []

    for file in csv_files:
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            idx = {k: header.index(k) for k in ['lon_ph', 'lat_ph', 'h_ph', 'classification', 'signal_conf_ph', 'beam_strength']}
            for row in reader:
                if len(row) > max(idx.values()) and row[idx['beam_strength']] == "strong" and int(row[idx['signal_conf_ph']]) > 2 and int(row[idx['classification']]) == 1:
                    all_points.append((row[idx['lat_ph']], row[idx['lon_ph']], row[idx['h_ph']]))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{len(all_points)}\n")
        for i, (lat, lon, h) in enumerate(all_points):
            f.write(f"{i+1}\t{lat}\t{lon}\t{h}\n")
