import sqlite3
from pathlib import Path
from datetime import datetime

# Database file location
DB_PATH = Path(__file__).resolve().parent / "finsight.db"

def init_sample_data():
    """Initialize the SQLite database with sample data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM goals")
    cursor.execute("DELETE FROM budgets")
    
    # Insert sample transactions
    sample_transactions = [
        ("2025-09-01", "Gaji September", 8000000, "income", "salary"),
        ("2025-09-02", "Makan pagi", 25000, "expense", "food"),
        ("2025-09-02", "Transportasi", 15000, "expense", "transport"),
        ("2025-09-05", "Belanja bulanan", 450000, "expense", "shopping"),
        ("2025-09-08", "Tagihan listrik", 200000, "expense", "utilities"),
        ("2025-09-10", "Bonus proyek", 1500000, "income", "bonus"),
        ("2025-09-15", "Makan siang", 45000, "expense", "food"),
        ("2025-09-18", "Kuliah online", 300000, "expense", "education"),
        ("2025-09-20", "Investasi reksadana", 500000, "expense", "investment"),
        ("2025-09-22", "Makan malam", 60000, "expense", "food"),
        ("2025-09-25", "Pengembalian uang", 100000, "income", "other"),
        ("2025-10-01", "Gaji Oktober", 8000000, "income", "salary"),
        ("2025-10-03", "Bensin mobil", 150000, "expense", "transport"),
        ("2025-10-05", "Warung makan", 35000, "expense", "food"),
        ("2025-10-07", "Internet bulanan", 300000, "expense", "utilities"),
        ("2025-10-10", "Coffe shop", 55000, "expense", "food"),
        ("2025-10-15", "Buku pelajaran", 150000, "expense", "education"),
        ("2025-10-18", "Donasi", 100000, "expense", "other"),
        ("2025-10-20", "Streaming service", 75000, "expense", "entertainment"),
        ("2025-10-22", "Laundry", 30000, "expense", "other"),
        ("2025-10-25", "Makan di restoran", 120000, "expense", "food"),
        ("2025-10-27", "Pembelian aplikasi", 45000, "expense", "entertainment"),
    ]
    
    cursor.executemany('''
        INSERT INTO transactions (date, description, amount, type, category)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_transactions)
    
    # Insert sample goals
    sample_goals = [
        ("Dana Darurat", 20000000, 8000000),
        ("Liburan Akhir Tahun", 10000000, 2500000),
        ("Pembelian Laptop Baru", 15000000, 5000000),
        ("Tabungan Pensiun", 500000000, 50000000),
    ]
    
    cursor.executemany('''
        INSERT INTO goals (name, target, current)
        VALUES (?, ?, ?)
    ''', sample_goals)
    
    # Insert sample budgets
    sample_budgets = [
        ("food", 1500000, "2025-10"),
        ("transport", 600000, "2025-10"),
        ("utilities", 500000, "2025-10"),
        ("entertainment", 400000, "2025-10"),
        ("shopping", 1000000, "2025-10"),
        ("education", 500000, "2025-10"),
        ("investment", 1000000, "2025-10"),
        ("other", 500000, "2025-10"),
    ]
    
    cursor.executemany('''
        INSERT INTO budgets (category, amount, month)
        VALUES (?, ?, ?)
    ''', sample_budgets)
    
    conn.commit()
    conn.close()
    
    print("Sample data has been inserted into the database.")

if __name__ == "__main__":
    init_sample_data()