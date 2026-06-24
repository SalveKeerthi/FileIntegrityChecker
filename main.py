import sys
import hashlib
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QLineEdit, QSplitter,
    QListWidget, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
import database

class FileIntegrityDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_file_name = None
        self.selected_file_path = None
        self.selected_file_hash = None
        
        self.initUI()
        self.load_registered_files()
        
    def initUI(self):
        self.setWindowTitle("File Integrity Checker - Security Dashboard")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # --- Header ---
        header_layout = QHBoxLayout()
        title_label = QLabel("File Integrity Security Dashboard")
        title_label.setObjectName("TitleLabel")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # --- Splitter ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # ==========================================
        # LEFT PANEL: Registered Files
        # ==========================================
        left_panel = QFrame()
        left_panel.setObjectName("PanelFrame")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        
        left_title = QLabel("Registered Files")
        left_title.setObjectName("SectionTitle")
        left_layout.addWidget(left_title)
        
        # Search Box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search files...")
        self.search_box.setObjectName("SearchBox")
        self.search_box.textChanged.connect(self.load_registered_files)
        left_layout.addWidget(self.search_box)
        
        # File List
        self.file_list = QListWidget()
        self.file_list.setObjectName("FileList")
        self.file_list.itemSelectionChanged.connect(self.on_file_selected)
        left_layout.addWidget(self.file_list)
        
        # Register Button
        self.btn_register = QPushButton("Register New File")
        self.btn_register.setObjectName("ActionBtn")
        self.btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_register.clicked.connect(self.register_new_file)
        left_layout.addWidget(self.btn_register)
        
        splitter.addWidget(left_panel)
        
        # ==========================================
        # RIGHT PANEL: Tabs
        # ==========================================
        right_panel = QTabWidget()
        right_panel.setObjectName("RightTabs")
        
        # TAB 1: File Verification
        self.tab_verify = QWidget()
        verify_layout = QVBoxLayout(self.tab_verify)
        verify_layout.setSpacing(15)
        verify_layout.setContentsMargins(15, 15, 15, 15)
        
        # Selected File Details
        details_frame = QFrame()
        details_frame.setObjectName("DetailsFrame")
        details_layout = QVBoxLayout(details_frame)
        
        self.lbl_selected_file = QLabel("No file selected")
        self.lbl_selected_file.setObjectName("SectionTitle")
        details_layout.addWidget(self.lbl_selected_file)
        
        self.lbl_selected_path = QLabel("Select a file from the list to view details.")
        self.lbl_selected_path.setObjectName("FileLabel")
        self.lbl_selected_path.setWordWrap(True)
        details_layout.addWidget(self.lbl_selected_path)
        
        self.le_original_hash = QLineEdit("N/A")
        self.le_original_hash.setObjectName("HashDisplay")
        self.le_original_hash.setReadOnly(True)
        details_layout.addWidget(self.le_original_hash)
        
        verify_layout.addWidget(details_frame)
        
        # Verification Actions
        self.btn_verify = QPushButton("Verify Selected File")
        self.btn_verify.setObjectName("VerifyBtn")
        self.btn_verify.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_verify.setEnabled(False)
        self.btn_verify.clicked.connect(self.verify_selected_file)
        verify_layout.addWidget(self.btn_verify)
        
        # Status Label
        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("StatusLabel")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setMinimumHeight(50)
        self.lbl_status.hide()
        verify_layout.addWidget(self.lbl_status)
        
        # History specific to file
        history_lbl = QLabel("Recent Verification History for this File")
        history_lbl.setObjectName("SectionTitle")
        verify_layout.addWidget(history_lbl)
        
        self.file_history_table = QTableWidget(0, 3)
        self.file_history_table.setHorizontalHeaderLabels(["Time", "File", "Result"])
        self.file_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.file_history_table.verticalHeader().setVisible(False)
        self.file_history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.file_history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        verify_layout.addWidget(self.file_history_table)
        
        right_panel.addTab(self.tab_verify, "File Verification")
        
        # TAB 2: Global Audit Log
        self.tab_audit = QWidget()
        audit_layout = QVBoxLayout(self.tab_audit)
        
        audit_lbl = QLabel("Global Integrity Audit Log")
        audit_lbl.setObjectName("SectionTitle")
        audit_layout.addWidget(audit_lbl)
        
        self.global_history_table = QTableWidget(0, 3)
        self.global_history_table.setHorizontalHeaderLabels(["Time", "File", "Result"])
        self.global_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.global_history_table.verticalHeader().setVisible(False)
        self.global_history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.global_history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        audit_layout.addWidget(self.global_history_table)
        
        btn_refresh_audit = QPushButton("Refresh Audit Log")
        btn_refresh_audit.clicked.connect(self.load_global_history)
        audit_layout.addWidget(btn_refresh_audit)
        
        right_panel.addTab(self.tab_audit, "Global Audit Log")
        
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])

        self.apply_styles()
        self.load_global_history()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f3f4f6;
            }
            QFrame#PanelFrame, QFrame#DetailsFrame {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
                padding: 10px;
            }
            QLabel {
                color: #111827; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#TitleLabel {
                color: #1f2937;
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
            QLineEdit#HashDisplay, QLineEdit#SearchBox {
                font-family: 'Consolas', 'Courier New', monospace;
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px;
                color: #111827;
                font-size: 13px;
            }
            QLineEdit#SearchBox {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#StatusLabel {
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton {
                background-color: #f3f4f6;
                color: #1f2937;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton#ActionBtn {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
            }
            QPushButton#ActionBtn:hover {
                background-color: #1d4ed8;
            }
            QPushButton#VerifyBtn {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton#VerifyBtn:hover {
                background-color: #059669;
            }
            QPushButton#VerifyBtn:disabled {
                background-color: #a7f3d0;
            }
            QListWidget {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f3f4f6;
                color: #111827;
            }
            QListWidget::item:selected {
                background-color: #eff6ff;
                color: #1d4ed8;
                font-weight: bold;
            }
            QTableWidget {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background-color: #ffffff;
                color: #111827;
                gridline-color: #e5e7eb;
            }
            QTableWidget::item {
                color: #111827;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                color: #374151;
                padding: 6px;
                border: 1px solid #e5e7eb;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                background-color: #ffffff;
                border-radius: 8px;
                border-top-left-radius: 0px;
            }
            QTabBar::tab {
                background-color: #f3f4f6;
                color: #6b7280;
                border: 1px solid #e5e7eb;
                border-bottom: none;
                padding: 8px 16px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #111827;
            }
        """)

    def calculate_sha256(self, filepath):
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def load_registered_files(self):
        query = self.search_box.text()
        files = database.get_registered_files(query)
        self.file_list.clear()
        for f in files:
            self.file_list.addItem(f['file_name'])

    def register_new_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Register")
        if file_path:
            file_name = os.path.basename(file_path)
            # Calculate Hash
            file_hash = self.calculate_sha256(file_path)
            if file_hash:
                database.register_file(file_name, file_path, file_hash)
                self.load_registered_files()
                # Automatically select the newly registered file
                items = self.file_list.findItems(file_name, Qt.MatchFlag.MatchExactly)
                if items:
                    self.file_list.setCurrentItem(items[0])
            else:
                QMessageBox.critical(self, "Error", "Failed to read the file for hashing.")

    def on_file_selected(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.btn_verify.setEnabled(False)
            return
            
        file_name = selected_items[0].text()
        file_data = database.get_file_by_name(file_name)
        
        if file_data:
            self.selected_file_name = file_name
            self.selected_file_path = file_data['file_path']
            self.selected_file_hash = file_data['sha256_hash']
            
            self.lbl_selected_file.setText(file_name)
            self.lbl_selected_path.setText(f"Path: {self.selected_file_path}\nRegistered: {file_data['registration_date']}")
            self.le_original_hash.setText(self.selected_file_hash)
            
            self.btn_verify.setEnabled(True)
            self.lbl_status.hide()
            
            self.load_file_history(file_name)

    def load_file_history(self, file_name):
        history = database.get_verification_history(file_name)
        self.populate_table(self.file_history_table, history)

    def load_global_history(self):
        history = database.get_verification_history()
        self.populate_table(self.global_history_table, history)

    def populate_table(self, table, history_data):
        table.setRowCount(len(history_data))
        for row_idx, record in enumerate(history_data):
            time_item = QTableWidgetItem(record['verification_date'])
            # Explicitly set color for general text to override any dark mode defaults
            time_item.setForeground(QColor("#111827")) 
            
            file_item = QTableWidgetItem(record['file_name'])
            file_item.setForeground(QColor("#111827"))
            
            result_item = QTableWidgetItem(record['result'])
            
            if record['result'] == "PASS":
                result_item.setForeground(QColor("#065f46"))
                result_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            else:
                result_item.setForeground(QColor("#991b1b"))
                result_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                
            table.setItem(row_idx, 0, time_item)
            table.setItem(row_idx, 1, file_item)
            table.setItem(row_idx, 2, result_item)

    def verify_selected_file(self):
        if not self.selected_file_path:
            return
            
        if not os.path.exists(self.selected_file_path):
            QMessageBox.critical(self, "File Not Found", f"The file could not be found at:\n{self.selected_file_path}\n\nIt may have been moved or deleted.")
            database.log_verification(self.selected_file_name, "ERROR: NOT FOUND")
            self.update_history_views()
            return
            
        current_hash = self.calculate_sha256(self.selected_file_path)
        
        if current_hash:
            self.lbl_status.show()
            if current_hash == self.selected_file_hash:
                result = "PASS"
                self.lbl_status.setText("✓ File Integrity Verified\nNo modifications detected")
                self.lbl_status.setStyleSheet("color: #065f46; background-color: #d1fae5; border: 1px solid #34d399;")
            else:
                result = "FAIL"
                self.lbl_status.setText(f"⚠ File Modified\nIntegrity Check Failed\n\nCurrent Hash: {current_hash}")
                self.lbl_status.setStyleSheet("color: #991b1b; background-color: #fee2e2; border: 1px solid #f87171;")
                
            database.log_verification(self.selected_file_name, result)
            self.update_history_views()
        else:
            QMessageBox.critical(self, "Error", "Failed to read the file for hashing.")

    def update_history_views(self):
        self.load_file_history(self.selected_file_name)
        self.load_global_history()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = FileIntegrityDashboard()
    window.show()
    sys.exit(app.exec())
