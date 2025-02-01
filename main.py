import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLineEdit, QFileDialog, QScrollArea, QScrollBar
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Reader/Annotator")
        self.setGeometry(100, 100, 800, 600)

        # Layout for the window
        self.layout = QVBoxLayout()

        # Page counter and input at the top
        self.page_info_layout_top = QHBoxLayout()
        self.page_label_top = QLabel(self)
        self.page_info_layout_top.addWidget(self.page_label_top, alignment=Qt.AlignmentFlag.AlignLeft)

        self.page_input_top = QLineEdit(self)
        self.page_input_top.setFixedWidth(50)
        self.page_input_top.setValidator(None)  # Allow any integer input
        self.page_input_top.returnPressed.connect(self.jump_to_page)
        self.page_info_layout_top.addWidget(self.page_input_top, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout.addLayout(self.page_info_layout_top)

        # QScrollArea to display the PDF pages as images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.label = QLabel()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setStyleSheet("border: 1px solid #444; background-color: #222;")
        self.layout.addWidget(self.scroll_area)

        # Navigation buttons (Next and Previous)
        self.nav_layout = QHBoxLayout()

        self.previous_button = QPushButton("Previous Page", self)
        self.previous_button.setStyleSheet(self.button_style())
        self.nav_layout.addWidget(self.previous_button)
        self.previous_button.clicked.connect(self.previous_page)

        self.next_button = QPushButton("Next Page", self)
        self.next_button.setStyleSheet(self.button_style())
        self.nav_layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.next_page)

        # Add navigation buttons to the layout
        self.layout.addLayout(self.nav_layout)

        # Button to load the PDF
        self.load_button = QPushButton("Load PDF", self)
        self.load_button.setStyleSheet(self.button_style())
        self.layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_pdf)

        # A container widget to hold the layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Initialize PyMuPDF PDF document object
        self.pdf_document = None
        self.current_page = 0
        self.zoom_factor = 1.0  # Initial zoom factor

        # Hide page info initially
        self.page_label_top.hide()
        self.page_input_top.hide()

    def button_style(self):
        """Return the stylesheet for buttons"""
        return """
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """

    def load_pdf(self):
        """Open file explorer to load the PDF and render the first page"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.pdf_document = fitz.open(file_path)
            self.current_page = 0  # Reset to the first page
            self.render_page(self.current_page)
            # Show page info after loading the PDF
            self.page_label_top.show()
            self.page_input_top.show()

    def render_page(self, page_number):
        """Render a specific page as an image and display it in the QLabel"""
        if not self.pdf_document:
            return

        # Ensure page number is within bounds
        if page_number < 0 or page_number >= self.pdf_document.page_count:
            return

        page = self.pdf_document.load_page(page_number)

        # Apply zoom factor directly to the PDF page rendering
        zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=zoom_matrix)

        # Convert the pixmap to a QImage and then to a QPixmap
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        # Set the scaled pixmap in the label
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Update page information
        self.page_label_top.setText(f"Page {self.current_page + 1} of {self.pdf_document.page_count}")
        self.page_input_top.setText(str(self.current_page + 1))  # Update the input box with the current page

    def next_page(self):
        """Load the next page"""
        if self.pdf_document and self.current_page < self.pdf_document.page_count - 1:
            self.current_page += 1
            self.render_page(self.current_page)

    def previous_page(self):
        """Load the previous page"""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.render_page(self.current_page)

    def jump_to_page(self):
        """Jump to the specified page"""
        if self.pdf_document:
            try:
                page_num = int(self.page_input_top.text()) - 1  # Convert to 0-based index
                if 0 <= page_num < self.pdf_document.page_count:
                    self.current_page = page_num
                    self.render_page(self.current_page)
            except ValueError:
                pass  # Invalid input, do nothing

    def zoom_in(self):
        """Zoom in the document"""
        self.zoom_factor *= 1.2  # Increase zoom factor by 20%
        self.render_page(self.current_page)

    def zoom_out(self):
        """Zoom out the document"""
        self.zoom_factor /= 1.2  # Decrease zoom factor by 20%
        self.render_page(self.current_page)

    def keyPressEvent(self, event):
        """Override key press events for zooming"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Equal:  # Detect Ctrl + key press
                self.zoom_in()
            elif event.key() == Qt.Key.Key_Minus:  # Detect Ctrl - key press
                self.zoom_out()
        super().keyPressEvent(event)  # Call the parent class's keyPressEvent


# Main function to run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFReader()
    window.show()
    sys.exit(app.exec())
