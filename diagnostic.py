import joblib
import pandas as pd
import itertools

# LOAD MODEL
model = joblib.load('model_kelulusan_tanpa_gbm.pkl')
print("🕵️‍♂️ SEDANG MENCARI KOMBINASI INPUT AGAR HASILNYA BEDA...")

# Kita coba variasi angka input untuk kategori (0 sampai 4)
# Karena kita tidak tahu temanmu pakai angka berapa.
range_angka = [0, 1, 2, 3, 4]

# Skenario IPK Rendah (Harusnya Tidak Lulus/Telat)
base_data = {
    'IPK': [1.0], 
    'IPS Rata-rata': [1.0], 
    'Jumlah Semester': [12], # Semester tua
    # Kita akan ubah-ubah Pekerjaan dan Kehadiran
}

found_diff = False

# Loop kombinasi Pekerjaan & Kehadiran
for job in range_angka:
    for att in range_angka:
        df = pd.DataFrame(base_data)
        df['Pekerjaan Sambil Kuliah'] = job
        df['Kategori Kehadiran'] = att
        
        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0]
        
        # Jika ketemu prediksi yang nilainya 1 (Atau apapun selain 0)
        if pred != 0:
            print(f"\n✅ KETEMU! Model memberikan respon beda (Output {pred}) pada:")
            print(f"   -> Pekerjaan Input Angka : {job}")
            print(f"   -> Kehadiran Input Angka : {att}")
            print(f"   -> Probabilitas: {proba}")
            found_diff = True
        
if not found_diff:
    print("\n❌ GAGAL. Model ini 'keras kepala'.")
    print("Semua kombinasi angka (0-4) pada IPK 1.0 tetap diprediksi sebagai '0'.")
    print("Kemungkinan model temanmu Overfitting (Bias ke satu jawaban saja) atau rusak.")