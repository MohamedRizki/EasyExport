# EasyExport Algorithm

## Description :
`EasyExportAlgorithm` is a Python script developed by **Mohamed RIZKI**, a second-year engineering student.  
It’s a handy tool that allows you to **automatically export map pages as PDF files** using predefined layouts in a **QGIS** project.

With it, you can:
- Select a layout from your QGIS project
- Exclude a layer (e.g., a base map like OSM)
- Set **horizontal and vertical overlaps**
- Choose the export path for the generated PDFs

## Requirements

- **QGIS** (version 3.10 or higher)
- `EasyExportAlgorithm.py` script

## Installation :

1. Download the `EasyExportAlgorithm.py` script and save it wherever you like
2. Open **QGIS**
3. Load the script in QGIS’s Python editor and run it

## How to Use :

Once the script is running, it will ask you for a few simple parameters:

### Algorithm Parameters :

| Parameter | Description | Type | Required |
|----------|-------------|------|----------|
| **Layout** | Choose a layout from your QGIS project | Dropdown list | Yes |
| **Layer to exclude** | Exclude a layer from extent calculation (e.g., base maps) | Layer selection | Optional |
| **Horizontal overlap (%)** | Overlap between exported pages (horizontal) | Numeric | Optional (default: 0) |
| **Vertical overlap (%)** | Overlap between exported pages (vertical) | Numeric | Optional (default: 0) |
| **Export path** | Where to save the exported PDF files | File destination (PDF) | Yes |

## Output Example :

When you run the algorithm, it:

1. Calculates the dimensions of the selected layout
2. Computes the visible extent of layers (excluding the chosen layer)
3. Splits the extent into multiple rectangles based on layout size and overlaps
4. Exports each rectangle as a **separate PDF file** using the selected layout

Example output filenames:
```bash
export_path_1.pdf  
export_path_2.pdf  
export_path_3.pdf  
```

Contact : Mohamedrizki07@gmail.com
