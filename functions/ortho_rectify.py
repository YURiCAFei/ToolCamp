# functions/ortho_rectify.py
import os
from osgeo import gdal
from pyproj import Geod
from dialogs.OrthoRectifyDialog import OrthoRectifyDialog
from worker_pool import run_in_thread

def launch_orthorectify_gui(window):
    dialog = OrthoRectifyDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: ortho_core(**params, window=w), window)

def ortho_core(input_folder, dem_folder, output_folder, resolution_m, window):
    window.log("\n===== 影像正射任务开始 =====")
    window.log(f"📂 影像目录：{input_folder}")
    window.log(f"🌄 DEM目录：{dem_folder}")
    window.log(f"💾 输出目录：{output_folder}")
    window.log(f"📏 分辨率（米）：{resolution_m}")

    os.makedirs(output_folder, exist_ok=True)
    tif_list = [f for f in os.listdir(input_folder) if f.lower().endswith((".tif", ".tiff"))]

    if not tif_list:
        window.log("⚠️ 没有找到有效影像文件")
        return

    for tif_name in tif_list:
        name_wo_ext = os.path.splitext(tif_name)[0]
        tif_path = os.path.join(input_folder, tif_name)
        rpc_path = os.path.join(input_folder, f"{name_wo_ext}_rpc.txt")
        dem_path = os.path.join(dem_folder, tif_name)  # DEM 必须同名
        out_path = os.path.join(output_folder, tif_name)

        if not os.path.exists(rpc_path):
            window.log(f"⚠️ 缺失RPC：{rpc_path}")
            continue
        if not os.path.exists(dem_path):
            window.log(f"⚠️ 缺失DEM：{dem_path}")
            continue

        try:
            degrees = meters_to_degrees(23.0, resolution_m)  # 默认纬度23°，或可从 RPC 中解析
            window.log(f"📌 开始正射：{tif_name} @ {degrees:.8f}°")

            dataset = gdal.Open(tif_path, gdal.GA_ReadOnly)
            gdal.Warp(out_path, dataset,
                      dstSRS='EPSG:4326',
                      xRes=degrees,
                      yRes=degrees,
                      resampleAlg=gdal.GRIORA_Bilinear,
                      rpc=True,
                      transformerOptions=[f"RPC_DEM={dem_path}"])

            window.log(f"✅ 正射完成：{out_path}")
        except Exception as e:
            window.log(f"❌ 正射失败 {tif_name}：{e}")

    window.log("✅ 全部正射任务完成")

def meters_to_degrees(lat, meters):
    geod = Geod(ellps='WGS84')
    lon2, _, _ = geod.fwd(0, lat, 90, meters)
    return lon2
