# 📦 遥感科研工具集中营

一个面向遥感与摄影测量科研人员的桌面数据处理工具箱。  
支持批量影像正射、点云抽稀、格式转换、Shapefile提取与优选、金字塔构建、文件操作、批量解压等常用科研功能。

> 基于 PyQt5 + GDAL + GeoPandas 构建，适用于大图、大数据、高效率处理场景。

---

## 🚀 功能模块

- [x] 生成矩形边界（SHP）
- [x] 影像优选（基于区域连通性与贡献面积的影像筛选）
- [x] 影像边界SHP提取（自动识别RPC并批量输出边界Shapefile）
- [x] SHP合并
- [x] SHP分类
- [x] 构建影像金字塔（支持内嵌、.ovr 和 .rrd 格式）
- [x] 删除/移动指定文件夹
- [x] 激光数据格式转换（CSV → TXT）
- [x] 激光点均匀抽稀（支持千万级激光点）
- [x] DSM重采样
- [x] 批量影像正射（RPC + DEM + 米级分辨率自动换算）
- [x] 批量解压（支持 zip/rar/tar.gz，排除 7z）

---

## 🖥️ 使用方法

```bash
conda create -n rs-tools python=3.9 -y
conda activate rs-tools
conda install pyqt geopandas rasterio fiona gdal shapely numpy opencv -c conda-forge
```

运行主程序：

```bash
python main.py
```

---

## 📂 项目结构

```
遥感科研工具集中营/
├── main.py                    # 主程序入口
├── main_window.py             # 主界面与菜单注册
├── worker_pool.py             # 通用线程池模块
├── dialogs/                   # 所有功能的对话框界面
│   ├── ImageSelectDialog.py
│   ├── PyramidDialog.py
│   └── ImageBoundaryExtractDialog.py
├── functions/                 # 各个功能模块的具体实现
│   ├── image_selector.py
│   ├── pyramid_builder.py
│   └── image_boundary_extractor.py
└── README.md
```

---

## 📫 联系与贡献

如你在使用中有任何功能需求或发现问题，欢迎提交 Issue 或 PR！
