import streamlit as st
import theme_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Panduan - PadiSense Premium",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Theme ───────────────────────────────────────────────────────
theme_utils.check_auth()
theme = theme_utils.THEMES[st.session_state.theme]
theme_utils.inject_theme("panduan")

# ─── Navbar ──────────────────────────────────────────────────────────────────
theme_utils.render_navbar("panduan")

# ─── Main Wrapper ─────────────────────────────────────────────────────────────
st.markdown('<div style="padding: 0 2.5rem 3rem; max-width: 1000px; margin: 0 auto;">', unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 2.5rem !important;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Panduan Penggunaan</h1>
    <p style="color: {theme['text_secondary']}; margin: 0; font-size: 1.05rem;">
        Pelajari langkah mudah menggunakan platform PadiSense untuk menganalisis dan menyembuhkan penyakit padi secara optimal.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Step 1 ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border-left: 5px solid {theme['primary']};">
    <h3 style="color: {theme['text']}; font-size: 1.4rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.6rem;">
        1️⃣ Siapkan Foto Daun Padi Terbaik
    </h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin-bottom: 0.8rem;">
        Ambil foto daun padi yang terkena gejala infeksi di tempat dengan pencahayaan yang cukup. Pastikan area bercak fokus dan tidak buram.
    </p>
    <ul style="color: {theme['text_secondary']}; margin-left: 1.8rem; line-height: 1.8; font-size: 0.92rem;">
        <li>📱 Gunakan kamera smartphone Anda dalam jarak dekat (Close-Up).</li>
        <li>💡 Ambil foto pada siang hari di bawah sinar matahari alami untuk menghindari distorsi warna.</li>
        <li>🎯 Format gambar yang didukung: JPG, JPEG, atau PNG.</li>
        <li>📐 Usahakan resolusi gambar minimal 640x480 piksel agar deteksi AI akurat.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─── Step 2 ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border-left: 5px solid {theme['gold']};">
    <h3 style="color: {theme['text']}; font-size: 1.4rem; margin-bottom: 0.8rem;">
        2️⃣ Unggah Foto di Dashboard
    </h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin: 0;">
        Buka halaman <strong>Beranda</strong>, lalu seret dan lepaskan file foto Anda atau klik tombol "Browse" pada panel di sebelah kiri untuk mengunggah gambar daun padi.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Step 3 ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border-left: 5px solid {theme['primary_light']};">
    <h3 style="color: {theme['text']}; font-size: 1.4rem; margin-bottom: 0.8rem;">
        3️⃣ Sesuaikan Slider Sensitivitas AI
    </h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin-bottom: 0.8rem;">
        Gunakan pengatur sensitivitas (Threshold) di bawah kolom unggah untuk menyesuaikan tingkat kepekaan model AI YOLOv8:
    </p>
    <ul style="color: {theme['text_secondary']}; margin-left: 1.8rem; line-height: 1.8; font-size: 0.92rem;">
        <li>🔴 <strong>Rendah (0.05 - 0.20):</strong> Sangat peka, cocok untuk mendeteksi gejala bercak halus/awal penyakit.</li>
        <li>🟡 <strong>Sedang (0.20 - 0.40):</strong> Tingkat optimal yang menyeimbangkan sensitivitas dan akurasi model.</li>
        <li>🟢 <strong>Tinggi (0.40 - 0.60):</strong> Hanya mendeteksi bercak penyakit yang sangat jelas dan kontras tinggi.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─── Step 4 ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border-left: 5px solid {theme['primary']};">
    <h3 style="color: {theme['text']}; font-size: 1.4rem; margin-bottom: 0.8rem;">
        4️⃣ Baca Hasil Laporan Analisis
    </h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin-bottom: 0.8rem;">
        AI akan secara otomatis menampilkan diagnosis kesehatan tanaman dengan rincian instan:
    </p>
    <ul style="color: {theme['text_secondary']}; margin-left: 1.8rem; line-height: 1.8; font-size: 0.92rem;">
        <li>🦠 Nama penyakit teridentifikasi lengkap dengan ikon status visual.</li>
        <li>📊 Skor keyakinan (Confidence level) dalam persen.</li>
        <li>📋 Penjelasan patogen, gejala bercak, dan dampaknya.</li>
        <li>📸 Gambar daun teranotasi dengan kotak pembatas (Bounding Box) untuk lokasi penyakit.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─── Step 5 ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border-left: 5px solid {theme['gold']};">
    <h3 style="color: {theme['text']}; font-size: 1.4rem; margin-bottom: 0.8rem;">
        5️⃣ Konsultasikan Penanganan dengan PadiBot
    </h3>
    <p style="color: {theme['text_secondary']}; line-height: 1.7; margin-bottom: 0.8rem;">
        Gunakan kotak obrolan (Chatbox) PadiBot di bagian bawah halaman untuk berdiskusi dengan asisten AI pintar pertanian:
    </p>
    <ul style="color: {theme['text_secondary']}; margin-left: 1.8rem; line-height: 1.8; font-size: 0.92rem;">
        <li>💡 Rekomendasi merek pestisida ramah lingkungan atau fungisida kimia.</li>
        <li>💊 Cara mencegah penyebaran infeksi ke tanaman sehat sekelilingnya.</li>
        <li>🌱 Pengaturan pemupukan seimbang (NPK) dan tata kelola irigasi sawah.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─── Tips Tambahan ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="background: linear-gradient(135deg, rgba(14, 24, 12, 0.8) 0%, rgba(46, 125, 50, 0.1) 100%) !important; border: 2px solid {theme['primary']} !important;">
    <h3 style="color: {theme['gold']}; font-size: 1.4rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;">
        💡 Tips Tambahan untuk Akurasi Maksimal
    </h3>
    <ul style="color: {theme['text_secondary']}; margin-left: 1.8rem; line-height: 1.8; font-size: 0.95rem;">
        <li>Pastikan kamera tidak goyang saat mengambil foto daun.</li>
        <li>Hindari bayangan tubuh Anda atau benda sekitar menutupi daun yang difoto.</li>
        <li>Jangan mengambil foto daun yang terlalu basah kuyup karena pantulan air bisa mengacaukan analisis visual AI.</li>
        <li>Jika ragu dengan satu diagnosis, cobalah ambil foto dari sudut berbeda untuk membandingkan hasil prediksi.</li>
    </ul>
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
