# PymuPDF_corrections.py | Technical Documentation

## 🎯 Objective
Post-processing of exported PDF map layouts to apply branding updates and text corrections without re-rendering from the GIS environment.

## 🛠 Tech Stack
- **Python 3.12**
- **PyMuPDF (fitz)**: For high-speed PDF stream manipulation.
- **OS**: For batch directory traversal.

## ⚙️ Logic & Workflow
1. **Targeting:** Iterates through hundreds of Municipality (OTA) folders to find PDF layouts.
2. **Cleaning:** Uses coordinate-based "white-out" rectangles to redact old logos or misspelled text.
3. **Patching:** Directly injects binary image streams (PNG logos) and new text blocks into the PDF object stream.
4. **Validation:** Implements sub-point offsets to mask vector line artifacts often left by PDF rendering engines.

## 🚀 Impact
Saved approximately 3 working days of re-plotting for a project involving over 1,000 A0-sized maps.
