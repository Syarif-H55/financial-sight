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

let allTx = [];
let viewTx = [];
let page = 1;
const PAGE_SIZE = 10;

async function init() {
  const data = await fetchJSON('/api/transactions');
  allTx = (data.transactions || []); // Store the full transaction data including IDs
  populateCategoryFilter(allTx);
  wireEvents();
  applyFilters();
}

function populateCategoryFilter(txs) {
  const sel = document.getElementById('f-category');
  if (!sel) return;
  const cats = Array.from(new Set(txs.map(t => t.category))).sort();
  sel.innerHTML = '<option value="">Semua kategori</option>' + cats.map(c => `<option value="${c}">${c}</option>`).join('');
}

function wireEvents() {
  const inputs = ['f-search', 'f-type', 'f-category', 'f-sort'];
  inputs.forEach(id => document.getElementById(id).addEventListener('input', () => { page = 1; applyFilters(); }));
  document.getElementById('pg-prev').addEventListener('click', () => { if (page > 1) { page--; renderTable(); } });
  document.getElementById('pg-next').addEventListener('click', () => { if (page * PAGE_SIZE < viewTx.length) { page++; renderTable(); } });

  const form = document.getElementById('tx-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      date: document.getElementById('i-date').value,
      description: document.getElementById('i-desc').value,
      amount: Number(document.getElementById('i-amount').value),
      type: document.getElementById('i-type').value,
      category: document.getElementById('i-category').value,
    };
    const res = await fetchJSON('/api/transactions', { method: 'POST', body: JSON.stringify(payload) });
    if (res && res.status === 'ok') {
      await init();
      form.reset();
    }
  });
}

function applyFilters() {
  const q = document.getElementById('f-search').value.toLowerCase();
  const type = document.getElementById('f-type').value;
  const cat = document.getElementById('f-category').value;
  const sort = document.getElementById('f-sort').value;

  viewTx = allTx.filter(t => {
    const okQ = !q || (t.description || '').toLowerCase().includes(q);
    const okT = !type || t.type === type;
    const okC = !cat || t.category === cat;
    return okQ && okT && okC;
  });

  const dir = sort.endsWith('desc') ? -1 : 1;
  if (sort.startsWith('date')) {
    viewTx.sort((a, b) => (a.date > b.date ? 1 : -1) * dir);
  } else {
    viewTx.sort((a, b) => (a.amount - b.amount) * dir);
  }

  renderTable();
}

function renderTable() {
  const tbody = document.getElementById('tx2-tbody');
  const info = document.getElementById('pg-info');
  if (!tbody) return;
  tbody.innerHTML = '';
  const start = (page - 1) * PAGE_SIZE;
  const rows = viewTx.slice(start, start + PAGE_SIZE);
  rows.forEach(t => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${t.date || ''}</td>
      <td>${t.description || ''}</td>
      <td>${t.category || ''}</td>
      <td>${t.type || ''}</td>
      <td>${formatCurrency(t.amount || 0)}</td>
      <td><button data-del="${t.id}">Hapus</button></td>
    `;
    tbody.appendChild(tr);
  });
  info.textContent = `Page ${page}`;
  tbody.querySelectorAll('button[data-del]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const index = e.target.getAttribute('data-del');
      const res = await fetchJSON('/api/transactions', { method: 'DELETE', body: JSON.stringify({ id: Number(index) }) });
      if (res && res.status === 'ok') {
        await init();
      }
    });
  });
}

window.addEventListener('DOMContentLoaded', init);


