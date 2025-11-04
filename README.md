# The Farmer Was Replaced Automation Toolkit

中文: [README.zh.md](README.zh.md)

## Overview
This repository contains automation scripts for the Steam puzzle game [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/_/). The code is written in Python syntax so that it can be edited comfortably, but it targets the game's in-engine language. The bundled `__builtins__.py` file provides type stubs for the game API to make authoring and linting easier in standard editors.

## Repository Layout
```
.
├── __builtins__.py        # Type hints for the in-game API
├── config.example.py      # Sample configuration for crop priority and thresholds
├── crop_cactus.py         # Sorted cactus harvesting routine
├── crop_carrots.py        # Carrot farming helper
├── crop_dinosaur.py       # Dinosaur minigame automation
├── crop_grass.py          # Grass harvesting loop
├── crop_maze.py           # Hedge maze solver and gold farming
├── crop_mix.py            # Companion planting automation
├── crop_pumpkins.py       # Giant pumpkin management
├── crop_sunflowers.py     # Power-focused sunflower harvesting
├── crop_trees.py          # Checkerboard tree farming
├── crop_weird.py          # Weird substance collection strategies
├── smart_priority.py      # Priority-based crop dispatcher
├── utils.py               # Shared navigation and farming helpers
└── README.zh.md           # Chinese documentation
```

## Smart Priority Controller (`smart_priority.py`)
The main entry point is an infinite control loop that evaluates resources and plants the most appropriate crop.
- Reads `PRIORITY` and `THRESHOLDS` from `config.py` (copy `config.example.py` to create it).
- Tracks power, carrots, wood, pumpkins, hay, fertilizer, water, cactus, weird substance, bones, and gold before each decision.
- Scores each configured crop based on current shortages and emergency thresholds (for example, sunflowers take precedence when power is low).
- Validates that enough inputs are available (checks costs via `get_cost` and unlock status for mazes).
- Falls back to harvesting grass when nothing else is affordable.

## Utility Helpers (`utils.py`)
A small helper module to streamline movement and field maintenance.
- `move_to(x, y)` walks the drone to a coordinate, choosing the shorter wrap-around path on the toroidal map.
- `tilling()` prepares soil when needed, keeping ground states consistent between modules.
- `water()` and `water_full()` help maintain optimal moisture levels.

## Crop Modules
Each `crop_*.py` file focuses on a single crop or mechanic so it can be called independently or through the smart controller.
- `crop_grass.farm_grass()` clears the board, restores grassland, and harvests hay quickly.
- `crop_trees.farm_trees()` plants trees in a checkerboard pattern to avoid the 16x adjacency growth penalty and waters them while waiting.
- `crop_carrots.farm_carrots()` tills soil, replants carrots, and waters immediately for the five-times growth boost.
- `crop_pumpkins.farm_pumpkins()` keeps the field full of pumpkins, tracks withered tiles, and replants only the affected positions until a giant pumpkin is ready.
- `crop_sunflowers.farm_sunflowers()` records petal counts at planting time, maintains high water levels, and harvests sunflowers in descending petal order to retain the power multiplier.
- `crop_cactus.farm_cactus()` sorts cactus sizes row by row and column by column using bubble swaps, then harvests from the origin to secure the full squared reward.
- `crop_mix.farm_mixed(main_crop)` leverages companion planting: it records companion requirements, plants supporting crops where demand is highest, and cleans up after harvest.

## Special Modules
- `crop_weird.py` provides three entry points: `farm_weird_substance()` for fast grass-based infection, `farm_weird_substance_advanced()` for fertilizer-boosted carrots, and `farm_weird_substance_chain()` that uses weird substance to propagate infections across the farm.
- `crop_dinosaur.py` automates the dinosaur hat minigame. It tracks the tail path to avoid collisions, navigates via Manhattan distance with fallback detours, and includes `farm_dinosaur_optimal()` and `farm_dinosaur_efficient()` variants to match your cactus (apple) budget.
- `crop_maze.py` grows hedge mazes, solves them using right-hand or left-hand rules (with a `measure`-guided fallback), and supports reuse counts or size adjustments through `farm_maze_optimal()` and `farm_maze_smart()`.

## Getting Started
1. Copy the sample configuration: `Copy-Item config.example.py config.py` in PowerShell (`cp config.example.py config.py` on macOS/Linux).
2. Edit `config.py` to set up your preferred `PRIORITY` order and resource `THRESHOLDS`. Each entry is a dictionary describing the crop name and optional parameters such as maze size or dinosaur mode.
3. Load the script in-game and run `smart_priority.py` to let the controller loop manage planting decisions. You can also import an individual `crop_*` module to farm a specific resource on demand.

Example configuration snippet:
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

## Strategy Highlights
- Giant Pumpkins: the withered-tile watch list avoids scanning the entire board every cycle, so the script only replants where needed.
- Sunflowers: storing initial petal counts enables harvesting only the maximum petals in each pass, preserving the five-times power bonus.
- Sorted Cactus: row-first and column-second bubble passes ensure the final layout stays ordered without unnecessary travel.
- Companion Planting: demand aggregation picks the companion crop that benefits the most main plots before the cleanup phase.
- Dinosaurs: tail tracking and Manhattan navigation keep the drone moving safely until the farm fills or apples run out.
- Mazes: resource checks and reuse counters prevent wasting weird substance and adapt to current upgrade levels.

## Contributing
Suggestions and improvements are welcome. Open an issue or submit a pull request with any refinements, bug fixes, or new farming strategies.

## License
This project is maintained as a personal learning aid. Feel free to reuse or modify the scripts at your own risk.
