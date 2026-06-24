import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'FileIntegrityChecker')
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_NAME = os.path.join(DB_DIR, "integrity_db.sqlite")

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table 1: Registered Files
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registered_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            sha256_hash TEXT NOT NULL,
            registration_date TEXT NOT NULL
        )
    """)
    
    # Table 2: Verification History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            verification_date TEXT NOT NULL,
            result TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def register_file(file_name, file_path, sha256_hash):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if already registered
    cursor.execute("SELECT id FROM registered_files WHERE file_path = ?", (file_path,))
    if cursor.fetchone():
        # Update existing
        cursor.execute("""
            UPDATE registered_files 
            SET file_name = ?, sha256_hash = ?, registration_date = ?
            WHERE file_path = ?
        """, (file_name, sha256_hash, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_path))
    else:
        # Insert new
        cursor.execute("""
            INSERT INTO registered_files (file_name, file_path, sha256_hash, registration_date)
            VALUES (?, ?, ?, ?)
        """, (file_name, file_path, sha256_hash, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
    conn.commit()
    conn.close()

def get_registered_files(search_query=""):
    conn = get_connection()
    cursor = conn.cursor()
    
    if search_query:
        cursor.execute("""
            SELECT file_name, file_path, sha256_hash, registration_date 
            FROM registered_files 
            WHERE file_name LIKE ? OR file_path LIKE ?
            ORDER BY file_name ASC
        """, (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("""
            SELECT file_name, file_path, sha256_hash, registration_date 
            FROM registered_files 
            ORDER BY file_name ASC
        """)
        
    results = cursor.fetchall()
    conn.close()
    
    # Convert to list of dicts for easier usage
    return [
        {
            "file_name": row[0],
            "file_path": row[1],
            "sha256_hash": row[2],
            "registration_date": row[3]
        }
        for row in results
    ]

def get_file_by_name(file_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT file_name, file_path, sha256_hash, registration_date 
        FROM registered_files 
        WHERE file_name = ?
    """, (file_name,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "file_name": row[0],
            "file_path": row[1],
            "sha256_hash": row[2],
            "registration_date": row[3]
        }
    return None

def log_verification(file_name, result):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO verification_history (file_name, verification_date, result)
        VALUES (?, ?, ?)
    """, (file_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), result))
    
    conn.commit()
    conn.close()

def get_verification_history(file_name=None, filter_result=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT file_name, verification_date, result FROM verification_history WHERE 1=1"
    params = []
    
    if file_name:
        query += " AND file_name = ?"
        params.append(file_name)
        
    if filter_result:
        query += " AND result = ?"
        params.append(filter_result)
        
    query += " ORDER BY verification_date DESC"
    
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "file_name": row[0],
            "verification_date": row[1],
            "result": row[2]
        }
        for row in results
    ]

# Initialize db when this module is imported
init_db()
