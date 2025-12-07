import pandas as pd
import joblib # atau import pickle jika error
import numpy as np

# 1. Load Model
try:
    model = joblib.load('model_kelulusan_tanpa_gbm.pkl')
    print("✅ Model berhasil di-load!")
    print(f"Tipe Model: {type(model)}")
except Exception as e:
    print(f"❌ Gagal load model: {e}")
    exit()

# 2. Cek Fitur yang Diharapkan (Jika model support)
print("\n--- INFO FEATURES ---")
try:
    # Ini biasanya ada jika model ditraining pakai Scikit-Learn versi baru + Pandas
    if hasattr(model, 'feature_names_in_'):
        print("Model mengharapkan fitur dengan urutan berikut:")
        print(model.feature_names_in_)
    else:
        print("Model tidak menyimpan nama fitur secara eksplisit.")
        print(f"Tapi model mengharapkan input sebanyak: {model.n_features_in_} kolom")
except AttributeError:
    print("Tidak bisa membaca atribut fitur otomatis.")

# 3. Tes Prediksi Dummy
# Kita buat data dummy sesuai urutan feature_names yang kamu sebutkan:
# [IPK, IPS, Semester, Pekerjaan, Kehadiran]
# Asumsi: Pekerjaan & Kehadiran sudah dikonversi jadi angka (0,1,2..)
input_test = [[3.50, 3.40, 6, 0, 3]] 

print("\n--- TES PREDIKSI ---")
try:
    hasil = model.predict(input_test)
    print(f"Input: {input_test}")
    print(f"Hasil Prediksi (Raw): {hasil}")
    
    # Cek probabilitas (jika model support) untuk tahu seberapa yakin dia
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(input_test)
        print(f"Probabilitas: {proba}")
        
except Exception as e:
    print(f"❌ Error saat prediksi: {e}")
    print("Tips: Mungkin urutan kolom salah atau format data salah.")