const API_BASE = "http://127.0.0.1:5000";

async function fetchJSON(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  return res.json();
}

async function loadBudgets() {
  try {
    const data = await fetchJSON('/api/budgets');
    const container = document.getElementById('budgets-list');
    
    if (!data.budgets || data.budgets.length === 0) {
      container.innerHTML = '<p>Tidak ada anggaran yang diatur.</p>';
      return;
    }
    
    let html = '<ul class="goals-list">';
    data.budgets.forEach((budget) => {
      html += `
        <li class="goal-item">
          <div class="goal-info">
            <h3>${budget.category}</h3>
            <p>Anggaran: ${formatCurrency(budget.amount)} | Bulan: ${budget.month}</p>
          </div>
          <button class="delete-btn" data-id="${budget.id}">Hapus</button>
        </li>
      `;
    });
    html += '</ul>';
    
    container.innerHTML = html;
    
    // Add event listeners to delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const budget_id = parseInt(btn.getAttribute('data-id'));
        if (confirm('Apakah Anda yakin ingin menghapus anggaran ini?')) {
          try {
            await fetchJSON(`/api/budgets`, {
              method: 'DELETE',
              body: JSON.stringify({ id: budget_id })
            });
            loadBudgets(); // Refresh the list
          } catch (error) {
            console.error('Error deleting budget:', error);
            alert('Gagal menghapus anggaran');
          }
        }
      });
    });
  } catch (error) {
    console.error('Error loading budgets:', error);
    document.getElementById('budgets-list').innerHTML = '<p>Terjadi kesalahan saat memuat anggaran.</p>';
  }
}

function formatCurrency(idr) {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(idr);
}

document.getElementById('budget-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const category = document.getElementById('category').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const month = document.getElementById('month').value;
  
  if (!category || !amount || !month) {
    alert('Harap lengkapi semua field');
    return;
  }
  
  try {
    await fetchJSON('/api/budgets', {
      method: 'POST',
      body: JSON.stringify({ category, amount, month })
    });
    
    document.getElementById('budget-form').reset();
    loadBudgets(); // Refresh the list
    alert('Anggaran berhasil ditambahkan');
  } catch (error) {
    console.error('Error adding budget:', error);
    alert('Gagal menambahkan anggaran');
  }
});

window.addEventListener('DOMContentLoaded', loadBudgets);