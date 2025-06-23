import os
import geopandas as gpd
from shapely.geometry import Polygon
from osgeo import gdal
from dialogs.ImageBoundaryExtractDialog import ImageBoundaryExtractDialog
from worker_pool import run_in_thread

def image_boundary_gui(window):
    dialog = ImageBoundaryExtractDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: extract_image_boundaries(**params, window=w), window)

def extract_image_boundaries(input_dir, output_dir, window):
    window.log("\n===== 影像边界SHP提取任务开始 =====")
    window.log(f"📂 输入目录：{input_dir}")
    window.log(f"💾 输出目录：{output_dir}")
    tif_exts = ('.tif', '.tiff', '.TIF', '.TIFF')

    for subfolder in os.listdir(input_dir):
        sub_path = os.path.join(input_dir, subfolder)
        if not os.path.isdir(sub_path):
            continue

        for file in os.listdir(sub_path):
            if not file.endswith(tif_exts):
                continue

            tif_path = os.path.join(sub_path, file)
            rpc_path = find_rpc(tif_path)
            if not rpc_path:
                window.log(f"⚠️ 跳过（无RPC）：{file}")
                continue

            try:
                poly = get_rpc_polygon(tif_path)
                gdf = gpd.GeoDataFrame([{
                    "geometry": poly,
                    "image": file
                }], crs="EPSG:4326")

                save_dir = os.path.join(output_dir, subfolder)
                os.makedirs(save_dir, exist_ok=True)
                base_name = os.path.splitext(file)[0]
                shp_path = os.path.join(save_dir, base_name + ".shp")
                gdf.to_file(shp_path, encoding='utf-8')
                window.log(f"✅ 已保存：{shp_path}")

            except Exception as e:
                window.log(f"❌ 失败：{file}，错误：{e}")

    window.log("✅ 影像边界SHP提取任务完成\n")

def get_rpc_polygon(tif_path):
    ds = gdal.Open(tif_path)
    if not ds:
        raise RuntimeError("无法打开影像")

    width = ds.RasterXSize
    height = ds.RasterYSize
    corners = [
        (0, 0), (width, 0), (width, height), (0, height), (0, 0)
    ]

    rpc = ds.GetMetadata('RPC')
    if not rpc:
        raise RuntimeError("RPC信息缺失")

    # 优先使用 RPC 中的高度偏移（如果存在）
    height_off = float(rpc.get("HEIGHT_OFF", rpc.get("HeightOffset", rpc.get("ATLOFF", "0"))))

    transformer = gdal.Transformer(ds, None, ['METHOD=RPC'])
    lonlat_points = []
    for px, py in corners:
        success, geo = transformer.TransformPoint(False, px, py, height_off)
        if not success:
            raise RuntimeError(f"RPC 投影失败 at ({px},{py})")
        lonlat_points.append((geo[0], geo[1]))

    ds = None
    return Polygon(lonlat_points)

def find_rpc(tif_path):
    base = os.path.splitext(tif_path)[0]
    for ext in [".rpb", "_rpc.txt"]:
        candidate = base + ext
        if os.path.exists(candidate):
            return candidate
    return None
