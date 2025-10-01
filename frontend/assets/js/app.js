const API_BASE = "http://127.0.0.1:5000";

async function fetchJSON(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return res.json();
}

function formatCurrency(idr) {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(idr);
}

async function loadSummary() {
  const data = await fetchJSON("/api/summary");
  const summary = data.summary || {};
  const health = data.health || {};

  document.getElementById("income").textContent = formatCurrency(summary.monthly_income || 0);
  document.getElementById("expenses").textContent = formatCurrency(summary.monthly_expenses || 0);
  document.getElementById("health-score").textContent = health.score ?? "-";
  document.getElementById("health-status").textContent = health.status ?? "-";

  renderCategoryChart(summary.by_category || {});
  await loadRecommendations(summary);
  await loadTrend();
  await loadAISuggestions();
}

async function loadRecommendations(summary) {
  const data = await fetchJSON("/api/recommendations", {
    method: "POST",
    body: JSON.stringify({ summary })
  });
  const ul = document.getElementById("reco-list");
  ul.innerHTML = "";
  (data.recommendations || []).forEach(t => {
    const li = document.createElement("li");
    li.textContent = `💡 ${t}`;
    ul.appendChild(li);
  });
}

let categoryChart;
function renderCategoryChart(byCategory) {
  const ctx = document.getElementById("categoryChart");
  const labels = Object.keys(byCategory);
  const values = labels.map(k => byCategory[k]);

  if (categoryChart) categoryChart.destroy();
  categoryChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        label: "Pengeluaran",
        data: values,
        backgroundColor: [
          "#2563eb",
          "#059669",
          "#d97706",
          "#dc2626",
          "#7c3aed",
          "#0ea5e9"
        ]
      }]
    },
    options: {
      plugins: { legend: { position: "bottom" } }
    }
  });
}

async function loadTrend() {
  const data = await fetchJSON("/api/trend");
  const ctx = document.getElementById("trendChart");
  if (!ctx) return;
  const months = data.months || [];
  const income = data.income || [];
  const expenses = data.expenses || [];
  new Chart(ctx, {
    type: "line",
    data: {
      labels: months,
      datasets: [
        { label: "Income", data: income, borderColor: "#059669", backgroundColor: "#05966933" },
        { label: "Expenses", data: expenses, borderColor: "#dc2626", backgroundColor: "#dc262633" }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "bottom" } }
    }
  });
}

window.addEventListener("DOMContentLoaded", loadSummary);

async function loadAISuggestions() {
  const data = await fetchJSON('/api/ai/suggestions');
  const ul = document.getElementById('reco-list');
  if (!ul) return;
  ul.innerHTML = '';
  (data.suggestions || []).forEach(s => {
    const li = document.createElement('li');
    const impact = s.impact_idr ? ` (~${formatCurrency(s.impact_idr)})` : '';
    li.textContent = `💡 ${s.message}${impact}`;
    ul.appendChild(li);
  });
}


