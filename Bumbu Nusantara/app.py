import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="RempahAI - Deteksi Bumbu Nusantara",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS ====================
st.markdown("""
<style>
    /* Font & reset */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Warna utama */
    :root {
        --primary: #2E7D32;
        --primary-light: #4CAF50;
        --primary-dark: #1B5E20;
        --secondary: #FF8F00;
        --bg-light: #F8F9FA;
        --card-white: #FFFFFF;
        --text-dark: #1E293B;
        --text-gray: #475569;
    }
    
    /* Sidebar premium - latar hijau gelap, teks putih kontras */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0F2B1D 0%, #1B5E20 100%);
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 500;
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 12px;
        transition: 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.15);
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 0.75rem;
    }
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] .stMarkdown p {
        color: rgba(255,255,255,0.85) !important;
    }
    
    /* Tombol modern */
    .stButton > button {
        background: linear-gradient(95deg, #2E7D32, #4CAF50);
        color: white !important;
        border: none;
        border-radius: 40px;
        padding: 0.5rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(46,125,50,0.3);
        background: linear-gradient(95deg, #1B5E20, #2E7D32);
    }
    
    /* Card glassmorphism */
    .glass-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-radius: 28px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.5);
        transition: all 0.3s;
        margin-bottom: 1.5rem;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 35px -12px rgba(0,0,0,0.15);
    }
    
    /* Hero header */
    .hero-header {
        background: linear-gradient(105deg, #1B5E20 0%, #2E7D32 50%, #4CAF50 100%);
        padding: 2rem;
        border-radius: 40px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    .hero-header h1, .hero-header p {
        color: white !important;
    }
    .hero-header::after {
        content: "🌿";
        font-size: 180px;
        position: absolute;
        bottom: -30px;
        right: -30px;
        opacity: 0.1;
        pointer-events: none;
    }
    
    /* Grid tim */
    .team-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
    }
    .team-item {
        background: white;
        border-radius: 20px;
        padding: 1rem 1.5rem;
        text-align: center;
        min-width: 140px;
        transition: 0.2s;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .team-item:hover {
        background: #F1F8E9;
        transform: scale(1.02);
        border-color: #4CAF50;
    }
    .team-name {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1B5E20;
    }
    .team-nim {
        font-size: 0.75rem;
        color: #475569;
        font-family: monospace;
    }
    
    /* Metric cards */
    .metric-modern {
        background: white;
        border-radius: 24px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-bottom: 3px solid #4CAF50;
    }
    .metric-number {
        font-size: 2.4rem;
        font-weight: 800;
        color: #2E7D32;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #475569;
        margin-top: 0.5rem;
    }
    
    /* Search bar */
    .search-wrapper input {
        border-radius: 60px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 0.7rem 1.5rem !important;
        font-size: 1rem !important;
        background: white !important;
        transition: 0.2s;
    }
    .search-wrapper input:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 3px rgba(76,175,80,0.2);
    }
    
    /* Rempah card */
    .rempah-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-left: 5px solid #4CAF50;
        transition: 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .rempah-card:hover {
        background: #F7FEF7;
        transform: translateX(4px);
        box-shadow: 0 6px 12px -6px rgba(0,0,0,0.1);
    }
    .rempah-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1B5E20;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Info badge */
    .info-badge {
        background: #E8F5E9;
        padding: 1rem 1.2rem;
        border-radius: 20px;
        color: #1B5E20;
        font-size: 0.9rem;
        border-left: 4px solid #2E7D32;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        font-size: 0.75rem;
        color: #64748B;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F8FAFC;
        border-radius: 30px;
        font-weight: 500;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        border-radius: 40px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }
    
    /* File uploader text */
    .stFileUploader label {
        color: #1E293B !important;
        font-weight: 500;
    }
    .stFileUploader .uploadedFileName {
        color: #1E293B !important;
    }
    
    /* Camera input label */
    .stCameraInput label {
        color: #1E293B !important;
    }
    
    /* Spinner text */
    .stSpinner > div {
        color: #2E7D32 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE REMPAH ====================
REMPAH_DB = {
    "Kluwek": "Biji buah keluarga pohon jati dengan cita rasa kuat dan sedikit pahit untuk rawon/soto.",
    "Wijen": "Biji kecil dengan rasa gurih, biasanya untuk topping atau olahan masakan Asia.",
    "Kemukus": "Lada tradisional dengan rasa pedas halus, sering untuk jamu.",
    "Saffron": "Benang merah bunga dengan aroma premium, untuk warna kuning emas dan aroma masakan.",
    "Serai": "Tanaman dengan aroma lemon segar, esensial untuk kari dan sup.",
    "Kemiri": "Biji keras untuk mengentalkan dan memperkaya rasa bumbu dasar.",
    "Lengkuas": "Rimpang dengan aroma khas dan rasa pedas getir untuk masakan bersantan.",
    "Kunyit": "Rimpang kuning keemasan, anti-inflamasi alami dan pewarna kuning masakan.",
    "Pala": "Biji dengan rasa hangat, manis, dan pedas untuk masakan daging atau kue.",
    "Vanili": "Polong dengan aroma manis khas, digunakan untuk dessert dan kue.",
    "Lada": "Bumbu universal dengan rasa pedas hangat yang kuat.",
    "Kencur": "Rimpang dengan rasa hangat dan aroma tajam untuk sambal atau jamu.",
    "Kayu Secang": "Kayu merah yang memberikan warna merah alami pada minuman.",
    "Kayu Manis": "Kulit pohon dengan aroma manis-hangat untuk masakan savory maupun manis.",
    "Kapulaga": "Biji dengan rasa campuran manis-pedas-mint, kunci aroma kari.",
    "Jinten": "Biji kecil dengan rasa hangat-pedas, khas untuk masakan berbumbu tajam.",
    "Daun Jeruk": "Daun dengan aroma jeruk segar yang tajam untuk menetralkan bau amis.",
    "Jahe": "Rimpang pedas hangat untuk menghangatkan tubuh dan bumbu masakan.",
    "Daun Ketumbar": "Daun dengan aroma segar unik, sering digunakan sebagai garnish.",
    "Daun Salam": "Daun dengan aroma harum lembut untuk menyedapkan nasi dan masakan.",
    "Biji Ketumbar": "Biji dengan rasa manis-pedas untuk bumbu dasar dan acar.",
    "Cengkeh": "Bunga kering dengan aroma sangat kuat untuk masakan daging/minuman.",
    "Bawang Merah": "Bumbu dasar utama dengan rasa manis tajam saat dimasak.",
    "Bawang Bombay": "Umbi besar dengan rasa manis saat dimasak, untuk volume masakan.",
    "Daun Kemangi": "Daun hijau dengan aroma harum khas untuk sambal atau lalapan.",
    "Asam Jawa": "Pasta buah dengan rasa asam kuat untuk menyeimbangkan rasa masakan.",
    "Bunga Lawang": "Bunga berbentuk bintang dengan aroma khas mirip licorice.",
    "Adas": "Biji dengan aroma manis untuk minuman herbal atau masakan.",
    "Bawang Putih": "Umbi dasar dengan rasa tajam dan aroma kuat saat digoreng.",
    "Andaliman": "Lada dengan sensasi menggelitik (kebas) khas masakan Sumatera.",
    "Temulawak": "Rimpang dengan rasa pahit-hangat, populer untuk jamu kesehatan."
}

@st.cache_resource
def load_model():
    return YOLO("best.pt")

def resize_image_for_inference(image, max_size=640):
    """Resize gambar agar cepat diproses model"""
    width, height = image.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    return image

def get_detection_info(results):
    detections = []
    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            name = results[0].names[cls]
            detections.append({"name": name, "confidence": conf})
    return detections

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1998/1998598.png", width=80)
    st.title("🌿 RempahAI")
    st.markdown("**Deteksi 31 rempah Nusantara**")
    st.markdown("---")
    menu = st.radio(
        "📌 Navigasi",
        ["🏠 Dashboard", "🔍 Deteksi Bumbu", "📖 Panduan Rempah"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("✨ Versi 2.0 • YOLOv8")

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":
    st.markdown("""
    <div class="hero-header">
        <h1>📦 Dashboard Deteksi Bumbu AI</h1>
        <p style="font-size:1.1rem; opacity:0.95;">Identifikasi rempah secara instan dengan kecerdasan buatan</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-modern">
            <div class="metric-number">31</div>
            <div class="metric-label">Jenis Rempah</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-modern">
            <div class="metric-number">YOLOv8</div>
            <div class="metric-label">Model AI</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-modern">
            <div class="metric-number">⚡ Real-time</div>
            <div class="metric-label">Deteksi Cepat</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👥 Tim Pengembang")
    
    tim = [
        ("Fauzan", "15240205", "👨‍🍳"),
        ("Alik", "15240008", "👩‍🍳"),
        ("Juan", "15240081", "🧑‍🍳"),
        ("Rama", "15240098", "👨‍🍳"),
        ("Dzakmal", "15240271", "👨‍🍳")
    ]
    
    cols = st.columns(len(tim))
    for idx, (nama, nim, emoji) in enumerate(tim):
        with cols[idx]:
            st.markdown(f"""
            <div class="team-item">
                <div style="font-size:2rem;">{emoji}</div>
                <div class="team-name">{nama}</div>
                <div class="team-nim">{nim}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-badge">
        🌟 <strong>Keunggulan Aplikasi</strong><br>
        • Model YOLO terlatih pada dataset rempah lokal<br>
        • Akurasi tinggi & deteksi multi-kelas<br>
        • Cocok untuk koki, peneliti, dan pecinta kuliner
    </div>
    """, unsafe_allow_html=True)

# ==================== DETEKSI ====================
elif menu == "🔍 Deteksi Bumbu":
    st.markdown("""
    <div class="hero-header">
        <h1>📸 Deteksi Bumbu Masak</h1>
        <p>Upload gambar atau foto langsung, AI akan mengenali rempahnya</p>
    </div>
    """, unsafe_allow_html=True)
    
    model = load_model()
    
    tab1, tab2 = st.tabs(["📁 Upload Gambar", "📱 Kamera Langsung"])
    
    file_gambar = None
    with tab1:
        file_gambar = st.file_uploader("Pilih foto (JPG/PNG)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    with tab2:
        file_gambar = st.camera_input("Ambil foto dengan kamera", label_visibility="collapsed")
    
    if file_gambar:
        col_img, col_res = st.columns(2, gap="medium")
        
        with col_img:
            st.markdown("##### 🖼️ Gambar Asli")
            img = Image.open(file_gambar).convert('RGB')
            st.image(img, use_column_width=True)
        
        with col_res:
            st.markdown("##### 🧠 Hasil Deteksi AI")
            # Resize gambar untuk percepatan
            img_resized = resize_image_for_inference(img, max_size=640)
            with st.spinner("⏳ Memproses gambar dengan model YOLO (gambar di-resize untuk kecepatan)..."):
                results = model(img_resized, imgsz=320)  # imgsz kecil untuk cepat
                detections = get_detection_info(results)
                plot_img = results[0].plot()
                st.image(plot_img, use_column_width=True, channels="BGR")
                
                if detections:
                    st.success(f"✅ Ditemukan {len(detections)} rempah")
                    for d in detections:
                        st.markdown(f"- 🌿 **{d['name']}** (keyakinan: {d['confidence']:.2%})")
                else:
                    st.info("Tidak ada rempah yang terdeteksi. Coba gambar lain dengan pencahayaan lebih baik.")
    else:
        st.markdown("""
        <div class="info-badge">
            💡 <strong>Tips optimal</strong><br>
            • Gunakan gambar dengan latar polos dan cahaya terang<br>
            • Pastikan rempah tidak tertutup objek lain<br>
            • Format yang didukung: JPG, PNG
        </div>
        """, unsafe_allow_html=True)

# ==================== PANDUAN REMPAH ====================
elif menu == "📖 Panduan Rempah":
    st.markdown("""
    <div class="hero-header">
        <h1>📚 Ensiklopedia Rempah Nusantara</h1>
        <p>Pelajari 31 jenis bumbu dapur tradisional Indonesia</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
    query = st.text_input("🔍 Cari rempah", placeholder="Contoh: jahe, kunyit, lada...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    daftar_rempah = sorted(REMPAH_DB.keys())
    if query:
        daftar_rempah = [nama for nama in daftar_rempah if query.lower() in nama.lower()]
    
    if not daftar_rempah:
        st.warning("Rempah tidak ditemukan. Coba kata kunci lain.")
    else:
        st.caption(f"Menampilkan {len(daftar_rempah)} dari {len(REMPAH_DB)} rempah")
        
        cols = st.columns(3)
        for idx, nama in enumerate(daftar_rempah):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="rempah-card">
                    <div class="rempah-title">
                        <span>🌿</span> {nama}
                    </div>
                    <div style="font-size:0.85rem; color:#334155; margin-top:0.5rem;">
                        {REMPAH_DB[nama][:110]}{'...' if len(REMPAH_DB[nama]) > 110 else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("📖 Detail selengkapnya"):
                    st.write(REMPAH_DB[nama])
                    st.caption("✨ Sering digunakan dalam masakan tradisional & jamu")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    © 2025 RempahAI — Deteksi Bumbu Cerdas | Dibangun dengan Streamlit & YOLOv8
</div>
""", unsafe_allow_html=True)
