# File Integrity Checker 

A sleek, professional desktop application built with Python and PyQt6 designed to verify the integrity of files. It calculates the SHA-256 cryptographic hash of a baseline file and allows you to compare it against another file to detect if any unauthorized modifications, tampering, or corruptions have occurred.

## Features

- **SHA-256 Hashing**: Uses the robust SHA-256 cryptographic algorithm to ensure high-security integrity checks.
- **Clean Graphical User Interface (GUI)**: Built with PyQt6, featuring a modern, scrollable, and fully responsive layout that supports high-resolution displays and prevents UI cut-offs.
- **Copyable Hash Outputs**: Generated hashes are presented in read-only text fields, making it simple to review and copy them.
- **Memory Efficient**: Processes files in optimized 4KB chunks, allowing it to easily handle large files without exhausting system RAM.
- **Instant Visual Feedback**: Clearly displays whether the integrity of the verified file is intact (green success message) or compromised (red warning message).

## Prerequisites

Ensure you have Python installed on your system (Python 3.8 or higher is recommended). 

## Installation

1. Download the project files to your local machine.
2. Open your terminal or command prompt.
3. Navigate to the project directory:
   ```powershell
   cd c:\....\file-integrity-checker
   ```
4. Install the required dependencies using `pip`:
   ```powershell
   pip install -r requirements.txt
   ```
   *(This will install the required `PyQt6` library).*

## User Guide (How to Use)

1. **Launch the Application**: Run the script from your terminal:
   ```powershell
   python main.py
   ```
2. **Register the Baseline File**: 
   - Under the **"1. Baseline File"** section, click **Select Original File**.
   - Browse and select the file you want to use as your trusted original source.
   - The application will automatically generate and display its SHA-256 hash.
3. **Verify a File**:
   - Under the **"2. Verification File"** section, click **Select File to Verify** (this button becomes clickable only after an original file is selected).
   - Browse and select the file you want to test against the baseline.
   - The application will generate its hash and instantly compare it.
4. **View the Results**:
   - Scroll down to the **Comparison Results** section.
   - You will see both the Original Hash and the Verification Hash displayed.
   - A prominent status message will inform you if the **File Integrity is Verified** (no changes detected) or if the **File is Modified** (integrity check failed).

## Technologies Used

- **Python**: Core programming language.
- **PyQt6**: The toolkit used for crafting the Graphical User Interface.
- **hashlib**: Built-in Python library used to compute the SHA-256 hashes.
- **os**: Used for handling file paths and basic operating system interactions.
