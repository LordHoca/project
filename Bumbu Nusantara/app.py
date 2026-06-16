import streamlit as st
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np

# Pengaturan Utama Halaman Streamlit
st.set_page_config(page_title="Deteksi Bumbu Nusantara", page_icon="🌿", layout="wide")

# ==================== KONTROL CSS KUSTOM (SERAGAM & FIXED SIZE) ====================
st.markdown("""
<style>
    /* Tema Dasar Dark Mode */
    [data-testid="stAppViewContainer"] { background-color: #0A0F16; color: #E2E8F0; }
    [data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1E293B; }
    
    /* Perataan Teks & Judul ke Tengah */
    h1, h2, h3 { text-align: center !important; color: #10B981 !important; }
    p, label { text-align: center !important; }
    
    /* Grid Tombol Utama */
    .stButton>button { 
        border-radius: 8px; 
        border: 1px solid #10B981; 
        color: #10B981; 
        transition: 0.3s; 
    }
    .stButton>button:hover { background-color: #10B981; color: white; }
    
    /* --- KOTAK DESKRIPSI DIKUNCI AGAR UKURANNYA SAMA RATA (ANTI-MELAR) --- */
    div[data-testid="stAlert"], div[data-testid="stNotification"], .stAlert {
        height: 150px !important;       /* Mengunci tinggi seluruh kotak bumbu secara absolut */
        min-height: 150px !important;
        max-height: 150px !important;
        overflow-y: auto !important;     /* Otomatis memunculkan scrollbar jika teks panjang */
        padding: 14px !important;
        border-radius: 10px !important;
    }
    
    /* Format teks di dalam kotak deskripsi agar rapi dan rata kiri */
    div[data-testid="stAlert"] p, div[data-testid="stNotification"] p {
        text-align: left !important;     
        margin-bottom: 4px !important;
    }
    
    /* Desain scrollbar internal tipis agar estetik */
    div[data-testid="stAlert"]::-webkit-scrollbar { width: 5px; }
    div[data-testid="stAlert"]::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 10px; }
    
    /* --- FORMAT TAMPILAN GAMBAR BERDAMPINGAN DAN TENGAH --- */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    [data-testid="stImage"] img {
        max-height: 320px !important;    /* Menjaga tinggi gambar seimbang */
        object-fit: contain !important;  
        border-radius: 12px;
        border: 2px solid #1E293B;
        margin: 0 auto !important;
    }
    
    .img-title {
        text-align: center;
        margin-bottom: 8px;
        font-size: 1.15rem;
        font-weight: bold;
        color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Memuat Model YOLO dengan Fitur Cache
@st.cache_resource
def load_model():
    return YOLO('best2.pt')

model = load_model()

# ==================== DATABASE LENGKAP 31 BUMBU NUSANTARA ====================
SPICE_DATA = {
    "adas": {"Manfaat": "Mengatasi kembung & gangguan pencernaan, serta membantu meredakan kolik.", "Penyimpanan": "Wadah kedap udara, simpan di tempat sejuk dan terlindung dari sinar matahari langsung.", "Tumbuh": "Dataran tinggi dengan iklim sejuk dan tanah yang gembur."},
    "andaliman": {"Manfaat": "Antioksidan tinggi, penambah getir khas masakan Batak, antimikroba alami.", "Penyimpanan": "Dalam freezer agar aroma dan kesegarannya tidak hilang.", "Tumbuh": "Dataran tinggi, tanah subur berhumus."},
    "asam-jawa": {"Manfaat": "Melancarkan pencernaan, meredakan demam, dan sebagai antiseptik alami.", "Penyimpanan": "Suhu ruang dalam wadah kering dan tertutup.", "Tumbuh": "Dataran rendah hingga menengah."},
    "bawang-bombay": {"Manfaat": "Menjaga kesehatan jantung, mengontrol kadar gula darah, dan menurunkan risiko kanker.", "Penyimpanan": "Tempat kering, terbuka dengan sirkulasi udara baik, jangan digabung dengan kentang.", "Tumbuh": "Iklim sedang hingga subtropis, membutuhkan intensitas cahaya matahari penuh."},
    "bawang-merah": {"Manfaat": "Menurunkan kadar kolesterol jahat, menjaga tekanan darah, dan kaya antioksidan.", "Penyimpanan": "Digantung di tempat kering, hindari tempat lembab atau kantong plastik tertutup.", "Tumbuh": "Dataran rendah, cuaca cenderung kering dan berangin."},
    "bawang-putih": {"Manfaat": "Antibiotik dan antibakteri alami, memperkuat imunitas tubuh, menurunkan tekanan darah.", "Penyimpanan": "Tempat kering yang gelap dengan sirkulasi baik agar tidak tumbuh tunas.", "Tumbuh": "Dataran tinggi dengan kondisi suhu udara cenderung dingin."},
    "biji-ketumbar": {"Manfaat": "Mengurangi peradangan, menurunkan kadar gula darah, meredakan nyeri sendi.", "Penyimpanan": "Wadah kaca tertutup rapat di tempat sejuk kering.", "Tumbuh": "Dataran rendah hingga menengah dengan paparan sinar matahari penuh."},
    "bunga-lawang": {"Manfaat": "Meredakan gejala flu & batuk, meningkatkan sirkulasi darah, menjaga kesehatan pencernaan.", "Penyimpanan": "Wadah kedap udara, jauhkan dari kelembaban.", "Tumbuh": "Kawasan tropis dan subtropis, dataran menengah."},
    "cengkeh": {"Manfaat": "Pereda alami untuk nyeri gigi, menjaga kesehatan hati, mengontrol kadar gula darah.", "Penyimpanan": "Tempat kering, sejuk, dan terhindar dari panas matahari langsung.", "Tumbuh": "Dataran menengah hingga tinggi dekat daerah pantai/kepulauan."},
    "daun-jeruk": {"Manfaat": "Aromaterapi penenang pikiran, mendetoksifikasi racun tubuh, menjaga kesehatan mulut.", "Penyimpanan": "Bungkus plastik kedap udara lalu simpan di dalam freezer.", "Tumbuh": "Dataran rendah hingga menengah, tanah berdrainase baik."},
    "daun-kemangi": {"Manfaat": "Menyegarkan aroma napas, meredakan stres, merawat kesehatan kulit.", "Penyimpanan": "Masukkan ke dalam wadah berisi sedikit air atau bungkus tisu di kulkas.", "Tumbuh": "Dataran rendah, cuaca panas dengan air yang cukup."},
    "daun-ketumbar": {"Manfaat": "Detoksifikasi zat logam berat dalam tubuh, menurunkan kecemasan, menyehatkan mata.", "Penyimpanan": "Dibalut kertas tisu kering lalu masukkan ke dalam kulkas.", "Tumbuh": "Dataran tinggi dengan kondisi tanah lembab dan subur."},
    "daun-salam": {"Manfaat": "Menurunkan kadar gula darah dan kolesterol, menjaga kesehatan jantung.", "Penyimpanan": "Keringkan daun secara alami, simpan dalam wadah kedap udara.", "Tumbuh": "Dataran rendah hingga area pegunungan setinggi 1500 mdpl."},
    "jahe": {"Manfaat": "Meredakan mual, mencegah mabuk perjalanan, serta memberikan efek kehangatan yang kuat pada seluruh tubuh setelah beraktivitas seharian.", "Penyimpanan": "Tempat sejuk kering terbuka, jangan dimasukkan ke dalam freezer atau kantong plastik basah.", "Tumbuh": "Dataran menengah, tanah gembur dengan sirkulasi udara yang baik."},
    "jinten": {"Manfaat": "Melancarkan metabolisme tubuh, meningkatkan imun, membantu manajemen berat badan.", "Penyimpanan": "Wadah kedap udara di tempat sejuk.", "Tumbuh": "Dataran rendah hingga menengah dengan kondisi tanah kering."},
    "kapulaga": {"Manfaat": "Mencegah bau mulut, mengontrol tekanan darah, menjaga kesehatan paru-paru.", "Penyimpanan": "Wadah kaca kedap udara agar aroma khasnya awet.", "Tumbuh": "Dataran menengah beriklim basah/lembab."},
    "kayu-manis": {"Manfaat": "Mengontrol gula darah, anti-inflamasi kuat, kaya akan antioksidan.", "Penyimpanan": "Tempat gelap, kering, dan sejuk dalam wadah tertutup.", "Tumbuh": "Dataran menengah ke atas beriklim lembab."},
    "kayu-secang": {"Manfaat": "Antioksidan penangkal radikal bebas, melegakan pernapasan dan radang tenggorokan.", "Penyimpanan": "Simpan serutan kayu di tempat kering.", "Tumbuh": "Dataran rendah hingga menengah, kondisi tanah kering berkelikir."},
    "kemiri": {"Manfaat": "Sumber lemak sehat, menjaga kekuatan rambut, meredakan diare.", "Penyimpanan": "Tempat kering, hindari area lembab agar tidak cepat berjamur.", "Tumbuh": "Dataran rendah hingga menengah di iklim tropis."},
    "kemukus": {"Manfaat": "Mengatasi asma, bronkitis, serta gangguan pernapasan lainnya.", "Penyimpanan": "Wadah kering kedap udara.", "Tumbuh": "Tropis, dataran menengah berpohon pelindung."},
    "kencur": {"Manfaat": "Meredakan batuk berdahak, mengatasi radang tenggorokan, serta menjadi penambah stamina tubuh yang sangat efektif secara alami.", "Penyimpanan": "Cukup letakkan di tempat kering pada suhu ruang terbuka dan hindari menyimpan di dalam kulkas.", "Tumbuh": "Dataran rendah hingga area pekarangan rumah berkapasitas ketinggian maksimal 1000 mdpl."},
    "kluwek": {"Manfaat": "Pengawet makanan alami, memiliki kandungan zat anti-bakteri, menurunkan kolesterol.", "Penyimpanan": "Tempat kering terbuka, jangan dikupas kulitnya sebelum dipakai.", "Tumbuh": "Daerah tropis, tanah basah dan lembab."},
    "kunyit": {"Manfaat": "Anti-inflamasi alami, menjaga kesehatan fungsi hati (liver), meringankan gejala maag.", "Penyimpanan": "Simpan di tempat kering terbuka atau dikubur dalam pasir bersih.", "Tumbuh": "Dataran rendah hingga menengah, wilayah tropis."},
    "lada": {"Manfaat": "Melancarkan sirkulasi darah, membantu menurunkan berat badan, meredakan hidung tersumbat.", "Penyimpanan": "Wadah kaca tertutup rapat di tempat gelap kering.", "Tumbuh": "Iklim tropis basah dengan kelembaban tinggi."},
    "lengkuas": {"Manfaat": "Agen antijamur dan antibakteri, meredakan radang sendi, menyehatkan lambung.", "Penyimpanan": "Dibalut dengan kertas koran/tisu, letakkan di suhu ruang.", "Tumbuh": "Tropis, dataran rendah dengan tanah gembur."},
    "pala": {"Manfaat": "Mengatasi insomnia (susah tidur), menenangkan sistem saraf, mendetoksifikasi tubuh.", "Penyimpanan": "Wadah kedap udara di tempat sejuk kering.", "Tumbuh": "Dataran rendah kepulauan, iklim panas lembab."},
    "saffron": {"Manfaat": "Antidepresan alami penenang suasana hati, meningkatkan memori, mengurangi gejala PMS.", "Penyimpanan": "Wadah kaca kecil kedap udara, simpan di tempat sangat kering.", "Tumbuh": "Iklim kering gersang, kawasan sub-tropis."},
    "serai": {"Manfaat": "Antioksidan penangkal kolesterol, relaksasi otot saraf, mengurangi kembung.", "Penyimpanan": "Simpan dalam kulkas setelah dibersihkan pangkalnya.", "Tumbuh": "Tropis, sangat adaptif di berbagai jenis tanah."},
    "temulawak": {"Manfaat": "Menjaga kesehatan fungsi hati (liver), menambah nafsu makan anak, antiradang.", "Penyimpanan": "Tempat kering sejuk pada suhu ruang.", "Tumbuh": "Dataran rendah hingga menengah, tanah gembur."},
    "vanili": {"Manfaat": "Menenangkan pikiran (efek relaksasi), menjaga kesehatan jantung, anti-inflamasi.", "Penyimpanan": "Wadah kaca kedap udara, lapisi kertas minyak, tempat gelap.", "Tumbuh": "Dataran menengah, iklim tropis basah/lembab."},
    "wijen": {"Manfaat": "Menjaga kekuatan tulang dan gigi, sumber protein nabati, menurunkan tekanan darah.", "Penyimpanan": "Wadah kedap udara, taruh di tempat sejuk kering.", "Tumbuh": "Dataran rendah, cuaca panas dengan curah hujan rendah."}
}

def predict_spices(image_pil):
    results = model.predict(source=image_pil, conf=0.25)
    res_plotted = results[0].plot()
    res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB) # Memastikan konversi warna agar gambar tidak biru
    res_image = Image.fromarray(res_rgb)
    detected = [model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]
    return res_image, detected

# Menu Navigasi Samping (Sidebar)
menu = st.sidebar.radio("Navigasi", ["📊 Dashboard", "🔍 Deteksi Bumbu", "📖 Ensiklopedia"])

# ==================== 1. MENU DASHBOARD ====================
if menu == "📊 Dashboard":
    st.title("🌿 Dashboard Bumbu Nusantara")
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Total Bumbu Terlatih", "31 Bumbu")
    with col_stat2:
        st.metric("Status Sistem", "Siap Digunakan")
        
    st.markdown("---")
    st.markdown("### 🗂️ Menu Daftar Bumbu Nusantara")
    st.info("Klik pada nama bumbu di bawah ini untuk melihat detail khasiat, penyimpanan, dan habitat tumbuhnya.")

    bumbu_list = sorted(SPICE_DATA.keys())
    kolom = st.columns(4)
    
    if "pilihan_dashboard" not in st.session_state:
        st.session_state.pilihan_dashboard = None

    for index, bumbu in enumerate(bumbu_list):
        nama_tombol = bumbu.replace("-", " ").title()
        with kolom[index % 4]:
            if st.button(nama_tombol, key=f"btn_{bumbu}", use_container_width=True):
                st.session_state.pilihan_dashboard = bumbu

    if st.session_state.pilihan_dashboard:
        selected_bumbu = st.session_state.pilihan_dashboard
        info = SPICE_DATA[selected_bumbu]
        nama_tampil = selected_bumbu.replace("-", " ").title()
        
        st.markdown("---")
        st.markdown(f"### 📋 Detail Informasi: {nama_tampil}")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.warning(f"**✨ Manfaat:**\n\n{info['Manfaat']}")
        with c2:
            st.info(f"**📦 Cara Penyimpanan:**\n\n{info['Penyimpanan']}")
        with c3:
            st.success(f"**🗺️ Habitat Tumbuh:**\n\n{info['Tumbuh']}")

# ==================== 2. MENU DETEKSI BUMBU (SIMETRIS BERDAMPINGAN) ====================
elif menu == "🔍 Deteksi Bumbu":
    st.title("🔍 Deteksi Bumbu")
    tab1, tab2 = st.tabs(["🖼️ Upload", "📸 Kamera"])
    
    # --- TAB 1: UPLOAD FOTO ---
    with tab1:
        file = st.file_uploader("Upload Foto Bumbu", type=["jpg", "png", "jpeg"])
        
        if file:
            image_pil = Image.open(file).convert('RGB')
            
            # Pratinjau awal tepat di tengah
            col_init1, col_init2, col_init3 = st.columns([1, 2, 1])
            with col_init2:
                st.markdown("<h3 class='img-title'>📷 Pratinjau Foto</h3>", unsafe_allow_html=True)
                st.image(image_pil)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Analisis Foto", key="btn_analisis_foto", use_container_width=True):
                with st.spinner("Menganalisis bumbu..."):
                    res, labels = predict_spices(image_pil)
                
                # RE-LAYOUT: POSISI BERDAMPINGAN HORIZONTAL PAS DI TENGAH
                st.markdown("<br>", unsafe_allow_html=True)
                col_u1, col_u2, col_u3, col_u4 = st.columns([0.5, 4, 4, 0.5])
                with col_u2:
                    st.markdown("<h3 class='img-title'>📷 Foto Asli</h3>", unsafe_allow_html=True)
                    st.image(image_pil)
                with col_u3:
                    st.markdown("<h3 class='img-title'>🎯 Hasil Deteksi</h3>", unsafe_allow_html=True)
                    st.image(res)
                
                st.markdown("<br>### 📋 Informasi Lengkap Bumbu Terdeteksi", unsafe_allow_html=True)
                if not labels:
                    st.warning("Tidak ada bumbu yang terdeteksi.")
                
                for l in set(labels):
                    key_label = l.lower().replace(" ", "-")
                    info = SPICE_DATA.get(key_label)
                    if info:
                        with st.expander(f"🌿 {l.replace('-', ' ').title()}", expanded=True):
                            det_c1, det_c2, det_c3 = st.columns(3)
                            with det_c1:
                                st.warning(f"**✨ Manfaat:**\n\n{info['Manfaat']}")
                            with det_c2:
                                st.info(f"**📦 Cara Penyimpanan:**\n\n{info['Penyimpanan']}")
                            with det_c3:
                                st.success(f"**🗺️ Habitat Tumbuh:**\n\n{info['Tumbuh']}")

    # --- TAB 2: KAMERA LIVE ---
    with tab2:
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            st.markdown("<h3 class='img-title'>📸 Kamera Live</h3>", unsafe_allow_html=True)
            cam = st.camera_input("Ambil Foto Bumbu", label_visibility="collapsed")
        
        if cam:
            image_pil = Image.open(cam).convert('RGB')
            with st.spinner("Menganalisis bumbu..."):
                res, labels = predict_spices(image_pil)
            
            # RE-LAYOUT KAMERA: BERDAMPINGAN HORIZONTAL PAS DI TENGAH
            st.markdown("<br>", unsafe_allow_html=True)
            col_cr1, col_cr2, col_cr3, col_cr4 = st.columns([0.5, 4, 4, 0.5])
            with col_cr2:
                st.markdown("<h3 class='img-title'>📷 Foto Asli</h3>", unsafe_allow_html=True)
                st.image(image_pil)
            with col_cr3:
                st.markdown("<h3 class='img-title'>🎯 Hasil Deteksi Kamera</h3>", unsafe_allow_html=True)
                st.image(res)
            
            st.markdown("---")
            st.markdown("### 📋 Informasi Lengkap Bumbu Terdeteksi")
            if not labels:
                st.warning("Tidak ada bumbu yang terdeteksi.")
                
            for l in set(labels):
                key_label = l.lower().replace(" ", "-")
                info = SPICE_DATA.get(key_label)
                
                if info:
                    with st.expander(f"🌿 {l.replace('-', ' ').title()}", expanded=True):
                        det_c1, det_c2, det_c3 = st.columns(3)
                        with det_c1:
                            st.warning(f"**✨ Manfaat:**\n\n{info['Manfaat']}")
                        with det_c2:
                            st.info(f"**📦 Cara Penyimpanan:**\n\n{info['Penyimpanan']}")
                        with det_c3:
                            st.success(f"**🗺️ Habitat Tumbuh:**\n\n{info['Tumbuh']}")

# ==================== 3. MENU ENSIKLOPEDIA ====================
elif menu == "📖 Ensiklopedia":
    st.title("📖 Ensiklopedia Bumbu Nusantara")
    
    col_ens1, col_ens2, col_ens3 = st.columns([1, 2, 1])
    with col_ens2:
        pilihan = st.selectbox("Pilih Bumbu", sorted(SPICE_DATA.keys()))
        
    if pilihan:
        info = SPICE_DATA[pilihan]
        nama_tampil = pilihan.replace("-", " ").title()
        
        st.markdown(f"<h2>{nama_tampil}</h2>", unsafe_allow_html=True)
        
        c_ens1, c_ens2, c_ens3 = st.columns(3)
        with c_ens1:
            st.warning(f"**✨ Manfaat:**\n\n{info['Manfaat']}")
        with c_ens2:
            st.info(f"**📦 Cara Penyimpanan:**\n\n{info['Penyimpanan']}")
        with c_ens3:
            st.success(f"**🗺️ Habitat Tumbuh:**\n\n{info['Tumbuh']}")
