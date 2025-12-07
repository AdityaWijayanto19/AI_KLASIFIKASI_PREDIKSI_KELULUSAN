import joblib

feature_names = [
    "IPK",
    "IPS Rata-rata",
    "Jumlah Semester",
    "Pekerjaan Sambil Kuliah",
    "Kategori Kehadiran"
]

joblib.dump(feature_names, "feature_names.pkl")
print("feature_names.pkl dibuat!")
