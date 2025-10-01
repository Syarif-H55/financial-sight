from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import json

# Robust imports: try absolute (python -m backend.app), then package-relative, then local
try:  # absolute package imports
    from backend.financial_ai import generate_recommendations, compute_financial_health
    from backend.database import (
        load_transactions,
        get_summary,
        append_transaction,
        remove_transaction_by_index,
        load_goals,
        save_goal,
        update_goal_progress,
        delete_goal,
    )
except ImportError:
    try:  # relative imports when run inside package context
        from .financial_ai import generate_recommendations, compute_financial_health
        from .database import (
            load_transactions,
            get_summary,
            append_transaction,
            remove_transaction_by_index,
            load_goals,
            save_goal,
            update_goal_progress,
            delete_goal,
        )
    except ImportError:  # fallback for direct script run
        from financial_ai import generate_recommendations, compute_financial_health
        from database import (
            load_transactions,
            get_summary,
            append_transaction,
            remove_transaction_by_index,
            load_goals,
            save_goal,
            update_goal_progress,
            delete_goal,
        )


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/transactions")
    def transactions():
        data = load_transactions()
        return jsonify({"transactions": data})

    @app.get("/api/summary")
    def summary():
        summary_data = get_summary()
        health = compute_financial_health(summary_data)
        return jsonify({"summary": summary_data, "health": health})

    def _in_range(month: str, start: str | None, end: str | None) -> bool:
        if not month:
            return False
        if start and month < start:
            return False
        if end and month > end:
            return False
        return True

    @app.get("/api/trend")
    def trend():
        # Aggregate by YYYY-MM with optional range filters (?start=YYYY-MM&end=YYYY-MM)
        start = request.args.get("start")
        end = request.args.get("end")
        txs = load_transactions()
        monthly = {}
        for tx in txs:
            date = str(tx.get("date", ""))
            month = date[:7]
            if (start or end) and not _in_range(month, start, end):
                continue
            if month not in monthly:
                monthly[month] = {"income": 0.0, "expenses": 0.0}
            amount = float(tx.get("amount", 0))
            if tx.get("type") == "income":
                monthly[month]["income"] += amount
            else:
                monthly[month]["expenses"] += amount
        # Sort by month key
        months = sorted(monthly.keys())
        income = [round(monthly[m]["income"], 2) for m in months]
        expenses = [round(monthly[m]["expenses"], 2) for m in months]
        return jsonify({"months": months, "income": income, "expenses": expenses})

    @app.get("/api/analytics/category-month")
    def analytics_category_month():
        # Build months and per-category series across months, with optional range filters
        start = request.args.get("start")
        end = request.args.get("end")
        txs = load_transactions()
        months_set = set()
        cats = set()
        for tx in txs:
            m = str(tx.get("date", ""))[:7]
            if (start or end) and not _in_range(m, start, end):
                continue
            months_set.add(m)
            if tx.get("type") != "income":
                cats.add(tx.get("category", "other"))
        months = sorted(months_set)
        cat_series = {c: [0.0 for _ in months] for c in cats}
        month_index = {m: i for i, m in enumerate(months)}
        for tx in txs:
            if tx.get("type") == "income":
                continue
            m = str(tx.get("date", ""))[:7]
            if (start or end) and not _in_range(m, start, end):
                continue
            idx = month_index.get(m)
            if idx is None:
                continue
            c = tx.get("category", "other")
            cat_series[c][idx] += float(tx.get("amount", 0))
        # round
        for c in cat_series:
            cat_series[c] = [round(v, 2) for v in cat_series[c]]
        return jsonify({"months": months, "categories": cat_series})

    @app.post("/api/recommendations")
    def recommendations():
        payload = request.get_json(silent=True) or {}
        summary_data = payload.get("summary") or get_summary()
        recs = generate_recommendations(summary_data)
        return jsonify({"recommendations": recs})

    @app.get("/api/ai/suggestions")
    def ai_suggestions():
        summary_data = get_summary()
        goals = load_goals()
        # reuse trend aggregation for monthly context if needed
        txs = load_transactions()
        monthly = {"count": len(txs)}
        from .financial_ai import generate_structured_suggestions  # safe local import
        suggestions = generate_structured_suggestions(summary_data, goals, monthly)
        return jsonify({"suggestions": suggestions})

    @app.post("/api/transactions")
    def add_transaction():
        payload = request.get_json(silent=True) or {}
        required = {"date", "description", "amount", "type", "category"}
        if not required.issubset(payload.keys()):
            return jsonify({"error": "Invalid payload"}), 400
        ok = append_transaction(payload)
        if not ok:
            return jsonify({"error": "Failed to save"}), 500
        return jsonify({"status": "ok"})

    @app.delete("/api/transactions")
    def delete_transaction():
        payload = request.get_json(silent=True) or {}
        index = payload.get("index")
        if index is None:
            return jsonify({"error": "index required"}), 400
        ok = remove_transaction_by_index(int(index))
        if not ok:
            return jsonify({"error": "Failed to delete"}), 400
        return jsonify({"status": "ok"})

    # Goals API
    @app.get("/api/goals")
    def goals_list():
        return jsonify({"goals": load_goals()})

    @app.post("/api/goals")
    def goals_add():
        payload = request.get_json(silent=True) or {}
        required = {"name", "target", "current"}
        if not required.issubset(payload.keys()):
            return jsonify({"error": "Invalid payload"}), 400
        ok = save_goal(payload)
        if not ok:
            return jsonify({"error": "Failed to save"}), 500
        return jsonify({"status": "ok"})

    @app.patch("/api/goals")
    def goals_update():
        payload = request.get_json(silent=True) or {}
        idx = payload.get("index")
        inc = payload.get("increment")
        if idx is None or inc is None:
            return jsonify({"error": "index and increment required"}), 400
        ok = update_goal_progress(int(idx), float(inc))
        if not ok:
            return jsonify({"error": "Failed to update"}), 400
        return jsonify({"status": "ok"})

    @app.delete("/api/goals")
    def goals_delete():
        payload = request.get_json(silent=True) or {}
        idx = payload.get("index")
        if idx is None:
            return jsonify({"error": "index required"}), 400
        ok = delete_goal(int(idx))
        if not ok:
            return jsonify({"error": "Failed to delete"}), 400
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    # Allow running as `python backend/app.py`
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


