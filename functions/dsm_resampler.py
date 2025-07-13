import os
import math
from osgeo import gdal
from dialogs.DsmResampleDialog import DsmResampleDialog
from worker_pool import run_in_thread

def resample_dsm_gui(window):
    dialog = DsmResampleDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: resample_dsm_core(**params, window=w), window)

def resample_dsm_core(input_dir, output_dir, target_resolution, window):
    import os
    import math
    from osgeo import gdal, osr
    import numpy as np

    window.log("\n===== DSM降采样任务开始 =====")
    window.log(f"📂 输入路径：{input_dir}")
    window.log(f"💾 输出路径：{output_dir}")
    window.log(f"🎯 目标分辨率：{target_resolution} 米（自动识别坐标系）")
    os.makedirs(output_dir, exist_ok=True)

    tif_exts = ('.tif', '.tiff', '.TIF', '.TIFF')

    for folder in os.listdir(input_dir):
        sub_path = os.path.join(input_dir, folder)
        if not os.path.isdir(sub_path):
            continue

        save_sub = os.path.join(output_dir, folder)
        os.makedirs(save_sub, exist_ok=True)

        for fname in os.listdir(sub_path):
            if not fname.endswith(tif_exts):
                continue

            src_path = os.path.join(sub_path, fname)
            dst_path = os.path.join(save_sub, fname)

            try:
                ds = gdal.Open(src_path)
                if not ds:
                    raise RuntimeError("无法打开DSM文件")

                proj = ds.GetProjection()
                srs = osr.SpatialReference(wkt=proj)
                is_geographic = srs.IsGeographic()

                # 默认设置
                xres = yres = target_resolution

                if is_geographic:
                    # 经纬度坐标（单位是度），需要换算
                    width = ds.RasterXSize
                    height = ds.RasterYSize
                    gt = ds.GetGeoTransform()
                    center_lat = gt[3] + gt[5] * height / 2
                    if abs(center_lat) > 89.0:
                        center_lat = 89.0
                    meters_per_degree = 111320 * math.cos(math.radians(center_lat))
                    deg_res = target_resolution / meters_per_degree
                    xres = yres = deg_res
                    window.log(f"🌐 {fname} 是地理坐标系，lat≈{center_lat:.4f}，1°≈{meters_per_degree:.2f}m")
                else:
                    window.log(f"🗺️ {fname} 是投影坐标系，直接使用 {target_resolution}m")

                # 执行降采样，保持原始坐标系
                gdal.Warp(
                    dst_path,
                    src_path,
                    xRes=xres,
                    yRes=yres,
                    resampleAlg="bilinear"
                )

                ds = None
                window.log(f"✅ 降采样完成：{folder}/{fname}")

            except Exception as e:
                window.log(f"❌ 降采样失败：{folder}/{fname}，错误：{e}")

    window.log("✅ DSM降采样任务完成\n")
