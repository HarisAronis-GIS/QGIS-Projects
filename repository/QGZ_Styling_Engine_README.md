# QGZ_Styling_Engine.py | Technical Documentation

## 🎯 Objective
Massive refactoring of QGIS Project files (.qgz) to enforce cartographic styling and resolve font-persistence bugs.

## 🛠 Tech Stack
- **Python 3.12**
- **PyQGIS API**: For interacting with the QGIS labeling and styling engine.

## ⚙️ Logic & Workflow
1. **Persistence Fix:** Addresses a known QGIS issue where font styles (Bold/Italics) revert to "Regular" in complex rule-based setups. 
2. **Data-Defined Overrides:** Injects Python expressions into the `QgsPalLayerSettings` to force font styles at runtime.
3. **Spatial Predicate Injection:** Automatically updates filters with `overlay_within` logic to ensure labels remain within administrative boundaries.
4. **Batch Processing:** Reads, modifies, and re-saves hundreds of project files in a single execution.

## 🚀 Impact
Ensured 100% compliance with national cartographic specifications across thousands of map annotations.
