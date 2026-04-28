# SHP_VERIFIER.py | Technical Documentation

## 🎯 Objective
This script is a comprehensive validation engine designed to audit the **SHAPE** delivery folder for large-scale Cadastre GIS projects. It ensures strict adherence to technical specifications by verifying folder structures, validating schema integrity, and performing attribute normalization.

## 🛠 Core Functionalities
- **Structure Audit:** Verifies the hierarchical integrity of the delivery folder, identifying and removing redundant files or unauthorized subdirectories.
- **Schema Validation & Repair:** Automates the verification of Shapefile headers, ensuring field names, data types, and lengths align with project standards.
- **Attribute Normalization:** Performs automated correction of field values based on pre-defined business rules (e.g., handling missing or incorrect address strings).
- **Manual Error Reporting:** Identifies and logs loading errors or complex inconsistencies that require manual intervention by the GIS team.
- **Placeholder Generation:** Automatically generates empty, schema-compliant Shapefiles for mandatory subfolders where data is missing.

## ⚙️ Initial Configuration (Setup)
- `base_path`: Target directory (e.g., Desktop/SHAPE) containing the source spatial data.
- `master_template_path`: Directory containing "gold-standard" empty Shapefiles (pre-verified for type/length compliance) used as templates for repairs and generation.
- `log_file_path`: Output destination and filename for the validation report.
- `ANONYMOS_SET`: List of invalid or null `PST.ADDRESS` entries to be normalized as "ΑΝΩΝΥΜΟΣ" (Anonymous).
- `TYFLO_SET`: List of erroneous `PST.ADDRESS` entries to be normalized as "ΤΥΦΛΟ" (Blind/Dead-end).
- `groups_dict`: Mapping of Municipality (OTA) codes to specific Basemaps and Subcontractor Offices to streamline the manual correction workflow.

## 📤 Output & Results
- **Verified Delivery Package:** A sanitized and compliant SHAPE folder ready for submission.
- **Validation Log:** A detailed report highlighting all automated corrections and a prioritized list of issues requiring manual resolution.

## ⚙️ Methodology & Workflow

### 1. Initialization
- Configures environment encoding (Windows-1253 for Greek characters).
- Initializes dual-logging system (Concurrent output to Console and Log File).
- Performs dependency checks for `base_path` and `master_templates` existence.

### 2. Schema Template Loading
- Parses "ideal" Shapefiles from the `master_template_path`.
- Maps the expected schema (field names, types, lengths) into a memory-resident dictionary (`masters`) for high-speed comparison.

### 3. Execution Scope
- Supports selective processing: Users can target specific Municipalities (OTA) using prefix filters (e.g., "41" for Viotia) or perform a full-scale scan of the entire `base_path`.

### 4. Scanning Phase
- **Data Integrity Check:** Evaluates attribute values against complex business logic. Issues are flagged as:
    - `[MANUAL]`: Critical inconsistencies requiring human intervention.
    - `[FIXABLE]`: Systematic errors that can be programmatically resolved.
- **Schema Validation:** Compares active Shapefile headers against the template. Identifies type mismatches, incorrect lengths, missing mandatory fields, or redundant attributes.
- **Heuristic Filtering:** Includes conditional logic to ignore minor schema discrepancies that do not trigger server-side loading errors, focusing only on mission-critical violations.

### 5. Reporting & Automated Rectification
- **Categorized Reporting:** Generates a summary log grouped by Subcontractor/Basemap (via `groups_dict`), separating fixable and manual issues.
- **The SHP_RECTIFIER Engine:** Upon user confirmation (`YES`), the script executes automated repairs:
    - **Schema Correction:** Uses a "Temporary Field" migration technique (Add TMP field -> Data Migration -> Drop Old -> Recreate Correct -> Restore Data) to safely change field types/lengths without data loss.
    - **Attribute Fixing:** Executes `CalculateField` operations with Python logic to normalize fields like `ORI_CODE`, `ADDRESS`, and `NUM`.
    - **Redundant Field Stripping:** Removes non-compliant fields.

### 6. Missing Layer Recovery
- Identifies mandatory layers missing from OTA folders.
- Provides a prompt for the user to bulk-generate schema-compliant empty Shapefiles from the master templates (selective or global generation).

### 7. Completion
- Logs total execution time.
- Triggers an audible alert (Beep) and remains active for log review before termination.
