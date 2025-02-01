# PDF Reader/Annotator - Version 1.0

A simple and lightweight PDF reader/annotator built using PyQt6 and PyMuPDF (fitz) for viewing and navigating PDF documents. The application supports loading PDFs, page navigation, zooming, and jumping to specific pages.

## Features

- **Load PDF**: Open PDF files from your computer.
- **Page Navigation**: Move between pages with Previous and Next buttons.
- **Jump to Page**: Quickly navigate to any page by entering the page number.
- **Zoom**: Zoom in and out of the PDF pages with mouse controls or keyboard shortcuts (`Ctrl +` to zoom in, `Ctrl -` to zoom out).
- **Responsive Interface**: The document viewer is integrated with a scroll area for smooth navigation of pages.
  
## Requirements

To run this application, you will need the following Python libraries:

- **PyQt6**: Python bindings for Qt6, used for the graphical user interface (GUI).
- **PyMuPDF (fitz)**: Library for handling and rendering PDFs.

You can install the required libraries using `pip`:

```bash
pip install PyQt6 PyMuPDF
