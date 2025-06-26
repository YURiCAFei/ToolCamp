# functions/shp_classifier.py
import os
import shutil
import geopandas as gpd
from dialogs.ShpClassifyDialog import ShpClassifyDialog
from worker_pool import run_in_thread

def classify_shp_gui(window):
    dialog = ShpClassifyDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: classify_shp_core(**params, window=w), window)

def classify_shp_core(image_dir, shp_dir, output_dir, window):
    import os
    import shutil
    import geopandas as gpd
    import networkx as nx

    window.log("\n===== SHP分类任务开始 =====")
    window.log(f"📂 影像路径：{image_dir}")
    window.log(f"📂 SHP路径：{shp_dir}")
    window.log(f"💾 输出路径：{output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    subfolders = sorted(os.listdir(image_dir))
    shp_paths = []
    folder_names = []

    for name in subfolders:
        img_sub = os.path.join(image_dir, name)
        shp_sub = os.path.join(shp_dir, name)
        if not os.path.isdir(img_sub) or not os.path.isdir(shp_sub):
            continue

        shp_file = next((f for f in os.listdir(shp_sub) if f.lower().endswith(".shp")), None)
        if shp_file:
            shp_paths.append(os.path.join(shp_sub, shp_file))
            folder_names.append(name)

    if not shp_paths:
        window.log("⚠️ 未找到任何SHP文件，任务结束")
        return

    # 加载所有几何边界
    geometries = []
    for shp_path in shp_paths:
        gdf = gpd.read_file(shp_path)
        union = gdf.unary_union
        geometries.append(union)

    gdf_all = gpd.GeoDataFrame({'geometry': geometries})
    gdf_all.crs = "EPSG:4326"  # 如有真实坐标系请替换

    # 构建空间索引 + 邻接图
    sindex = gdf_all.sindex
    G = nx.Graph()

    for i, geom in enumerate(gdf_all.geometry):
        candidates = list(sindex.intersection(geom.bounds))
        for j in candidates:
            if i >= j:
                continue
            if geom.intersects(gdf_all.geometry[j]):
                G.add_edge(i, j)

    # 提取连通分量
    groups = list(nx.connected_components(G))
    all_idxs = set(range(len(gdf_all)))
    connected = set().union(*groups)
    for solo in all_idxs - connected:
        groups.append({solo})

    summary_lines = []

    # 输出结果 + 生成分类说明
    for idx, group in enumerate(groups):
        group_name = f"group_{idx + 1}"
        group_out = os.path.join(output_dir, group_name)
        os.makedirs(group_out, exist_ok=True)

        summary_lines.append(f"{group_name}:")
        for i in group:
            name = folder_names[i]
            summary_lines.append(f"  - {name}")
            src_folder = os.path.join(image_dir, name)
            for item in os.listdir(src_folder):
                src_path = os.path.join(src_folder, item)
                dst_path = os.path.join(group_out, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)

        window.log(f"✅ 已保存：{group_out}（共 {len(group)} 个）")

    # 写入说明文档
    summary_path = os.path.join(output_dir, "分类结果说明.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    window.log(f"\n📄 分类说明文件已生成：{summary_path}")
    window.log("✅ SHP分类任务完成\n")
