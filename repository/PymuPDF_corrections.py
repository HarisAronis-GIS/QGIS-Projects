import fitz  # PyMuPDF library

def patch_map_metadata(pdf_path, output_path, corrections):
    """
    Directly updates text objects within an exported PDF (titles, logos, labels).
    Bypasses the need to re-render complex GIS layouts.
    """
    doc = fitz.open(pdf_path)
    
    for page in doc:
        for old_text, new_text in corrections:
            # Locate the coordinates of the target text
            text_instances = page.search_for(old_text)
            
            for inst in text_instances:
                # Redact the old content (white-out)
                page.add_redact_annotation(inst, fill=(1, 1, 1))
                page.apply_redactions()
                
                # Insert the corrected text at the exact same location
                # Ensuring font-consistency and spatial alignment
                page.insert_text(inst.tl, new_text, 
                                 fontname="helv", 
                                 fontsize=11, 
                                 color=(0, 0, 0))
                                 
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

# Example Usage: Batch updating misspelled Municipality names in map titles
corrections = [("MUNICIPALITY OF AGIALEIA", "MUNICIPALITY OF AIGIALEIA")]
patch_map_metadata("Map_A0_v1.pdf", "Map_A0_final.pdf", corrections)
