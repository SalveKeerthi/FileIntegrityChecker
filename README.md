# File Integrity Checker (SHA-256) - Phase 2 Security Dashboard

A professional desktop application built with Python and PyQt6 designed to verify the integrity of files. Phase 2 introduces a persistent **SQLite Database** to act as a secure repository for your trusted files and maintains a comprehensive **Verification Audit Log**.

## Features

- **Permanent File Registration**: Safely store metadata and original SHA-256 hashes of critical files in a local SQLite database. 
- **Invisible Data Storage**: The application cleanly stores the SQLite database in the hidden Windows `AppData` directory (`%LOCALAPPDATA%\FileIntegrityChecker`) to maintain a professional, clutter-free environment for the user.
- **Registered Files Dashboard**: A clean left-hand panel lists all your monitored files, allowing you to instantly search and select them.
- **Verification History**: Every integrity check is tracked. See a historical log of PASS/FAIL events for each specific file.
- **Global Audit Log**: Maintain a complete, enterprise-like security record of all verification activities across the entire system.
- **SHA-256 Hashing**: Uses the robust SHA-256 cryptographic algorithm to ensure high-security integrity checks.
- **Clean Graphical User Interface (GUI)**: Built with PyQt6, featuring a modern split-pane layout and responsive design.
- **Standalone Executable**: Fully compiled into a single `.exe` file that can be distributed and run on any Windows machine without requiring a Python installation.

## Cybersecurity Concepts Applied

- **File Integrity Monitoring (FIM)**: Tracking trusted files and identifying unauthorized changes.
- **Audit Logging**: Maintaining records of security-related events.
- **Security Event Tracking**: Recording all verification attempts for future investigation.
- **Digital Evidence Preservation**: Providing historical records that can be used to determine when modifications occurred.

## Installation & Deployment

### Running the Standalone Executable (Recommended)
1. Navigate to the `dist` folder.
2. Run `File_Integrity_Dashboard.exe`.
*No installation of Python or dependencies is required!*

### Running from Source Code
1. Open your terminal or command prompt and navigate to the project directory:
   ```powershell
   cd "c:\Users\salve\DEV\Cyber\FILE INTEGRITY CHECKER"
   ```
2. Install the required dependencies using `pip`:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the application:
   ```powershell
   python main.py
   ```

### Building the Executable Yourself
If you modify the source code, you can easily package a new `.exe` by running:
```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name "File_Integrity_Dashboard" main.py
```

## User Guide (How to Use)

1. **Launch the Application**: Run the `File_Integrity_Dashboard.exe` or `python main.py`.
2. **Register a New File**: 
   - Click the **Register New File** button on the left panel.
   - Select your trusted baseline file. It will be hashed and permanently stored in the database.
   - The file will now appear in the "Registered Files" list.
3. **Verify a File**:
   - Select a file from the "Registered Files" list.
   - Click the **Verify Selected File** button on the right panel.
   - The app will re-hash the target file and compare it with the stored original hash.
   - The result (PASS/FAIL) will be displayed immediately and permanently logged.
4. **View History and Logs**:
   - Look under **Recent Verification History for this File** to see past checks for the currently selected file.
   - Switch to the **Global Audit Log** tab to view a comprehensive list of all verification activities across all files.
5. **Search**:
   - Use the search bar at the top of the left panel to filter through your registered files by name.

## Technologies Used

- **Python**: Core programming language.
- **PyQt6**: The toolkit used for crafting the Graphical User Interface.
- **SQLite3**: Lightweight, disk-based database for persistence.
- **hashlib**: Built-in Python library used to compute the SHA-256 hashes.
- **PyInstaller**: Used to compile the application into a standalone Windows executable.
