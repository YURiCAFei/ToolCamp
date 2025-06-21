# functions/lidar_downsampler.py
import os
from dialogs.LidarDownsampleDialog import LidarDownsampleDialog
from worker_pool import run_in_thread

def batch_downsample_gui(window):
    dialog = LidarDownsampleDialog(window)
    if dialog.exec_():
        params = dialog.get_params()
        run_in_thread(lambda w: downsample_core(**params, window=w), window)


def downsample_core(input_dir, output_dir, ratio, window):
    window.log("\n===== 激光点均匀抽稀任务开始 =====")
    window.log(f"📂 输入目录：{input_dir}")
    window.log(f"📁 输出目录：{output_dir}")
    window.log(f"📊 抽样比例：{ratio}")

    if not os.path.exists(input_dir):
        window.log("❌ 输入目录不存在")
        return

    os.makedirs(output_dir, exist_ok=True)
    txt_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    window.log(f"🧾 共检测到 {len(txt_files)} 个 .txt 文件")

    if not txt_files:
        window.log("⚠️ 输入目录中没有 .txt 文件")
        return

    for file in txt_files:
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)
        window.log(f"🛠️ 准备处理：{file}")
        try:
            msg = _downsample(input_path, output_path, ratio)
            window.log(msg or f"⚠️ 没有返回日志：{file}")
        except Exception as e:
            window.log(f"❌ 处理 {file} 出错：{e}")

    window.log("✅ 激光点均匀抽稀任务完成")


def _downsample(input_path, output_path, ratio):
    print(f"📥 打开文件: {input_path}")
    if not os.path.exists(input_path):
        return f"⚠️ 文件不存在：{input_path}"

    try:
        with open(input_path, 'r', encoding='utf-8') as fin:
            total_line = fin.readline()
            try:
                total = int(total_line.strip())
            except:
                return f"⚠️ 无法解析点数头部：{total_line.strip()}"

            if total == 0:
                return f"⚠️ 点数为0，跳过：{os.path.basename(input_path)}"

            count = max(1, int(total * ratio))
            interval = total / count
            selected_indexes = {int(i * interval) for i in range(count)}

            selected_lines = []
            for i, line in enumerate(fin):
                if i in selected_indexes:
                    selected_lines.append(line)
                if len(selected_lines) >= count:
                    break

    except Exception as e:
        return f"❌ 读取失败：{e}"

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as fout:
            fout.write(f"{len(selected_lines)}\n")
            fout.writelines(selected_lines)
    except Exception as e:
        return f"❌ 写入失败：{e}"

    return f"✅ 抽取 {len(selected_lines)}/{total} 点 → {os.path.basename(output_path)}"
