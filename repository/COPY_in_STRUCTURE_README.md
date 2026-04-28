# COPY_in_STRUCTURE.ps1 | Technical Documentation

## 🎯 Objective
High-speed, multi-threaded distribution of GIS deliverables while maintaining strict hierarchical folder structures.

## 🛠 Tech Stack
- **PowerShell**
- **RoboCopy**: Used as the underlying engine for robust, fast file copying.

## ⚙️ Logic & Workflow
1. **Orchestration:** Uses PowerShell to build a dynamic task list based on OTA codes (with wildcard support).
2. **Parallelism:** Implements a `ThrottleLimit` of 6 parallel processes, each running 8 RoboCopy threads (48 threads total).
3. **Safety Check:** Performs a size estimation and requests user confirmation before saturating network bandwidth.
4. **Integrity:** Mirrors the source directory structure (`SHAPE\OTA\LAYER`) precisely to match National Registry requirements.

## 🚀 Impact
Optimized office-to-server data migration, reducing transfer times for large datasets by over 70%.
