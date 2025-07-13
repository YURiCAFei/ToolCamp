import os
from tqdm import tqdm
from dialogs.LidarMergeDialog import LidarMergeDialog
from worker_pool import run_in_thread

def match_lidar_file(lidar_files, image_name):
    """
    匹配规则：影像名以“前缀_XXX”，激光点文件名为“前缀_merged.txt”
    只要前缀一致，即可匹配
    """
    for f in lidar_files:
        if not f.endswith('_merged.txt'):
            continue
        prefix = f.replace('_merged.txt', '')
        if image_name.startswith(prefix):
            return f
    return None

def merge_lidar_by_group(lidar_dir, group_txt_path, save_dir, window):
    window.log("\n===== 激光点分组合并任务开始 =====")
    window.log(f"📂 点云目录：{lidar_dir}")
    window.log(f"📄 分组说明文件：{group_txt_path}")
    window.log(f"💾 保存路径：{save_dir}")
    os.makedirs(save_dir, exist_ok=True)

    # 所有激光点txt文件
    lidar_files = [f for f in os.listdir(lidar_dir) if f.lower().endswith('.txt')]
    lidar_files_full = [os.path.join(lidar_dir, f) for f in lidar_files]

    # 读取分组信息
    with open(group_txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    group_data = {}
    current_group = None
    for line in lines:
        line = line.strip()
        if line.startswith("group_"):
            current_group = line.replace(":", "")
            group_data[current_group] = []
        elif line.startswith("-"):
            name = line.replace("-", "").strip()
            group_data[current_group].append(name)

    # 合并每组
    for group, img_names in group_data.items():
        merged_points = []
        for img_name in img_names:
            matched = match_lidar_file(lidar_files, img_name)
            if matched is None:
                window.log(f"⚠️ 未找到匹配：{img_name}")
                continue

            full_path = os.path.join(lidar_dir, matched)
            with open(full_path, 'r') as f:
                lines = f.readlines()
                if not lines:
                    continue
                num_pts = int(lines[0].strip())
                merged_points.extend(lines[1:])  # 保留点数据，不包括第一行

        total_points = len(merged_points)
        save_path = os.path.join(save_dir, f"{group}.txt")
        with open(save_path, 'w') as f:
            f.write(f"{total_points}\n")
            f.writelines(merged_points)
        window.log(f"✅ 写入：{group}.txt，共合并 {total_points} 个点")

    window.log("🎉 激光点分组合并任务完成\n")

def merge_lidar_gui(window):
    dialog = LidarMergeDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: merge_lidar_by_group(**params, window=w), window)
