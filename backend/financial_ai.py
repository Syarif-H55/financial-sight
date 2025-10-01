from typing import Dict, List, Any


def compute_financial_health(summary: Dict) -> Dict:
    income = summary.get("monthly_income", 0)
    expenses = summary.get("monthly_expenses", 0)
    savings = income - expenses if income and expenses else 0

    # Simple scoring: higher savings rate -> higher score
    score = 50
    if income > 0:
        savings_rate = max(0.0, min(1.0, savings / income))
        score = int(50 + savings_rate * 50)

    status = "sehat"
    if score < 40:
        status = "kritis"
    elif score < 70:
        status = "hati-hati"

    return {
        "score": score,
        "status": status,
        "savings": savings,
    }


def generate_recommendations(summary: Dict) -> List[str]:
    income = summary.get("monthly_income", 0)
    expenses = summary.get("monthly_expenses", 0)
    emergency_fund = summary.get("emergency_fund", 0)
    monthly_expenses_avg = summary.get("monthly_expenses", 0)

    recs: List[str] = []

    if income > 0 and expenses > 0 and expenses > 0.7 * income:
        recs.append("Pengeluaran >70% pendapatan. Kurangi biaya hiburan 10-20% bulan ini.")

    if emergency_fund < 3 * monthly_expenses_avg:
        recs.append("Tambahkan dana darurat hingga minimal 3x pengeluaran bulanan.")

    if income - expenses > 0:
        recs.append("Alokasikan 10% dari sisa pendapatan untuk investasi jangka panjang.")

    if not recs:
        recs.append("Kondisi stabil. Pertahankan kebiasaan baik dan evaluasi target keuangan.")

    return recs


def _format_idr(amount: float) -> int:
    try:
        return int(round(float(amount)))
    except Exception:
        return 0


def generate_structured_suggestions(summary: Dict[str, Any], goals: List[Dict[str, Any]], monthly: Dict[str, Any]) -> List[Dict[str, Any]]:
    income = float(summary.get("monthly_income", 0) or 0)
    expenses = float(summary.get("monthly_expenses", 0) or 0)
    by_category: Dict[str, float] = {k: float(v) for k, v in (summary.get("by_category", {}) or {}).items()}

    suggestions: List[Dict[str, Any]] = []

    # 1) Overspend quick win on top categories
    if expenses > 0 and by_category:
        top = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:2]
        for cat, amt in top:
            cut = amt * 0.1  # suggest cutting 10%
            suggestions.append({
                "id": f"overspend_{cat}",
                "message": f"Kurangi pengeluaran {cat} sebesar 10%",
                "reason": f"Kategori {cat} termasuk pengeluaran terbesar bulan ini",
                "suggested_action": f"Tetapkan batas baru untuk {cat} dan pantau mingguan",
                "impact_idr": _format_idr(cut),
                "level": "medium",
            })

    # 2) Emergency fund target (3x monthly expenses)
    emergency_fund = float(summary.get("emergency_fund", 0) or 0)
    target_em = expenses * 3
    if target_em > 0 and emergency_fund < target_em:
        gap = max(0.0, target_em - emergency_fund)
        monthly_boost = gap / 6.0  # 6 months plan
        suggestions.append({
            "id": "emergency_fund",
            "message": "Tambahkan dana darurat hingga 3x pengeluaran",
            "reason": "Dana darurat di bawah rekomendasi (3x pengeluaran bulanan)",
            "suggested_action": f"Sisihkan sekitar {_format_idr(monthly_boost)} per bulan selama 6 bulan",
            "impact_idr": _format_idr(monthly_boost),
            "level": "high",
        })

    # 3) Allocate surplus to highest priority goal
    surplus = max(0.0, income - expenses)
    if goals and surplus > 0:
        # pick goal with lowest progress ratio
        def progress(g: Dict[str, Any]) -> float:
            t = float(g.get("target", 0) or 0)
            c = float(g.get("current", 0) or 0)
            return (c / t) if t > 0 else 0.0
        goal_sorted = sorted(goals, key=progress)
        g0 = goal_sorted[0]
        allocate = surplus * 0.5  # 50% of surplus
        suggestions.append({
            "id": "surplus_allocation",
            "message": f"Alokasikan 50% surplus ke goal: {g0.get('name', 'Goal')}",
            "reason": "Ada surplus bulanan yang bisa dipercepat ke target prioritas",
            "suggested_action": f"Alokasikan {_format_idr(allocate)} ke '{g0.get('name','')}' bulan ini",
            "impact_idr": _format_idr(allocate),
            "level": "medium",
        })

    # 4) Savings rate check
    if income > 0:
        rate = max(0.0, (income - expenses) / income)
        if rate < 0.2:
            uplift = income * 0.2 - (income - expenses)
            suggestions.append({
                "id": "savings_rate",
                "message": "Naikkan savings rate ke 20%",
                "reason": f"Savings rate saat ini ~{int(rate*100)}%",
                "suggested_action": f"Cari penghematan {_format_idr(uplift)}/bulan atau tambah pemasukan",
                "impact_idr": _format_idr(uplift),
                "level": "high",
            })

    # Limit to top 3 by impact
    suggestions.sort(key=lambda s: s.get("impact_idr", 0), reverse=True)
    return suggestions[:3] if suggestions else [{
        "id": "stable",
        "message": "Kondisi stabil, pertahankan dan review target",
        "reason": "Tidak ada anomali berarti pada periode ini",
        "suggested_action": "Lanjutkan rencana dan evaluasi bulanan",
        "impact_idr": 0,
        "level": "low",
    }]


