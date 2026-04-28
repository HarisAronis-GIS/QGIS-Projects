import os
from qgis.core import QgsProject, QgsRuleBasedLabeling, QgsPalLayerSettings, QgsProperty

def refactor_project_labels(project_path, rules_config):
    """
    Automates font style overrides and spatial filters for labeling.
    Solves persistence issues where QGIS fails to retain Bold/Italic styles 
    in complex rule-based setups.
    """
    project = QgsProject.instance()
    project.read(project_path)

    for l_name in ['POI_ANNOT_1', 'POI_ANNOT_5']:
        layers = project.mapLayersByName(l_name)
        for layer in layers:
            labeling = layer.labeling()
            if not isinstance(labeling, QgsRuleBasedLabeling): continue
            
            root_rule = labeling.rootRule()
            for rule in root_rule.children():
                current_filter = rule.filterExpression()
                
                for pname_val, config in rules_config.items():
                    if f"\"PNAME\" = {pname_val}" in current_filter:
                        # 1. Inject Spatial Predicate (ensure label is within boundary)
                        new_filter = f"\"PNAME\" = {pname_val}"
                        if config["within"]:
                            new_filter += " AND overlay_within('ASTOTA')"
                        rule.setFilterExpression(new_filter)
                        
                        # 2. Force Font Style via Data Defined Overrides
                        settings = rule.settings()
                        style_val = config["style"]
                        settings.dataDefinedProperties().setProperty(
                            QgsPalLayerSettings.FontStyle, 
                            QgsProperty.fromExpression(f"'{style_val}'")
                        )
                        
                        # 3. Optimization: Force visibility even on overlaps
                        settings.showAllLabels = True 
                        rule.setSettings(settings)
            
            layer.setLabeling(labeling)
    
    project.write()
    project.clear()
