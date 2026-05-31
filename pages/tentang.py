import streamlit as st
import theme_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tentang - PadiSense Premium",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Theme ───────────────────────────────────────────────────────
theme_utils.check_auth()
theme = theme_utils.THEMES[st.session_state.theme]
theme_utils.inject_theme("tentang")

# ─── Navbar ──────────────────────────────────────────────────────────────────
theme_utils.render_navbar("tentang")

# ─── Main Wrapper ─────────────────────────────────────────────────────────────
st.markdown('<div style="padding: 0 2.5rem 3rem; max-width: 1100px; margin: 0 auto;">', unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 2.5rem !important;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Tentang PadiSense</h1>
    <p style="color: {theme['text_secondary']}; margin: 0; font-size: 1.05rem;">
        Menyingkap misi kami dalam memadukan teknologi kecerdasan buatan terdepan demi kemakmuran tani Nusantara.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Apa itu PadiSense ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="background: linear-gradient(135deg, rgba(14, 24, 12, 0.8) 0%, rgba(46, 125, 50, 0.1) 100%) !important;">
    <h3 style="color: {theme['text']}; font-size: 1.5rem; margin-bottom: 1rem;">🌾 Apa itu PadiSense?</h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.8; font-size: 1.05rem; margin: 0;">
        <strong>PadiSense</strong> adalah aplikasi agro-teknologi berbasis kecerdasan buatan (Artificial Intelligence) yang dirancang khusus untuk mendeteksi penyakit daun tanaman padi secara instan.
        Melalui kamera smartphone, PadiSense menganalisis foto daun padi secara presisi menggunakan model deep learning <strong>YOLOv8</strong>, mengklasifikasikan jenis penyakit, dan menyuguhkan rekomendasi solusi dari asisten pakar <strong>PadiBot</strong> berbasis Gemini AI.
    </p>
    <div style="margin-top: 1.2rem; padding: 0.8rem 1.2rem; background: rgba(46,125,50,0.1); border-radius: 10px; border-left: 4px solid {theme['gold']};">
        <span style="color: {theme['gold']}; font-style: italic;">
            💡 Moto Kami: "From Leaf to Insight - Dari Dedaunan menuju Kemakmuran Pangan"
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Visi & Misi ─────────────────────────────────────────────────────────────
col_vis, col_mis = st.columns(2, gap="large")

with col_vis:
    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <h3 style="color: {theme['gold']}; margin-bottom: 0.8rem;">🎯 Visi Luhur</h3>
        <p style="color: {theme['text_secondary']}; line-height: 1.7; margin: 0; font-size: 0.98rem;">
            Menjadi pelopor digitalisasi pertanian padi nasional yang andal dan terjangkau bagi jutaan petani di seluruh kepulauan Indonesia guna memperkuat kedaulatan pangan bangsa.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_mis:
    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <h3 style="color: {theme['primary_light']}; margin-bottom: 0.8rem;">⚡ Misi Utama</h3>
        <p style="color: {theme['text_secondary']}; line-height: 1.7; margin: 0; font-size: 0.98rem;">
            Menghadirkan solusi diagnosa kesehatan padi yang cepat, akurat, dan mudah dipahami, serta mempersempit kesenjangan pengetahuan agronomi melalui asisten cerdas PadiBot.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Statistik Model ─────────────────────────────────────────────────────────
col_st1, col_st2, col_st3, col_st4 = st.columns(4, gap="medium")

with col_st1:
    st.markdown("""
    <div class="stat-badge">
        <div class="stat-badge-value">9 Jenis</div>
        <div class="stat-badge-label">Penyakit Terlatih</div>
    </div>
    """, unsafe_allow_html=True)

with col_st2:
    st.markdown("""
    <div class="stat-badge">
        <div class="stat-badge-value">63.4%</div>
        <div class="stat-badge-label">Akurasi Model</div>
    </div>
    """, unsafe_allow_html=True)

with col_st3:
    st.markdown("""
    <div class="stat-badge">
        <div class="stat-badge-value">8.660+</div>
        <div class="stat-badge-label">Data Training</div>
    </div>
    """, unsafe_allow_html=True)

with col_st4:
    st.markdown("""
    <div class="stat-badge">
        <div class="stat-badge-value">YOLOv8n</div>
        <div class="stat-badge-label">Arsitektur AI</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Teknologi & Data ─────────────────────────────────────────────────────────
col_tech, col_data = st.columns(2, gap="large")

with col_tech:
    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <h3 style="color: {theme['gold']}; margin-bottom: 1rem; border-bottom: 2px solid {theme['border']}; padding-bottom: 0.5rem;">🔬 Teknologi Penggerak</h3>
        <ul style="color: {theme['text_secondary']}; margin-left: 1.5rem; line-height: 1.8; font-size: 0.95rem;">
            <li><strong>Model Deteksi:</strong> YOLOv8 (You Only Look Once) untuk deteksi objek real-time.</li>
            <li><strong>Computer Vision:</strong> Image processing kustom untuk penajaman gambar.</li>
            <li><strong>Large Language Model:</strong> Gemini 2.5 Flash dari Google untuk PadiBot.</li>
            <li><strong>Framework Utama:</strong> Streamlit untuk performa aplikasi web yang responsif.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_data:
    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <h3 style="color: {theme['primary_light']}; margin-bottom: 1rem; border-bottom: 2px solid {theme['border']}; padding-bottom: 0.5rem;">📊 Data Latihan Model</h3>
        <ul style="color: {theme['text_secondary']}; margin-left: 1.5rem; line-height: 1.8; font-size: 0.95rem;">
            <li><strong>Sumber:</strong> Rice Leaf Diseases Dataset (Repositori Kaggle Terbuka).</li>
            <li><strong>Jumlah Foto:</strong> Sekitar 8.660+ dokumentasi kondisi daun padi.</li>
            <li><strong>Pembagian Data:</strong> 80% data latih (training), 20% data validasi.</li>
            <li><strong>Penyakit Sasaran:</strong> 9 kategori penyakit dan kondisi daun sehat.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Penyakit yang Dideteksi ─────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card">
    <h3 style="color: {theme['text']}; margin-bottom: 1.2rem;">🦠 Penyakit yang Mampu Dideteksi</h3>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; font-size: 0.95rem; color: {theme['text_secondary']};">
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">✅ Daun Sehat (Healthy)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">🦠 Hawar Daun Bakteri (Blight)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">🟤 Bercak Coklat (Brown Spot)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">🐛 Hama Kumbang (Hispa)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">⚡ Blast Daun (Leaf Blast)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">🔥 Gosong Daun (Scald)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">⬛ Gosong Palsu (Smut)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">📍 Bercak Sempit (Narrow Spot)</div>
        <div style="padding: 0.8rem; background: rgba(46,125,50,0.1); border-radius: 8px; border-left: 4px solid {theme['primary']};">🚨 Blast Leher Malai (Neck Blast)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tim Pengembang ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card">
    <h3 style="color: {theme['gold']}; margin-bottom: 0.8rem;">👥 Tim Pengembang PadiSense</h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin: 0; font-size: 0.95rem;">
        Dibuat penuh dedikasi oleh para mahasiswa program <strong>Data Science &amp; Generative AI</strong> pada platform <strong>CAMP Batch 4 tahun 2026</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Disclaimer ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border: 1px solid rgba(249, 168, 37, 0.4) !important; background: linear-gradient(135deg, rgba(14, 24, 12, 0.8) 0%, rgba(249, 168, 37, 0.05) 100%) !important;">
    <h3 style="color: {theme['gold']}; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;">
        📝 Pernyataan Batasan Tanggung Jawab (Disclaimer)
    </h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin: 0; font-size: 0.95rem;">
        PadiSense didesain murni sebagai asisten deteksi awal berbasis vision-AI dan saran pakar obrolan. Aplikasi ini bukan pengganti mutlak atas inspeksi fisik langsung dari penyuluh lapangan bersertifikat maupun lembaga dinas pertanian resmi. Kami sangat menganjurkan petani untuk mendiskusikan hasil analisis dengan dinas pertanian setempat guna rencana pengobatan masif sawah Anda.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align: center; padding: 4rem 0 2rem; border-top: 1px solid {theme['border']}; color: {theme['text_muted']}; font-size: 0.9rem;">
    🌾 <strong>PadiSense Premium v1.2</strong> | Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity: 0.65; font-size: 0.8rem;">© 2026 CAMP Batch 4 | Data Science &amp; Generative AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
