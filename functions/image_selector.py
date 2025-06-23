# functions/image_selector.py
import os
import shutil
import geopandas as gpd
import pandas as pd

from dialogs.ImageSelectDialog import ImageSelectDialog
from worker_pool import run_in_thread

def select_images_gui(window):
    dialog = ImageSelectDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: select_images_core(**params, window=w), window)

def select_images_core(shp_files, target_shp, destination_folder, max_images, window):
    window.log("\n===== 影像优选任务开始 =====")
    try:
        region_gdf = gpd.read_file(target_shp)
        region_polygon = region_gdf.unary_union

        all_images = []
        for shp_path in shp_files:
            image_gdf = gpd.read_file(shp_path)
            image_gdf['image_name'] = os.path.basename(shp_path)
            all_images.append(image_gdf)

        images_gdf = gpd.GeoDataFrame(pd.concat(all_images, ignore_index=True), crs=all_images[0].crs)
        selected_images = []
        remaining_area = region_polygon
        connected_region = None

        while remaining_area.area > 0 and not images_gdf.empty and len(selected_images) < max_images:
            images_gdf['contribution_area'] = images_gdf.geometry.apply(
                lambda geom: geom.intersection(remaining_area).area)
            images_gdf['overlap_ratio'] = images_gdf.geometry.apply(
                lambda geom: geom.intersection(remaining_area).area / geom.area if geom.area > 0 else 0)
            images_gdf['weight'] = images_gdf['contribution_area'] * (1 - images_gdf['overlap_ratio'])

            if connected_region is None:
                best_image_row = images_gdf.loc[images_gdf['weight'].idxmax()]
            else:
                adjacent_images = images_gdf[images_gdf.geometry.apply(lambda geom: geom.intersects(connected_region))]
                if adjacent_images.empty:
                    window.log("⚠️ 无法继续连通区域影像")
                    break
                best_image_row = adjacent_images.loc[adjacent_images['weight'].idxmax()]

            if best_image_row['contribution_area'] == 0:
                window.log("⚠️ 无新增覆盖区域")
                break

            best_image_geom = best_image_row.geometry
            best_image_name = best_image_row['image_name']
            connected_region = best_image_geom if connected_region is None else connected_region.union(best_image_geom)
            remaining_area = remaining_area.difference(best_image_geom)
            selected_images.append(best_image_name)
            images_gdf = images_gdf[images_gdf['image_name'] != best_image_name]

        os.makedirs(destination_folder, exist_ok=True)
        for selected_image in selected_images:
            base_name = os.path.splitext(selected_image)[0]
            source_folder = os.path.dirname(shp_files[0])
            for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                f = f"{base_name}{ext}"
                src = os.path.join(source_folder, f)
                if os.path.exists(src):
                    shutil.copy(src, destination_folder)
                    window.log(f"📁 已复制：{f}")

        window.log("✔️ 优选完成，共选中：\n" + "\n".join(selected_images))
        window.log("===== 影像优选任务完成 =====")
    except Exception as e:
        window.log(f"❌ 影像优选功能异常退出：{e}")
    window.log("")
