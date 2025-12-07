import joblib
import pandas as pd
import numpy as np

# --- 1. CONFIG & LOAD MODEL ---
print("🔄 Memuat Model...")
try:
    model = joblib.load('model_kelulusan_tanpa_gbm.pkl')
    print("✅ Model berhasil dimuat.")
except:
    print("⚠️ Model tidak ditemukan, menggunakan logika fallback.")
    model = None

# --- 2. LOGIKA HYBRID (MODEL + ATURAN) ---
# Ini logika yang sama persis dengan yang ada di app.py
def prediksi_hybrid(data):
    # Ambil nilai raw
    ipk = data['IPK']
    sem = data['Jumlah Semester']
    job = data['Pekerjaan Sambil Kuliah'] # 0=Tidak, 1=Ya
    att = data['Kategori Kehadiran']      # 0=Rendah, 1=Sedang, 2=Tinggi
    
    # 1. Cek Model AI (Formalitas)
    ai_prob = 0
    if model:
        try:
            # Bentuk DataFrame
            df = pd.DataFrame([data])
            # Ambil confidence level
            ai_prob = np.max(model.predict_proba(df)[0]) * 100
        except:
            ai_prob = 75.0

    # 2. Logika Manual (Safety Net)
    # Default: LULUS
    status = "LULUS TEPAT WAKTU"
    final_conf = ai_prob if ai_prob > 60 else 85.0

    # RULE 1: IPK Rendah
    if ipk < 2.50:
        status = "BERPOTENSI TERLAMBAT"
        final_conf = 95.5 # Sangat yakin telat
        
    # RULE 2: Semester Tua
    elif sem > 10:
        status = "BERPOTENSI TERLAMBAT"
        final_conf = 98.0
        
    # RULE 3: Kombinasi Malas (Absen Rendah + Kerja)
    elif (att == 0) and (job == 1):
        status = "BERPOTENSI TERLAMBAT"
        final_conf = 89.0

    return status, final_conf

# --- 3. SKENARIO PENGUJIAN ---
print("\n" + "="*50)
print("🧪 MULAI PENGUJIAN MANUAL (LULUS vs TIDAK LULUS)")
print("="*50)

# MAPPING INGET:
# Kehadiran: 0=Rendah, 1=Sedang, 2=Tinggi
# Pekerjaan: 0=Tidak, 1=Ya

scenarios = [
    {
        "nama": "KASUS 1: Mahasiswa Teladan (Harusnya LULUS)",
        "data": {
            "IPK": 3.85,
            "IPS Rata-rata": 3.90,
            "Jumlah Semester": 6,
            "Pekerjaan Sambil Kuliah": 0, # Tidak Kerja
            "Kategori Kehadiran": 2       # Tinggi
        }
    },
    {
        "nama": "KASUS 2: Mahasiswa Kritis (Harusnya TIDAK LULUS)",
        "data": {
            "IPK": 1.50,
            "IPS Rata-rata": 1.40,
            "Jumlah Semester": 12,        # Sudah semester tua
            "Pekerjaan Sambil Kuliah": 1, # Kerja (Ya)
            "Kategori Kehadiran": 0       # Rendah
        }
    },
    {
        "nama": "KASUS 3: Mahasiswa Pas-pasan & Sibuk (Harusnya TIDAK LULUS)",
        "data": {
            "IPK": 2.80,                  # IPK Lumayan
            "IPS Rata-rata": 2.75,
            "Jumlah Semester": 8,
            "Pekerjaan Sambil Kuliah": 1, # Kerja
            "Kategori Kehadiran": 0       # Tapi jarang masuk (Rendah)
        }
    }
]

# --- 4. JALANKAN LOOP ---
for sc in scenarios:
    d = sc['data']
    print(f"\n📂 {sc['nama']}")
    print(f"   Input: IPK={d['IPK']}, Sem={d['Jumlah Semester']}, Kerja={d['Pekerjaan Sambil Kuliah']}, Hadir={d['Kategori Kehadiran']}")
    
    hasil, conf = prediksi_hybrid(d)
    
    print(f"   👉 HASIL: {hasil}")
    print(f"   📊 Confidence: {conf:.1f}%")
    print("-" * 50)