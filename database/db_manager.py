import sqlite3
import bcrypt
import os

class DatabaseManager:
    def __init__(self, db_path='d:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # Users Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            display_name TEXT,
            last_login DATETIME
        )
        ''')

        # Customers Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            total_purchases REAL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Vehicles Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            vin TEXT UNIQUE,
            price REAL NOT NULL,
            status TEXT DEFAULT 'Available',
            image_path TEXT
        )
        ''')

        # Sales Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            vehicle_id INTEGER,
            user_id INTEGER,
            price REAL NOT NULL,
            sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            payment_type TEXT,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Warehouse Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS warehouse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_name TEXT NOT NULL,
            quantity INTEGER DEFAULT 0,
            min_quantity INTEGER DEFAULT 10,
            price REAL
        )
        ''')

        # Activity Logs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        conn.commit()
        conn.close()
        self._seed_data()

    def _seed_data(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # Check if admin exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            password = b"admin123"
            hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO users (username, password_hash, role, display_name) VALUES (?, ?, ?, ?)",
                           ('admin', hashed, 'Admin', 'Administrator'))
        
        # Seed some dummy data if empty
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        if cursor.fetchone()[0] == 0:
            vehicles = [
                ('Chevrolet', 'Tracker Premier', 2024, 'VIN123456789', 21400.0, 'Available'),
                ('Chevrolet', 'Onix Turbo', 2024, 'VIN987654321', 18200.0, 'Available'),
                ('Kia', 'K5 Prestige', 2023, 'VIN555666777', 32000.0, 'Available'),
                ('BYD', 'Song Plus', 2024, 'VIN888999000', 38000.0, 'Available')
            ]
            cursor.executemany("INSERT INTO vehicles (brand, model, year, vin, price, status) VALUES (?, ?, ?, ?, ?, ?)", vehicles)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialized and seeded.")
