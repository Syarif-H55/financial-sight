from pathlib import Path
import json
from collections import defaultdict
from typing import List, Dict, Any


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SAMPLE_FILE = DATA_DIR / "sample_data.json"
GOALS_FILE = DATA_DIR / "goals.json"


def load_transactions() -> List[Dict[str, Any]]:
    if SAMPLE_FILE.exists():
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("transactions", [])
    return []


def get_summary() -> Dict[str, Any]:
    txs = load_transactions()
    monthly_income = 0.0
    monthly_expenses = 0.0
    by_category = defaultdict(float)

    for tx in txs:
        amount = float(tx.get("amount", 0))
        category = tx.get("category", "other")
        ttype = tx.get("type", "expense")
        if ttype == "income":
            monthly_income += amount
        else:
            monthly_expenses += amount
            by_category[category] += amount

    # Convert defaultdict to regular dict for JSON serialization
    return {
        "monthly_income": round(monthly_income, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "by_category": dict(by_category),
        "emergency_fund": round(2 * monthly_expenses, 2),  # simple placeholder
    }


def save_transactions(transactions: List[Dict[str, Any]]) -> bool:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(SAMPLE_FILE, "w", encoding="utf-8") as f:
            json.dump({"transactions": transactions}, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def append_transaction(tx: Dict[str, Any]) -> bool:
    txs = load_transactions()
    txs.append(tx)
    return save_transactions(txs)


def remove_transaction_by_index(index: int) -> bool:
    txs = load_transactions()
    if index < 0 or index >= len(txs):
        return False
    del txs[index]
    return save_transactions(txs)


# Goals persistence
def load_goals() -> List[Dict[str, Any]]:
    if GOALS_FILE.exists():
        with open(GOALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("goals", [])
    return []


def save_goals(goals: List[Dict[str, Any]]) -> bool:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(GOALS_FILE, "w", encoding="utf-8") as f:
            json.dump({"goals": goals}, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def save_goal(goal: Dict[str, Any]) -> bool:
    goals = load_goals()
    goals.append(goal)
    return save_goals(goals)


def update_goal_progress(index: int, increment: float) -> bool:
    goals = load_goals()
    if index < 0 or index >= len(goals):
        return False
    goals[index]["current"] = float(goals[index].get("current", 0)) + float(increment)
    return save_goals(goals)


def delete_goal(index: int) -> bool:
    goals = load_goals()
    if index < 0 or index >= len(goals):
        return False
    del goals[index]
    return save_goals(goals)


