const API_BASE = "http://127.0.0.1:5000";

async function fetchJSON(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  return res.json();
}

async function initAnalytics() {
  wireFilters();
  await rerender();
}

function wireFilters() {
  document.getElementById('f-apply').addEventListener('click', rerender);
}

function buildQuery() {
  const s = document.getElementById('f-start').value;
  const e = document.getElementById('f-end').value;
  const params = new URLSearchParams();
  if (s) params.set('start', s);
  if (e) params.set('end', e);
  const q = params.toString();
  return q ? `?${q}` : '';
}

async function rerender() {
  await renderTrend();
  await renderTopCategories();
  await renderCategoryByMonth();
  await renderBudgetActual();
}

async function renderTrend() {
  const data = await fetchJSON('/api/trend' + buildQuery());
  const ctx = document.getElementById('trendChart');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.months,
      datasets: [
        { label: 'Income', data: data.income, borderColor: '#059669', backgroundColor: '#05966933' },
        { label: 'Expenses', data: data.expenses, borderColor: '#dc2626', backgroundColor: '#dc262633' }
      ]
    },
    options: { plugins: { legend: { position: 'bottom' } } }
  });
}

async function renderTopCategories() {
  const summary = await fetchJSON('/api/summary');
  const cat = summary.summary.by_category || {};
  const entries = Object.entries(cat).sort((a,b) => b[1] - a[1]).slice(0, 5);
  const labels = entries.map(e => e[0]);
  const values = entries.map(e => e[1]);
  const ctx = document.getElementById('topCatChart');
  new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Top Categories', data: values, backgroundColor: '#2563eb' }] },
    options: { plugins: { legend: { display: false } } }
  });
}

async function renderCategoryByMonth() {
  const data = await fetchJSON('/api/analytics/category-month' + buildQuery());
  const ctx = document.getElementById('catMonthChart');
  const datasets = Object.keys(data.categories).map((cat, idx) => ({
    label: cat,
    data: data.categories[cat],
    borderColor: palette(idx),
    backgroundColor: palette(idx) + '33'
  }));
  new Chart(ctx, {
    type: 'line',
    data: { labels: data.months, datasets },
    options: { plugins: { legend: { position: 'bottom' } } }
  });
}

function palette(i) {
  const colors = ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed', '#0ea5e9', '#16a34a'];
  return colors[i % colors.length];
}

async function renderBudgetActual() {
  const data = await fetchJSON('/api/analytics/budget-vs-actual');
  const ctx = document.getElementById('budgetActualChart');
  
  // Prepare datasets for budget and actual values
  const months = data.months;
  const categories = data.categories;
  const chartData = data.data;
  
  // Create datasets for each category (budget and actual)
  let datasets = [];
  let colorIdx = 0;
  
  for (const category of categories) {
    // Budget dataset
    datasets.push({
      label: `${category} (Budget)`,
      data: chartData[category]?.budget || [],
      borderColor: palette(colorIdx),
      backgroundColor: palette(colorIdx) + '33',
      type: 'line',
      yAxisID: 'y'
    });
    
    // Actual dataset
    datasets.push({
      label: `${category} (Actual)`,
      data: chartData[category]?.actual || [],
      borderColor: palette(colorIdx + 1),
      backgroundColor: palette(colorIdx + 1) + '88',
      type: 'bar',
      yAxisID: 'y'
    });
    
    colorIdx += 2;
  }
  
  new Chart(ctx, {
    type: 'bar', // Use bar as base, but add line datasets for budget
    data: {
      labels: months,
      datasets: datasets
    },
    options: {
      plugins: { 
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (context.parsed.y !== null) {
                label += new Intl.NumberFormat('id-ID', { 
                  style: 'currency', 
                  currency: 'IDR' 
                }).format(context.parsed.y);
              }
              return label;
            }
          }
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
        }
      }
    }
  });
}

window.addEventListener('DOMContentLoaded', initAnalytics);


