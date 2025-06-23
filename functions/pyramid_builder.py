# functions/pyramid_builder.py
import os
from osgeo import gdal
from dialogs.PyramidDialog import PyramidDialog
from worker_pool import run_in_thread

def build_pyramids_gui(window):
    dialog = PyramidDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: build_pyramids_core(**params, window=w), window)

def build_pyramids_core(input_dir, types, window):
    window.log("\n===== 构建影像金字塔任务开始 =====")
    try:
        tif_files = [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if f.lower().endswith((".tif", ".tiff", ".img"))
        ]
        if not tif_files:
            window.log("❌ 未找到影像文件")
            window.log("===== 构建影像金字塔任务完成 =====\n")
            return

        for tif in tif_files:
            window.log(f"📄 处理：{os.path.basename(tif)}")

            if types.get("embed"):
                _build_pyramid(tif, overview_type="embed")
                window.log("✅ 内嵌金字塔完成")

            if types.get("ovr"):
                _build_pyramid(tif, overview_type="ovr")
                window.log("✅ .ovr 金字塔完成")

            if types.get("rrd"):
                _build_pyramid(tif, overview_type="rrd")
                window.log("✅ .rrd 金字塔完成")

    except Exception as e:
        window.log(f"❌ 异常退出：{e}")

    window.log("===== 构建影像金字塔任务完成 =====\n")

def _build_pyramid(image_path, overview_type="embed"):
    # 设置金字塔格式
    if overview_type == "ovr":
        gdal.SetConfigOption("USE_RRD", "NO")
        gdal.SetConfigOption("OVERVIEW_FORMAT", "GTiff")
    elif overview_type == "rrd":
        gdal.SetConfigOption("USE_RRD", "YES")
        gdal.SetConfigOption("OVERVIEW_FORMAT", "HFA")
    else:
        gdal.SetConfigOption("USE_RRD", None)
        gdal.SetConfigOption("OVERVIEW_FORMAT", None)

    # 打开影像
    ds = gdal.Open(image_path, gdal.GA_Update)
    if ds is None:
        raise RuntimeError(f"无法打开影像：{image_path}")

    # 设置压缩和构建
    levels = [2, 4, 8, 16]
    gdal.SetConfigOption("COMPRESS_OVERVIEW", "LZW")
    ds.BuildOverviews("GAUSS", levels)
    ds = None
