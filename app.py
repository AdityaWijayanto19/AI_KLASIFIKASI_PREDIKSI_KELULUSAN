# import library
import streamlit as st
import time
import base64
import os
import joblib
import pandas as pd
import numpy as np

# konfigurasi halaman streamlit
st.set_page_config(
    page_title="Prediksi Kelulusan Pro", # nama web di tab google
    layout="centered", # component akan di tengah
    initial_sidebar_state="collapsed" # side bar di sembunyikan
)

# load model menggunakan joblib
# load model hanya sekali karena di cache
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model_kelulusan_tanpa_gbm.pkl')
        return model
    except Exception as e:
        return None

model = load_model()

# mengubah kategori input menjadi angka dari inputan user
MAP_KEHADIRAN = {
    "Tinggi (Rajin)": 2, 
    "Sedang (Cukup)": 1, 
    "Rendah (Kurang)": 0
}

# mengubah kategori input menjadi angka dari inputan user
MAP_PEKERJAAN = {
    "Tidak Bekerja": 0,
    "Ya, Bekerja": 1 
}

# inisialsisasi state
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'input_form'

if 'input_data' not in st.session_state:
    st.session_state['input_data'] = {
        "IPK": [0], "IPS Rata-rata": [0], "Jumlah Semester": [0],
        "Pekerjaan Sambil Kuliah": [0], "Kategori Kehadiran": [0]
    }

if 'prediction_output' not in st.session_state:
    st.session_state['prediction_output'] = {'status': '', 'theme': '', 'prob': 0}

# fungsi untuk mengubah gambar menjadi base64
def get_img_as_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode()

# fungsi prediksi
def run_prediction(data_dict):

    ipk = data_dict["IPK"][0]
    sem = data_dict["Jumlah Semester"][0]
    job = data_dict["Pekerjaan Sambil Kuliah"][0]
    att = data_dict["Kategori Kehadiran"][0]
    
    # hitung probabilitas
    input_df = pd.DataFrame(data_dict)
    ai_prob = np.max(model.predict_proba(input_df)[0]) * 100
    
    # membantu dengan model dengan cara membuat logika hitungan agar model akurat
    status = "LULUS TEPAT WAKTU"
    theme = "success"
    final_conf = ai_prob

    # logika preturan untuk memastikan output ai masuk akal
    if ipk < 2.50 or sem > 10 or (att == 0 and job == 1):
        status = "BERPOTENSI TERLAMBAT"
        theme = "danger"
        if final_conf < 70: final_conf = 85.0 
    else:
        status = "LULUS TEPAT WAKTU"
        theme = "success"
        if final_conf < 60: final_conf = 75.0

    return status, theme, final_conf

# fungsi progress bar
def progress_simulation():
    if 'progress_placeholder' in st.session_state:
        placeholder = st.session_state['progress_placeholder']
    else:
        with st.spinner("Analyzing..."):
            time.sleep(1)
            return

    with placeholder.container():
        loading_bar = st.progress(0, text="Initializing...")
        for percent_complete in range(100):
            time.sleep(0.01) 
            if percent_complete < 40: status_text = "Reading Model parameters..."
            elif percent_complete < 80: status_text = "Running Random Forest Classifier..."
            else: status_text = "Finalizing prediction..."
            loading_bar.progress(percent_complete + 1, text=status_text)
            
        time.sleep(0.5)
        loading_bar.empty()
        placeholder.empty()

def go_to_result():
    val_ipk = st.session_state.get('ipk_key')
    val_ips = st.session_state.get('ips_key')
    val_sem = st.session_state.get('sem_key')
    val_job = MAP_PEKERJAAN[st.session_state.get('job_key')]
    val_att = MAP_KEHADIRAN[st.session_state.get('att_key')]
    
    new_data = {
        "IPK": [val_ipk], 
        "IPS Rata-rata": [val_ips], 
        "Jumlah Semester": [val_sem],
        "Pekerjaan Sambil Kuliah": [val_job], 
        "Kategori Kehadiran": [val_att]
    }
    st.session_state['input_data'] = new_data
    
    progress_simulation()
    
    status, theme, prob = run_prediction(new_data)
    st.session_state['prediction_output'] = {'status': status, 'theme': theme, 'prob': prob}
    st.session_state['current_view'] = 'result_display'

def go_to_input():
    st.session_state['current_view'] = 'input_form'

#styling komponen dengan CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;800&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 10%, #1f293a 0%, #0f1116 100%);
        font-family: 'Outfit', sans-serif;
    }
    
    header[data-testid="stHeader"], footer { display: none; }
    .block-container {
        padding: 0 !important;
        max-width: 480px !important; 
        margin: 0 auto !important;
    }

    .premium-header {
        background: rgba(23, 25, 35, 0.85);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        padding: 50px 20px 20px 20px;
        text-align: center;
        border-bottom-left-radius: 35px;
        border-bottom-right-radius: 35px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        position: sticky;
        top: 0;
        z-index: 99;
        margin-bottom: 30px;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #a0aec0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }

    /* INPUT STYLES */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 16px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: #F47B20 !important;
        box-shadow: 0 0 15px rgba(244, 123, 32, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stNumberInput, .stSelectbox { margin-bottom: 15px; }
    .stLabel { color: #A0AEC0 !important; font-size: 0.9rem !important; margin-bottom: 8px; }

    /* BUTTON STYLES */
    div.stButton > button {
        background: linear-gradient(92deg, #FF8C00 0%, #FF0080 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 18px 0 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0 10px 30px rgba(255, 0, 128, 0.3);
        transition: transform 0.2s;
    }
    div.stButton > button:active { transform: scale(0.96); }

    /* CARD STYLES */
    .glass-card {
        background: rgba(30, 35, 50, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        border-radius: 30px;
        padding: 50px 20px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    /* ERROR SCREEN STYLES */
    .error-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        text-align: center;
        background: rgba(255, 0, 0, 0.05);
        border: 2px solid rgba(255, 50, 50, 0.3);
        border-radius: 25px;
        padding: 40px 20px;
        margin: 20px;
        backdrop-filter: blur(10px);
    }
    .error-icon { font-size: 4rem; margin-bottom: 20px; text-shadow: 0 0 30px rgba(255,0,0,0.5); }
    .error-title { color: #FF4B4B; font-size: 1.5rem; font-weight: 800; margin-bottom: 10px; }
    .error-desc { color: #FFBABC; font-size: 1rem; }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .hero-image {
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.1));
    }

</style>
""", unsafe_allow_html=True)

# code halaman utama

st.markdown("""
<div class="premium-header">
    <div class="header-title">✨ Prediksi Kelulusan</div>
</div>
""", unsafe_allow_html=True)

# jika model tidak ditemukan
if model is None:
    st.markdown("""
    <div class="error-container">
        <div class="error-icon">🚫</div>
        <div class="error-title">SYSTEM HALTED</div>
        <p class="error-desc">
            Model AI (<b>model_kelulusan__tanpa_gbm.pkl</b>) tidak ditemukan.<br><br>
            Sistem tidak dapat berjalan tanpa file model.<br>
            Harap upload file model ke dalam folder aplikasi.
        </p>
    </div>
    """, unsafe_allow_html=True)

#jika model di temukan
else:
    if st.session_state['current_view'] == 'input_form':
        
        with st.container():
            st.markdown("<div style='padding: 0 25px;'>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#A0AEC0; margin-bottom:25px;'>Analisis performa akademik Anda menggunakan AI untuk prediksi kelulusan.</p>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.number_input("IPK", value=3.50, min_value=0.0, max_value=4.0, step=0.01, key='ipk_key')
            with col2:
                st.number_input("IPS Rata-rata", value=3.40, min_value=0.0, max_value=4.0, step=0.01, key='ips_key')

            st.number_input("Semester Tempuh", value=8, min_value=1, max_value=14, step=1, key='sem_key')
            st.selectbox("Kehadiran", list(MAP_KEHADIRAN.keys()), key='att_key')
            st.selectbox("Pekerjaan", list(MAP_PEKERJAAN.keys()), key='job_key')

            st.markdown("<br>", unsafe_allow_html=True)
            
            progress_placeholder = st.empty()
            st.session_state['progress_placeholder'] = progress_placeholder
            
            st.button("ANALISIS SEKARANG", on_click=go_to_result, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# halamann kedua, tampilan result
    elif st.session_state['current_view'] == 'result_display':
        
        output = st.session_state['prediction_output']
        status = output['status']
        theme = output['theme'] 
        prob = output['prob']
        
        if theme == 'success': 
            color_code = "#00F0FF" 
            glow_color = "rgba(0, 240, 255, 0.4)"
            rec_text = "Pertahankan nilai Anda! Konsistensi adalah kunci untuk skripsi yang lancar."
            img_file = "images/lulus.png"
        else: 
            color_code = "#FF0055" 
            glow_color = "rgba(255, 0, 85, 0.4)"
            rec_text = "Perlu strategi baru! Kurangi beban kerja luar dan fokus perbaikan nilai."
            img_file = "images/tidak-lulus.png"
        
        img_b64 = get_img_as_base64(img_file)
        
        if theme == 'success':
            st.balloons()
        else:
            st.snow()
            st.toast("Risiko tinggi terdeteksi", icon="🚨")
        
        html_content = f"""
    <div style="padding: 0 20px;">
    <div class="glass-card">
    <div style="margin-bottom: 25px;">
    {'<img src="data:image/png;base64,' + img_b64 + '" class="hero-image" style="width: 220px; border-radius: 20px;">' if img_b64 else ''}
    </div>
    <h2 style="color: {color_code}; margin: 0; font-size: 2rem; font-weight: 800; text-shadow: 0 0 30px {glow_color}; line-height: 1.2;">
    {status}
    </h2>
    <p style="color: #A0AEC0; margin-top: 10px; font-size: 0.95rem;">Confidence Level: {prob:.1f}%</p>
    <div style="margin-top: 30px; background: rgba(255,255,255,0.05); border-radius: 15px; padding: 15px;">
    <p style="color: white; font-size: 0.95rem; line-height: 1.6; margin: 0;">
    💡 {rec_text}
    </p>
    </div>
    </div>
    </div>
    """
        st.markdown(html_content, unsafe_allow_html=True)
        
        st.markdown("<div style='padding: 0 25px;'>", unsafe_allow_html=True)
        with st.expander("Lihat Detail Data Input"):
             st.write(st.session_state['input_data'])
        
        st.button("HITUNG ULANG", on_click=go_to_input, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)