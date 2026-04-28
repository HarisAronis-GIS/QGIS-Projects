# BatchExportPoints.lsp | Technical Documentation

## 🎯 Objective
Automated extraction of survey (tachymetric) points from multiple DWG files into a standardized GIS-ready CSV format.

## 🛠 Tech Stack
- **AutoLISP / Visual LISP**
- **ObjectDBX**: To process closed DWG files without the overhead of the graphical interface.
- **Python**: For secondary data splitting and integrity reporting.

## ⚙️ Logic & Workflow
1. **Extraction (LISP):** Scans a directory for DWGs. Using ObjectDBX, it identifies point entities on specific layers or block insertions by name.
2. **Deduplication:** Filters unique coordinates and exports them to `all_points.csv`.
3. **Refining (Python):** `SplitPoints.py` parses the CSV and categorizes data into schema-compliant Shapefile structures.
4. **Validation:** `Check_n_Report.py` generates a final report on data consistency before GIS ingestion.

## 🚀 Impact
Streamlined the CAD-to-GIS pipeline for massive topographic datasets, ensuring zero coordinate loss during migration.
