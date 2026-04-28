;; AutoLISP snippet using ObjectDBX for high-speed data extraction
;; Processes closed DWG files to extract coordinates from Blocks and Points
(defun c:BatchExportPoints (/ dbx addr pt)
  (vl-load-com)
  (setq baseDir "D:\\PROJECT_DATA\\")
  (setq TARGET_LAYER "TOPO_SURVEY_POINTS")
  (setq TARGET_BLOCK "SURVEY_NODE")

  ;; Initialize ObjectDBX to read DWGs without opening them in the editor
  (setq dbx (vlax-create-object 
              (strcat "ObjectDBX.AxDbDocument." (substr (getvar "ACADVER") 1 2))))

  (foreach dwg (vl-directory-files baseDir "*.dwg" 1)
    (vla-open dbx (strcat baseDir dwg))
    (vlax-for block (vla-get-blocks dbx)
      (vlax-for obj block
        ;; Extract from Blocks (Insertion Points) or Point Entities (Coordinates)
        (if (or (and (= (vla-get-ObjectName obj) "AcDbBlockReference")
                     (= (strcase (vla-get-Name obj)) (strcase TARGET_BLOCK)))
                (and (= (vla-get-ObjectName obj) "AcDbPoint")
                     (= (strcase (vla-get-Layer obj)) (strcase TARGET_LAYER))))
            (setq pt (vlax-safearray->list (vlax-variant-value (vla-get-InsertionPoint obj))))
        )
        ;; Logic for uniqueness check and CSV logging follows...
      )
    )
  )
  (vlax-release-object dbx)
)
