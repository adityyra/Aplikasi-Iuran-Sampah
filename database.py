import sqlite3

DB_NAME = "data.db"

class MockResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pembayaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_warga TEXT NOT NULL,
            alamat TEXT,
            bulan TEXT,
            nominal INTEGER,
            status TEXT,
            status_langganan TEXT DEFAULT 'Aktif'
        )
    ''')
    
    # Migrasi sederhana: Coba tambah kolom kalau belum ada
    try:
        c.execute("ALTER TABLE pembayaran ADD COLUMN status_langganan TEXT DEFAULT 'Aktif'")
    except sqlite3.OperationalError:
        # Kolomnya mungkin sudah ada
        pass
        
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Supaya hasilnya bisa diakses kayak dictionary
    c = conn.cursor()
    c.execute("SELECT * FROM pembayaran ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    
    # Ubah jadi list berisi dictionary
    result = []
    for row in rows:
        result.append(dict(row))
    return result

def insert_data(payload):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO pembayaran (nama_warga, alamat, bulan, nominal, status, status_langganan)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            payload['nama_warga'], 
            payload['alamat'], 
            payload['bulan'], 
            payload['nominal'], 
            payload['status'],
            payload.get('status_langganan', 'Aktif')
        ))
        conn.commit()
        conn.close()
        return MockResponse(201)
    except Exception as e:
        return MockResponse(500, str(e))

def update_data(id_data, payload):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            UPDATE pembayaran 
            SET nama_warga=?, alamat=?, bulan=?, nominal=?, status=?, status_langganan=?
            WHERE id=?
        ''', (
            payload['nama_warga'], 
            payload['alamat'], 
            payload['bulan'], 
            payload['nominal'], 
            payload['status'],
            payload.get('status_langganan', 'Aktif'),
            id_data
        ))
        conn.commit()
        conn.close()
        return MockResponse(200)
    except Exception as e:
        return MockResponse(500, str(e))

def delete_data(id_data):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM pembayaran WHERE id=?", (id_data,))
        conn.commit()
        conn.close()
        return MockResponse(200)
    except Exception as e:
        return MockResponse(500, str(e))
