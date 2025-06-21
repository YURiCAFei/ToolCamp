# functions/rect_creator.py
import os
import geopandas as gpd
from shapely.geometry import Polygon
from dialogs.RectDialog import RectDialog
from worker_pool import run_in_thread

def create_rectangle_gui(window):
    print("📌 打开对话框")
    dialog = RectDialog(window)
    if dialog.exec_():
        print("📌 点击了执行")
        params = dialog.get_params()
        print("📌 获取参数：", params)
        if not params:
            window.log("⚠️ 参数为空，未执行")
            return

        # ✅ 使用简化后的线程池调用 create_core
        run_in_thread(lambda w: create_core(**params, window=w), window)

def create_core(lat1, lon1, lat2, lon2, save_path, window):
    window.log("\n===== 生成矩形边界任务开始 =====")
    try:
        top, bottom = max(lat1, lat2), min(lat1, lat2)
        left, right = min(lon1, lon2), max(lon1, lon2)
        polygon = Polygon([(left, top), (right, top), (right, bottom), (left, bottom), (left, top)])
        gdf = gpd.GeoDataFrame(index=[0], geometry=[polygon], crs="EPSG:4326")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        gdf.to_file(save_path, driver="ESRI Shapefile", encoding="utf-8")
        window.log(f"✅ 矩形边界已保存：{save_path}")
    except Exception as e:
        window.log(f"❌ 生成失败：{e}")
    else:
        window.log("✅ 生成矩形边界任务完成")
