FINSIGHT (Financial Insight) - Localhost MVP

Run locally with Python Flask backend and a simple HTML/CSS/JS frontend.

Quickstart
1) Create virtual env (optional) and install deps:
   pip install -r requirements.txt
2) Start backend (choose one):
   python -m backend.app
   # or
   python backend/app.py
3) Open frontend pages (or serve via Live Server):
   - frontend/pages/index.html (Dashboard)
   - frontend/pages/transaction.html (Transactions)
   - frontend/pages/goals.html (Goals)
   - frontend/pages/analytics.html (Analytics)

Project Structure
backend/                         # Flask server, AI rules, data access
frontend/
  pages/                        # .html pages
  assets/
    css/                        # styles
    js/                         # scripts
data/                           # Sample JSON/SQLite files

Endpoints
- GET /api/health                -> backend health status
- GET /api/transactions         -> list sample transactions
- GET /api/summary              -> aggregates for charts
- POST /api/recommendations     -> AI suggestions based on simple rules
 - GET /api/ai/suggestions       -> Rich AI suggestions (reason, action, impact)

Notes
- This MVP uses in-memory/sample JSON. You can switch to SQLite later.
- Frontend fetches data from http://localhost:5000.

NEXT DEVELOPMENT=
Oke, paham! Untuk keperluan kelulusan semester 3 yang berjalan di localhost saja, arsitektur dan teknologi yang dibutuhkan bisa jauh lebih sederhana. Berikut penyesuaian rekomendasinya:

## 🎯 **Rekomendasi Teknologi (Versi Localhost/Skala Kampus)**

### **Frontend: Tetap HTML, CSS, JavaScript**
- **HTML**: Struktur aplikasi
- **CSS**: Styling dan layout dasbor  
- **JavaScript**: Interaktivitas, grafik, dan komunikasi dengan backend
- **Framework Pilihan**: 
  - **React.js** atau **Vue.js** (jika ingin belajar framework modern)
  - **Vanilla JavaScript** dengan **Chart.js** untuk grafik (lebih sederhana)

### **Backend & AI: Python dengan Flask**
- **Flask** (micro web framework) - sangat cocok untuk project skala kecil
- **Python** untuk logika AI dan analisis data
- **SQLite** untuk database (file-based, tidak perlu install server)

## 🚀 **Arsitektur Sederhana untuk Localhost**

```
Financial Insight (FINSIGHT)
├── frontend/ (HTML, CSS, JavaScript)
│   ├── index.html (dashboard utama)
│   ├── styles/ (file CSS)
│   ├── scripts/ (file JavaScript)
│   └── charts/ (visualisasi data)
├── backend/ (Python Flask)
│   ├── app.py (server utama)
│   ├── ai_models/ (logika AI sederhana)
│   ├── database/ (SQLite files)
│   └── utils/ (helper functions)
└── data/ (sample data untuk demo)
```

## 💡 **Implementasi Fitur AI yang Realistis**

### **1. AI Suggestion Financial (Sederhana)**
```python
# Contoh logika AI sederhana untuk rekomendasi
def financial_suggestion(pengeluaran, tabungan, tujuan):
    if pengeluaran > 0.7 * pendapatan:
        return "⚠️ Pengeluaran melebihi 70% pendapatan. Disarankan mengurangi pengeluaran hiburan."
    elif tabungan < 3 * pengeluaran_bulanan:
        return "🎯 Prioritaskan menambah dana darurat hingga 3x pengeluaran bulanan."
    else:
        return "✅ Kondisi keuangan sehat. Pertimbangkan investasi jangka panjang."
```

### **2. Financial Analytic** 
- **Chart.js** untuk visualisasi:
  - Pie chart kategori pengeluaran
  - Line chart trend bulanan
  - Bar chart perbandingan anggaran vs realisasi

### **3. Financial Recommendation**
- Sistem rule-based sederhana
- Rekomendasi berdasarkan kondisi keuangan mockup data

## 🛡️ **Mitigasi Risiko untuk Skala Kampus**

### **Risiko Teknis:**
- **Data Tidak Tersimpan**: Gunakan SQLite dengan backup manual
- **Bug & Error**: Implementasi unit testing sederhana
- **Integrasi API**: Gunakan dataset mock/stub data

### **Risiko Kinerja:**
- **Tampilan Responsif**: Gunakan CSS Grid/Flexbox
- **Penanganan Data**: Batasi data demo (max 1000 records)

### **Risiko Akurasi AI:**
- **AI Sederhana**: Fokus pada rule-based system, bukan machine learning kompleks
- **Transparansi**: Tampilkan jelas bahwa ini adalah sistem demo

### **Risiko Keamanan:**
- **Localhost Only**: Tidak perlu enkripsi kompleks
- **Basic Validation**: Validasi input di frontend dan backend

## 📋 **Checklist Kelayakan Project**

### **Yang Perlu Disiapkan:**
- [ ] Mockup data transaksi keuangan (6 bulan)
- [ ] Design wireframe dasbor
- [ ] Rule-based algorithm untuk rekomendasi
- [ ] Visualisasi data dengan Chart.js
- [ ] Flask API endpoints
- [ ] Dokumentasi penggunaan

### **Teknologi yang Perlu Dipelajari:**
1. **Python & Flask** (backend sederhana)
2. **JavaScript Fetch API** (komunikasi frontend-backend)
3. **Chart.js** atau **D3.js** (visualisasi)
4. **SQLite** (database sederhana)
5. **CSS Grid/Flexbox** (layout responsive)

## 🎓 **Kriteria Penilaian yang Kemungkinan Diperhatikan**

1. **Kelengkapan Fitur** - Semua fitur dasar berfungsi
2. **Kualitas Kode** - Terstruktur dan terdokumentasi
3. **User Experience** - Interface yang intuitif
4. **Inovasi** - Implementasi "AI" meski sederhana
5. **Presentasi** - Dokumentasi dan demo yang jelas

## 📝 **Contoh Struktur Project Sederhana**

```bash
finsight-project/
├── README.md
├── requirements.txt
├── backend/
│   ├── app.py
│   ├── financial_ai.py
│   └── database.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── charts.js
└── data/
    └── sample_data.json
```

**Kesimpulan**: Dengan scope localhost, project FINSIGHT sangat feasible menggunakan HTML/CSS/JS + Python Flask. Fokus pada implementasi fitur dasar yang bekerja dengan baik, dan buat "AI" sebagai sistem rule-based yang intelligent meski sederhana.

Semoga membantu! Ada pertanyaan lebih lanjut tentang implementasi teknis tertentu?

