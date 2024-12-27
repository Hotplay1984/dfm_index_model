# DFM Index Model

基于动态因子模型（Dynamic Factor Model）的宏观经济指数构建工具。该工具通过Wind Python API获取中国宏观经济指标数据，经过数据清洗和预处理后，使用动态因子模型提取共同驱动因素，最终生成一个能够反映宏观经济整体走势的综合指数。

## 项目目的

1. 从Wind数据库获取关键宏观经济指标数据
2. 对原始数据进行清洗、标准化和预处理
3. 使用动态因子模型（DFM）提取各指标的共同驱动因素
4. 生成反映宏观经济整体走势的综合指数时间序列

## 配置文件

项目使用`.ini`格式的配置文件来管理宏观经济指标的设置。配置文件默认位置：

- 开发环境：`~/.config/dfm_index_model/macro_indicators.ini`
- 生产环境：`/etc/dfm_index_model/macro_indicators.ini`

也可以通过环境变量 `DFM_INDEX_CONFIG` 指定配置文件路径。

### 配置文件示例

```ini
[DEFAULT]
# 宏观指标配置文件

[S0027012]
name = 产量:发电量
indicator_type = 当期值
dimension = 增长
stl = trend

[S0027571]
name = 产量:铝材
indicator_type = 当期值
dimension = 增长
stl = trend

# ... 更多指标配置
```

### 配置项说明

- `name`: 指标名称
- `indicator_type`: 指标类型（当期值/年累计值/环比值）
- `dimension`: 指标维度（增长）
- `stl`: 时间序列分解方法（trend）

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置配置文件路径（可选）：
```bash
export DFM_INDEX_CONFIG=~/.config/dfm_index_model/macro_indicators.ini
```

3. 运行模型：
```python
from dfm_index_model import IndexModel

# 初始化模型
model = IndexModel()

# 获取并处理数据
model.fetch_data()
model.process_data()

# 运行DFM模型并获取指数
index = model.generate_index()
```

## 项目结构

```
dfm_index_model/
├── __init__.py
├── model.py          # 核心模型实现
├── data_processor.py # 数据处理模块
└── utils.py         # 工具函数

configs/
└── macro_indicators.ini  # 示例配置文件

notebooks/
└── examples/        # 示例notebook
```

## 依赖项

- Python >= 3.8
- pandas
- numpy
- statsmodels
- WindPy

## 注意事项

1. 需要有效的Wind Python API访问权限
2. 配置文件中的Wind代码需要与数据库保持一致
3. 建议将配置文件放在系统配置目录，与源代码分离

## 许可证

[添加许可证信息]

## 贡献指南

[添加贡献指南] 