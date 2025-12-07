import streamlit as st
import time
import base64
import os

# --- 1. SETUP & KONFIGURASI ---
st.set_page_config(
    page_title="Prediksi Kelulusan Pro",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MAPPING DATA ---
MAP_KEHADIRAN = {"Excellent": 3, "Good": 2, "Average": 1, "Poor": 0}
MAP_PEKERJAAN = {"Tidak Bekerja": 0, "Paruh Waktu": 1, "Penuh Waktu": 2}

# --- STATE MANAGEMENT ---
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'input_form'

if 'input_data' not in st.session_state:
    st.session_state['input_data'] = {
        "IPK": [3.50], "IPS Rata-rata": [3.40], "Jumlah Semester": [6],
        "Pekerjaan Sambil Kuliah": [0], "Kategori Kehadiran": [3]
    }

if 'prediction_output' not in st.session_state:
    st.session_state['prediction_output'] = {'status': 'LULUS TEPAT WAKTU', 'theme': 'success'}

# --- HELPER FUNCTIONS ---
def get_img_as_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode()

def run_prediction_logic(data_dict):
    ipk = data_dict["IPK"][0]
    kehadiran = data_dict["Kategori Kehadiran"][0]
    
    # Contoh Logika
    if ipk >= 3.0 and kehadiran >= 2:
        return "LULUS TEPAT WAKTU", "success"
    else:
        return "BERPOTENSI TERLAMBAT", "danger"

# --- FUNGSI PROGRESS BAR ---
def progress_simulation():
    if 'progress_placeholder' in st.session_state:
        placeholder = st.session_state['progress_placeholder']
    else:
        with st.spinner("Analyzing..."):
            time.sleep(1)
            return

    with placeholder.container():
        loading_bar = st.progress(0, text="Initializing model...")
        for percent_complete in range(100):
            time.sleep(0.015) 
            if percent_complete < 20: status_text = "Loading input data..."
            elif percent_complete < 50: status_text = "Preprocessing data features..."
            elif percent_complete < 85: status_text = "Running AI algorithm..."
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
        "IPK": [val_ipk], "IPS Rata-rata": [val_ips], "Jumlah Semester": [val_sem],
        "Pekerjaan Sambil Kuliah": [val_job], "Kategori Kehadiran": [val_att]
    }
    st.session_state['input_data'] = new_data
    
    progress_simulation()
    
    status, theme = run_prediction_logic(new_data)
    st.session_state['prediction_output'] = {'status': status, 'theme': theme}
    st.session_state['current_view'] = 'result_display'

def go_to_input():
    st.session_state['current_view'] = 'input_form'

# -----------------------------------------------------------------------------
# 2. PREMIUM CSS
# -----------------------------------------------------------------------------
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

    div[data-testid="stProgress"] > div > div > div > div {
        background-image: linear-gradient(to right, #F47B20, #FF0080);
    }
    div[data-testid="stProgress"] > div > div > p {
        color: #A0AEC0 !important;
        font-size: 0.85rem !important;
    }

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

# -----------------------------------------------------------------------------
# 3. UI LAYOUT
# -----------------------------------------------------------------------------

st.markdown("""
<div class="premium-header">
    <div class="header-title">✨ Prediksi Kelulusan</div>
</div>
""", unsafe_allow_html=True)


if st.session_state['current_view'] == 'input_form':
    
    with st.container():
        st.markdown("<div style='padding: 0 25px;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#A0AEC0; margin-bottom:25px;'>Analisis performa akademik Anda menggunakan AI untuk prediksi kelulusan.</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.number_input("IPK", value=3.50, min_value=0.0, max_value=4.0, step=0.01, key='ipk_key')
        with col2:
            st.number_input("IPS Rata-rata", value=3.40, min_value=0.0, max_value=4.0, step=0.01, key='ips_key')

        st.number_input("Semester Tempuh", value=6, min_value=1, max_value=14, step=1, key='sem_key')
        st.selectbox("Kehadiran", list(MAP_KEHADIRAN.keys()), key='att_key')
        st.selectbox("Pekerjaan", list(MAP_PEKERJAAN.keys()), key='job_key')

        st.markdown("<br>", unsafe_allow_html=True)
        
        progress_placeholder = st.empty()
        st.session_state['progress_placeholder'] = progress_placeholder
        
        st.button("🚀  ANALISIS SEKARANG", on_click=go_to_result, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


elif st.session_state['current_view'] == 'result_display':
    
    output = st.session_state['prediction_output']
    status = output['status']
    theme = output['theme'] 
    
    if theme == 'success': 
        color_code = "#00F0FF" 
        glow_color = "rgba(0, 240, 255, 0.4)"
        rec_text = "Pertahankan nilai Anda! Konsistensi adalah kunci untuk skripsi yang lancar."
    else: 
        color_code = "#FF0055" 
        glow_color = "rgba(255, 0, 85, 0.4)"
        rec_text = "Perlu strategi baru! Kurangi beban kerja luar dan fokus perbaikan nilai."
    
    img_file = "images/lulus.png" if theme != 'danger' else "images/tidak-lulus.png"
    img_b64 = get_img_as_base64(img_file)
    
    if theme == 'success':
        st.balloons()
    
    # --- HTML STRING FIX (Rata Kiri Total) ---
    # Perhatikan: Bagian HTML ini TIDAK di-indentasi untuk mencegah isu blok kode
    html_content = f"""
<div style="padding: 0 20px;">
<div class="glass-card">
<div style="margin-bottom: 25px;">
{'<img src="data:image/png;base64,' + img_b64 + '" class="hero-image" style="width: 220px; border-radius: 20px;">' if img_b64 else ''}
</div>
<h2 style="color: {color_code}; margin: 0; font-size: 2rem; font-weight: 800; text-shadow: 0 0 30px {glow_color}; line-height: 1.2;">
{status}
</h2>
<p style="color: #A0AEC0; margin-top: 10px; font-size: 0.95rem;">Hasil Prediksi AI</p>
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
    with st.expander("🔍  Lihat Detail Data Input"):
         st.write(st.session_state['input_data'])
    
    st.button("🔄  HITUNG ULANG", on_click=go_to_input, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)