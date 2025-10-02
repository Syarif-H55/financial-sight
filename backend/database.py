import sqlite3
from pathlib import Path
from typing import List, Dict, Any


# Database file location
DB_PATH = Path(__file__).resolve().parent / "finsight.db"


def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    # Create goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target REAL NOT NULL,
            current REAL NOT NULL DEFAULT 0
        )
    ''')
    
    # Create budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


def load_transactions() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, description, amount, type, category FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    transactions = []
    for row in rows:
        transactions.append({
            "id": row[0],
            "date": row[1],
            "description": row[2],
            "amount": row[3],
            "type": row[4],
            "category": row[5]
        })
    
    return transactions


def get_summary() -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT type, category, amount FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    
    monthly_income = 0.0
    monthly_expenses = 0.0
    by_category = {}
    
    for row in rows:
        ttype, category, amount = row[0], row[1], row[2]
        amount = float(amount)
        if ttype == "income":
            monthly_income += amount
        else:
            monthly_expenses += amount
            if category in by_category:
                by_category[category] += amount
            else:
                by_category[category] = amount

    # Convert defaultdict to regular dict for JSON serialization
    return {
        "monthly_income": round(monthly_income, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "by_category": by_category,
        "emergency_fund": round(2 * monthly_expenses, 2),  # simple placeholder
    }


def append_transaction(tx: Dict[str, Any]) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO transactions (date, description, amount, type, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (tx["date"], tx["description"], tx["amount"], tx["type"], tx["category"]))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def remove_transaction_by_id(transaction_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def get_transaction_by_id(trans_id: int) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date, description, amount, type, category FROM transactions WHERE id = ?", (trans_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "date": row[0],
            "description": row[1],
            "amount": row[2],
            "type": row[3],
            "category": row[4]
        }
    return None


def get_transaction_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    conn.close()
    return count


# Goals persistence
def load_goals() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, target, current FROM goals ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    goals = []
    for row in rows:
        goals.append({
            "id": row[0],
            "name": row[1],
            "target": row[2],
            "current": row[3]
        })
    
    return goals


def save_goal(goal: Dict[str, Any]) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO goals (name, target, current)
            VALUES (?, ?, ?)
        ''', (goal["name"], goal["target"], goal["current"]))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def update_goal_progress(goal_id: int, increment: float) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE goals SET current = current + ? WHERE id = ?", (increment, goal_id))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def delete_goal(goal_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def get_goal_by_id(goal_id: int) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, target, current FROM goals WHERE id = ?", (goal_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "target": row[2],
            "current": row[3]
        }
    return None


# Budget persistence
def load_budgets() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, month FROM budgets ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    budgets = []
    for row in rows:
        budgets.append({
            "id": row[0],
            "category": row[1],
            "amount": row[2],
            "month": row[3]
        })
    
    return budgets


def save_budget(budget: Dict[str, Any]) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO budgets (category, amount, month)
            VALUES (?, ?, ?)
        ''', (budget["category"], budget["amount"], budget["month"]))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def delete_budget(budget_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def get_budget_by_id(budget_id: int) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, month FROM budgets WHERE id = ?", (budget_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "category": row[1],
            "amount": row[2],
            "month": row[3]
        }
    return None


# Initialize the database on import
init_db()


