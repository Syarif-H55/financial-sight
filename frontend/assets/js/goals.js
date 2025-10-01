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

async function initGoals() {
  wireForm();
  await renderGoals();
}

function wireForm() {
  const form = document.getElementById('goal-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('g-name').value,
      target: Number(document.getElementById('g-target').value),
      current: Number(document.getElementById('g-current').value),
      deadline: document.getElementById('g-deadline').value || null,
    };
    const res = await fetchJSON('/api/goals', { method: 'POST', body: JSON.stringify(payload) });
    if (res && res.status === 'ok') {
      form.reset();
      await renderGoals();
    }
  });
}

async function renderGoals() {
  const list = document.getElementById('goals-list');
  list.innerHTML = '';
  const data = await fetchJSON('/api/goals');
  (data.goals || []).forEach((g, idx) => {
    const pct = g.target > 0 ? Math.min(100, Math.round((g.current / g.target) * 100)) : 0;
    const div = document.createElement('div');
    div.className = 'goal-card';
    div.innerHTML = `
      <div>
        <div class="goal-title">${g.name}</div>
        <div class="goal-meta">${formatCurrency(g.current)} / ${formatCurrency(g.target)}${g.deadline ? ` · target: ${g.deadline}` : ''}</div>
        <div class="progress"><span style="width:${pct}%"></span></div>
      </div>
      <div class="goal-actions">
        <input type="number" min="0" placeholder="Tambah (IDR)" data-add />
        <button data-add-btn="${idx}">Update</button>
        <button data-del-btn="${idx}">Hapus</button>
      </div>
    `;
    list.appendChild(div);
  });

  list.querySelectorAll('[data-add-btn]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const idx = Number(e.target.getAttribute('data-add-btn'));
      const input = e.target.closest('.goal-card').querySelector('[data-add]');
      const inc = Number(input.value || 0);
      if (inc <= 0) return;
      const res = await fetchJSON('/api/goals', { method: 'PATCH', body: JSON.stringify({ index: idx, increment: inc }) });
      if (res && res.status === 'ok') await renderGoals();
    });
  });

  list.querySelectorAll('[data-del-btn]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const idx = Number(e.target.getAttribute('data-del-btn'));
      const res = await fetchJSON('/api/goals', { method: 'DELETE', body: JSON.stringify({ index: idx }) });
      if (res && res.status === 'ok') await renderGoals();
    });
  });
}

window.addEventListener('DOMContentLoaded', initGoals);


