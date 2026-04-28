import os
import time
from multiprocessing import Pool
from qgis.core import QgsApplication, QgsVectorLayer, QgsGeometry

# Setup QGIS Path (Standard for Python 3.12 standalone scripts)
QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

def spatial_worker(task):
    """
    Independent worker process for geometry validation.
    Runs in parallel to bypass Python's GIL and maximize CPU usage.
    """
    group_id, layer_name, ota_list, base_path = task
    errors = []
    
    for ota in ota_list:
        shp_path = os.path.join(base_path, ota, layer_name, f"{layer_name}.shp")
        
        if not os.path.exists(shp_path):
            continue
            
        # Load layer in off-screen mode
        layer = QgsVectorLayer(shp_path, layer_name, "ogr")
        if not layer.isValid():
            continue

        # Iterate through features and validate geometry engine
        for feature in layer.getFeatures():
            geom = feature.geometry()
            if not geom.isGeosvalid():
                # Capture critical metadata for the error report
                errors.append({
                    'OTA': ota,
                    'FID': feature.id(),
                    'ERROR': geom.validateGeometry(),
                    'GROUP': group_id
                })
    return errors

if __name__ == '__main__':
    # Configuration for a 6-core High-End Workstation
    NUM_CORES = 6
    BASE_PATH = "C:/GIS_DATA/SHAPE"
    
    # Task distribution logic (example slice)
    tasks = [("GROUP_A", "PST", ["41001", "41002"], BASE_PATH),
             ("GROUP_B", "PST", ["41003", "41004"], BASE_PATH)]

    print(f"🚀 Initializing Parallel Audit on {NUM_CORES} cores...")
    start_time = time.time()

    with Pool(processes=NUM_CORES) as pool:
        # imap_unordered for maximum memory efficiency
        results = pool.imap_unordered(spatial_worker, tasks)
        
        final_report = []
        for i, res in enumerate(results):
            final_report.extend(res)
            print(f"✅ Processed task {i+1}/{len(tasks)}", end="\r")

    duration = time.time() - start_time
    print(f"\n\n✨ Audit Complete. Total Errors: {len(final_report)}")
    print(f"⏱ Execution Time: {duration:.2f} seconds")

# Clean up QGIS resources
qgs.exitQgis()
