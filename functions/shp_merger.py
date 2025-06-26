# functions/shp_merger.py
import os
import geopandas as gpd
from dialogs.ShpMergeDialog import ShpMergeDialog
from worker_pool import run_in_thread
import pandas as pd

def merge_shp_gui(window):
    dialog = ShpMergeDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: merge_shp_core(**params, window=w), window)

def merge_shp_core(input_dir, output_dir, window):
    window.log("\n===== SHP合并任务开始 =====")
    window.log(f"📂 输入路径：{input_dir}")
    window.log(f"💾 保存路径：{output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    for subfolder in os.listdir(input_dir):
        sub_path = os.path.join(input_dir, subfolder)
        if not os.path.isdir(sub_path):
            continue

        shp_files = [
            os.path.join(sub_path, f) for f in os.listdir(sub_path)
            if f.lower().endswith(".shp")
        ]
        if not shp_files:
            window.log(f"⚠️ 跳过：{subfolder}（无shp文件）")
            continue

        try:
            gdfs = [gpd.read_file(f) for f in shp_files]
            merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)
            save_dir = os.path.join(output_dir, subfolder)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{subfolder}_merged.shp")
            merged.to_file(save_path, encoding="utf-8")
            window.log(f"✅ 合并完成：{save_path}")
        except Exception as e:
            window.log(f"❌ 合并失败：{subfolder}，错误：{e}")

    window.log("✅ SHP合并任务完成\n")
