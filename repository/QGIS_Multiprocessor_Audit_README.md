# ChkGeom.py | Technical Documentation

## 🎯 Objective
This script is a high-performance geometry validation and repair engine designed for large-scale GIS projects. It automates the detection of topological errors (e.g., self-intersections, null geometries), generates georeferenced error reports, and performs batch repairs to ensure data compliance with National Cadastre standards.

## 🛠 Core Functionalities
- **Geometry Audit:** Identifies invalid geometries across multiple datasets simultaneously.
- **Georeferenced Reporting:** Exports detailed error logs, including Feature IDs (FID), Municipality codes (OTA), and spatial location (KAEK or X/Y coordinates).
- **Automated Repair:** Provides a batch-repair workflow to rectify identified geometry violations.
- **Missing PRJ Restoration:** Automatically generates GGRS87 (.prj) files if missing, ensuring coordinate system consistency during the audit.
- **Empty Dataset Reporting:** Identifies and lists empty Shapefiles within the project structure for administrative oversight.

## ⚙️ Initial Configuration (Setup)
- `base_path`: Target directory containing the hierarchical folder structure of the project.
- `output_folder`: Destination for the consolidated error reports.
- `groups_dict`: Mapping of Municipality (OTA) codes to specific Basemaps and Subcontractor Offices to facilitate targeted data correction.
- `prj_content`: Standardized GGRS87 (EPSG:2100) spatial reference string for automated .prj file generation.

## ⚙️ Methodology & Workflow

### 1. Parallel Processing Architecture
- To optimize performance for thousands of files, the script utilizes **multi-core processing (6 parallel threads)**.
- Workload is distributed across processes to verify data existence and schema integrity simultaneously.

### 2. Geometry Validation Engine
- Leverages the `arcpy.CheckGeometry_management` command within each parallel process.
- For every detected error, the script generates a temporary enriched table (t_xxx.dbf) that captures the **KAEK** (Cadastral Code) or the **Centroid Coordinates** (X,Y) of the problematic feature.
- **Spatial Referencing:** For non-cadastral layers (e.g., FBOUND, ROADS), the script uses the `SHAPE@XY` token. For linear features, it calculates the Extent Centroid to provide a reliable zoom-to target.

### 3. Reporting & Consolidation
- Merges individual process results into a single, comprehensive DBF report: `GEOMETRY_REPORT_YYYY-MM-DD_HHMMSS`.
- Reports are enriched with metadata (Basemap ID, Subcontractor Office) for efficient task distribution.

### 4. Automated Repair Workflow
- Following the audit, the user is prompted to execute `Repair Geometry`.
- Upon confirmation, the script performs a batch repair, followed by a **re-validation pass** to ensure all issues were successfully resolved.
- A final repair log is generated for documentation and quality assurance.

## 📤 Output & Results
- **Consolidated Error Report:** A georeferenced .dbf file for easy navigation to problematic features in QGIS/ArcMap.
- **Sanitized Spatial Data:** Fixed Shapefiles with validated topology.
- **Empty File Summary:** On-screen report for quick identification of datasets without features.
