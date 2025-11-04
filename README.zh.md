# The Farmer Was Replaced 自动化工具集

English: [README.md](README.md)

## 项目简介
本仓库收录了 Steam 解谜游戏 [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/_/) 的自动化脚本。代码使用接近 Python 的语法，便于在常规编辑器中编写，但目标运行环境仍然是游戏内置语言。`__builtins__.py` 提供了游戏 API 的类型提示，让代码补全与静态检查更加顺畅。

## 仓库结构
```
.
├── __builtins__.py        # 游戏 API 的类型提示
├── config.example.py      # 作物优先级与阈值的示例配置
├── crop_cactus.py         # 仙人掌排序与收获流程
├── crop_carrots.py        # 胡萝卜种植助手
├── crop_dinosaur.py       # 恐龙小游戏自动化
├── crop_grass.py          # 草地快速收割
├── crop_maze.py           # 树篱迷宫求解与金币收集
├── crop_mix.py            # 伴生种植自动化
├── crop_pumpkins.py       # 巨型南瓜管理
├── crop_sunflowers.py     # 专注能量的向日葵模块
├── crop_trees.py          # 棋盘式树木种植
├── crop_weird.py          # 奇异物质采集策略
├── smart_priority.py      # 基于优先级的作物调度器
├── utils.py               # 通用移动与耕作工具
└── README.md              # 英文文档
```

## 智能优先级控制器 (`smart_priority.py`)
主循环会持续评估资源，并选择当前最合适的作物进行操作。
- 从 `config.py` 读取 `PRIORITY` 与 `THRESHOLDS`（请先复制 `config.example.py` 创建该文件）。
- 每轮决策前都会统计能量、胡萝卜、木材、南瓜、干草、肥料、水、仙人掌、奇异物质、骨头与金币数量。
- 根据资源缺口与紧急阈值为各作物评分，例如能量不足时优先种向日葵。
- 在执行前确认资源是否足够（通过 `get_cost` 查询成本，也会校验迷宫是否解锁）。
- 如果所有作物都无法执行，则回退到收割草地补给基础资源。

## 工具模块 (`utils.py`)
通用工具模块，用于简化移动与土地维护。
- `move_to(x, y)` 会考虑环形地图的最短路径，将无人机移动到指定坐标。
- `tilling()` 在需要时翻土，保证不同模块之间的用地状态一致。
- `water()` 与 `water_full()` 帮助维持理想的水分水平。

## 作物模块
每个 `crop_*.py` 文件都专注于一种作物或机制，可单独导入或由智能控制器调用。
- `crop_grass.farm_grass()` 清理全场、恢复草地并快速收割干草。
- `crop_trees.farm_trees()` 以棋盘方式种树，避免 16 倍邻接惩罚，并在等待期间自动浇水。
- `crop_carrots.farm_carrots()` 翻土、补种胡萝卜，并立即浇水获取 5 倍生长加速。
- `crop_pumpkins.farm_pumpkins()` 维持满场南瓜，记录枯萎坐标，只对受影响位置复种直到巨型南瓜成熟。
- `crop_sunflowers.farm_sunflowers()` 种植时记录花瓣数、保持高水位，并按照花瓣数从高到低收割以保留能量倍率。
- `crop_cactus.farm_cactus()` 先按行、再按列执行冒泡排序，最后从原点收割以确保获得平方收益。
- `crop_mix.farm_mixed(main_crop)` 收集伴生需求，优先满足需求最高的位置并在收获后清理场地。

## 特殊模块
- `crop_weird.py` 提供三种入口：`farm_weird_substance()` 使用草地加速感染，`farm_weird_substance_advanced()` 结合肥料与胡萝卜提升收益，`farm_weird_substance_chain()` 借助奇异物质扩散感染以节省肥料。
- `crop_dinosaur.py` 自动化恐龙帽小游戏，追踪尾巴路径避免碰撞，采用曼哈顿距离加辅助绕行策略，并提供 `farm_dinosaur_optimal()` 与 `farm_dinosaur_efficient()` 等变体适配不同仙人掌（苹果）预算。
- `crop_maze.py` 生成树篱迷宫，利用右手/左手法则或 `measure` 导航求解，并通过 `farm_maze_optimal()` 与 `farm_maze_smart()` 支持重用次数与迷宫尺寸的自动化设置。

## 快速上手
1. 复制示例配置：在 PowerShell 中执行 `Copy-Item config.example.py config.py`（macOS/Linux 可使用 `cp config.example.py config.py`）。
2. 编辑 `config.py`，设置你偏好的 `PRIORITY` 顺序与资源 `THRESHOLDS`。每个条目是一段描述作物名称及其可选参数（如迷宫大小、恐龙模式）的字典。
3. 在游戏内加载脚本并运行 `smart_priority.py`，让控制器循环托管种植决策。你也可以单独导入任意 `crop_*` 模块来获取特定资源。

示例配置片段：
```python
PRIORITY = [
    {"crop": "sunflowers"},
    {"crop": "mixed", "main": Entities.Tree},
    {"crop": "pumpkins"},
    {"crop": "maze", "mode": "smart", "size": 5},
]

THRESHOLDS = {
    "power_low": 100,
    "power_safe": 200,
    "carrot_min": 2000,
    "wood_min": 3000,
    "hay_min": 1000,
    "fertilizer_min": 5,
}
```

## 策略要点
- 巨型南瓜：使用枯萎坐标列表避免全图扫描，只在必要时复种。
- 向日葵：保存初始花瓣数，分批收割最大花瓣的植株以保持 5 倍能量奖励。
- 仙人掌：先行后列的冒泡排序既保证顺序，又减少不必要的移动距离。
- 伴生种植：统计需求并优先满足收益最高的位置，再统一清场。
- 恐龙：尾巴路径记录配合曼哈顿导航，让无人机在资源耗尽前保持安全移动。
- 迷宫：生成前检查奇异物质消耗，按重用次数和升级等级自动安排策略，避免浪费。

## 贡献
欢迎提交 Issue 或 Pull Request，分享你的优化思路、修复方案或新策略。

## 许可
项目定位为个人学习资料，欢迎在自担风险的前提下自由使用或修改脚本。
