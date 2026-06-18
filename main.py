import sys
import hashlib
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class FileIntegrityChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_file_path = None
        self.original_hash = None
        self.verify_file_path = None
        self.verify_hash = None
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("File Integrity Checker")
        self.resize(700, 750) # Increased default size
        self.setMinimumSize(500, 400)
        
        # --- Scroll Area Setup ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("ScrollArea")
        self.setCentralWidget(scroll_area)
        
        # Main widget and layout
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # --- Title ---
        title_label = QLabel("File Integrity Checker")
        title_label.setObjectName("TitleLabel")
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Generate and verify SHA-256 hashes for your files.")
        subtitle_label.setObjectName("SubtitleLabel")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(10)
        
        # --- Section 1: File Registration ---
        reg_frame = QFrame()
        reg_frame.setObjectName("CardFrame")
        reg_layout = QVBoxLayout(reg_frame)
        reg_layout.setSpacing(10)
        
        reg_title = QLabel("1. Baseline File")
        reg_title.setObjectName("SectionTitle")
        reg_layout.addWidget(reg_title)
        
        self.reg_file_label = QLabel("No file selected.")
        self.reg_file_label.setObjectName("FileLabel")
        self.reg_file_label.setWordWrap(True)
        reg_layout.addWidget(self.reg_file_label)
        
        self.btn_select_original = QPushButton("Select Original File")
        self.btn_select_original.setMinimumHeight(40)
        self.btn_select_original.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select_original.clicked.connect(self.select_original_file)
        reg_layout.addWidget(self.btn_select_original)
        
        main_layout.addWidget(reg_frame)
        
        # --- Section 2: File Verification ---
        ver_frame = QFrame()
        ver_frame.setObjectName("CardFrame")
        ver_layout = QVBoxLayout(ver_frame)
        ver_layout.setSpacing(10)
        
        ver_title = QLabel("2. Verification File")
        ver_title.setObjectName("SectionTitle")
        ver_layout.addWidget(ver_title)
        
        self.ver_file_label = QLabel("No file selected.")
        self.ver_file_label.setObjectName("FileLabel")
        self.ver_file_label.setWordWrap(True)
        ver_layout.addWidget(self.ver_file_label)
        
        self.btn_select_verify = QPushButton("Select File to Verify")
        self.btn_select_verify.setMinimumHeight(40)
        self.btn_select_verify.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select_verify.clicked.connect(self.select_verify_file)
        self.btn_select_verify.setEnabled(False) 
        ver_layout.addWidget(self.btn_select_verify)
        
        main_layout.addWidget(ver_frame)
        
        # --- Section 3 & 4: Hash Display and Integrity Status ---
        result_frame = QFrame()
        result_frame.setObjectName("CardFrame")
        result_layout = QVBoxLayout(result_frame)
        result_layout.setSpacing(15)
        
        res_title = QLabel("Comparison Results")
        res_title.setObjectName("SectionTitle")
        result_layout.addWidget(res_title)
        
        # Original Hash
        self.lbl_original_hash_title = QLabel("Original Hash:")
        self.lbl_original_hash_title.setObjectName("HashTitle")
        
        self.le_original_hash = QLineEdit("N/A")
        self.le_original_hash.setObjectName("HashDisplay")
        self.le_original_hash.setReadOnly(True)
        self.le_original_hash.setMinimumHeight(35)
        
        result_layout.addWidget(self.lbl_original_hash_title)
        result_layout.addWidget(self.le_original_hash)
        
        # Verification Hash
        self.lbl_verify_hash_title = QLabel("Verification Hash:")
        self.lbl_verify_hash_title.setObjectName("HashTitle")
        
        self.le_verify_hash = QLineEdit("N/A")
        self.le_verify_hash.setObjectName("HashDisplay")
        self.le_verify_hash.setReadOnly(True)
        self.le_verify_hash.setMinimumHeight(35)
        
        result_layout.addWidget(self.lbl_verify_hash_title)
        result_layout.addWidget(self.le_verify_hash)
        
        # Status Display
        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("StatusLabel")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setMinimumHeight(60) 
        self.lbl_status.hide() 
        result_layout.addWidget(self.lbl_status)
        
        main_layout.addWidget(result_frame)
        
        # Add a stretch to push everything up so it doesn't spread out too much if window is tall
        main_layout.addStretch()

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QScrollArea#ScrollArea, QScrollArea#ScrollArea > QWidget > QWidget {
                background-color: #f3f4f6;
            }
            QFrame#CardFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                padding: 10px;
            }
            QLabel {
                border: none;
                background: transparent;
                color: #111827; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#TitleLabel {
                color: #1f2937;
            }
            QLabel#SubtitleLabel {
                color: #6b7280;
                font-size: 13px;
            }
            QLabel#SectionTitle {
                color: #111827;
                font-size: 15px;
                font-weight: bold;
            }
            QLabel#FileLabel {
                color: #4b5563;
                font-size: 13px;
                font-style: italic;
            }
            QLabel#HashTitle {
                color: #374151;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit#HashDisplay {
                font-family: 'Consolas', 'Courier New', monospace;
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 5px 10px;
                color: #111827;
                font-size: 13px;
            }
            QLabel#StatusLabel {
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QPushButton:disabled {
                background-color: #93c5fd;
                color: #eff6ff;
            }
        """)

    def calculate_sha256(self, filepath):
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return None

    def select_original_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Baseline File")
        if file_path:
            self.original_file_path = file_path
            filename = os.path.basename(file_path)
            self.reg_file_label.setText(f"Selected: {filename}")
            
            # Calculate Hash
            self.original_hash = self.calculate_sha256(file_path)
            if self.original_hash:
                self.le_original_hash.setText(self.original_hash)
                self.btn_select_verify.setEnabled(True)
                
                # Reset verification side
                self.reset_verification()
            else:
                self.le_original_hash.setText("Error reading file.")

    def select_verify_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Verify")
        if file_path:
            self.verify_file_path = file_path
            filename = os.path.basename(file_path)
            self.ver_file_label.setText(f"Selected: {filename}")
            
            # Calculate Hash
            self.verify_hash = self.calculate_sha256(file_path)
            if self.verify_hash:
                self.le_verify_hash.setText(self.verify_hash)
                self.compare_hashes()
            else:
                self.le_verify_hash.setText("Error reading file.")
                
    def reset_verification(self):
        self.verify_file_path = None
        self.verify_hash = None
        self.ver_file_label.setText("No file selected.")
        self.le_verify_hash.setText("N/A")
        self.lbl_status.hide()
        self.lbl_status.setText("")
        self.lbl_status.setStyleSheet("")

    def compare_hashes(self):
        if self.original_hash and self.verify_hash:
            self.lbl_status.show()
            if self.original_hash == self.verify_hash:
                self.lbl_status.setText("✓ File Integrity Verified\nNo modifications detected")
                self.lbl_status.setStyleSheet("color: #065f46; background-color: #d1fae5; border: 1px solid #34d399;")
            else:
                self.lbl_status.setText("⚠ File Modified\nIntegrity Check Failed")
                self.lbl_status.setStyleSheet("color: #991b1b; background-color: #fee2e2; border: 1px solid #f87171;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = FileIntegrityChecker()
    window.show()
    sys.exit(app.exec())
