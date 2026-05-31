import streamlit as st
import theme_utils
import base64
from io import BytesIO
from PIL import Image

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Profil - PadiSense Premium",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Session Setup ──────────────────────────────────────────────
theme_utils.check_auth()

# ─── Theme Loading ───────────────────────────────────────────────────────────
theme = theme_utils.THEMES[st.session_state.theme]
theme_utils.inject_theme("profil")

# ─── Render Floating Header/Navbar ───────────────────────────────────────────
theme_utils.render_navbar("profil")

# ─── Main Page Content Wrapper ───────────────────────────────────────────────
st.markdown('<div style="padding: 0 2.5rem 3rem; max-width: 1100px; margin: 0 auto;">', unsafe_allow_html=True)

# ─── Elegant Header Section ──────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 2.5rem !important;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Profil Pengguna</h1>
    <p style="color: {theme['text_secondary']}; margin: 0; font-size: 1.05rem;">
        Kelola informasi akun petani Anda, perbarui foto profil, dan atur keamanan masuk.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Build Avatar HTML Helper ─────────────────────────────────────────────────
def get_avatar_html(size=130, border_size=3):
    """Returns HTML for user avatar (custom image or emoji)."""
    if st.session_state.get("profile_avatar_img") is not None:
        try:
            buffered = BytesIO()
            st.session_state.profile_avatar_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return (
                f'<img src="data:image/png;base64,{img_str}" '
                f'style="width: {size}px; height: {size}px; object-fit: cover; '
                f'border-radius: 50%; border: {border_size}px solid {theme["primary_light"]}; '
                f'box-shadow: 0 10px 30px rgba(46, 125, 50, 0.35);" />'
            )
        except Exception:
            pass
    emoji = st.session_state.get("profile_avatar_emoji", "👨‍🌾")
    return (
        f'<div style="width: {size}px; height: {size}px; border-radius: 50%; '
        f'background: linear-gradient(135deg, {theme["primary"]} 0%, {theme["gold"]} 100%); '
        f'margin: 0 auto; display: flex; align-items: center; justify-content: center; '
        f'font-size: {size * 0.31:.0f}px; '
        f'box-shadow: 0 10px 30px rgba(46, 125, 50, 0.35); '
        f'border: {border_size}px solid rgba(255,255,255,0.1);">'
        f'{emoji}</div>'
    )

# ─── Avatar & Profile Info Card ───────────────────────────────────────────────
avatar_html = get_avatar_html(size=130)
st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 3rem 2rem !important;
     background: linear-gradient(135deg, rgba(14, 24, 12, 0.8) 0%, rgba(249, 168, 37, 0.05) 100%) !important;">
    <div style="margin: 0 auto 1.5rem; width: 130px;">
        {avatar_html}
    </div>
    <h2 style="font-size: 2rem; margin-bottom: 0.3rem;">{st.session_state.current_user}</h2>
    <div style="font-size: 0.95rem; color: {theme['gold']}; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
        🌾 Pengguna Premium PadiSense | Petani Modern
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Ganti Foto Profil Card ───────────────────────────────────────────────────
surf_rgb = "14, 24, 12" if st.session_state.theme == "dark" else "255, 255, 255"

st.markdown(f"""
<style>
/* Avatar Upload Styling */
.avatar-section-card {{
    background: rgba({surf_rgb}, 0.75);
    border: 1px solid {theme['border']};
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
}}
.emoji-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}}
</style>
<div class="avatar-section-card">
    <h3 style="color: {theme['gold']}; margin-bottom: 0.3rem; font-family: 'Playfair Display', serif;">
        📸 Ganti Foto Profil
    </h3>
    <p style="color: {theme['text_secondary']}; font-size: 0.9rem; margin-bottom: 1rem;">
        Unggah foto profil kustom Anda atau pilih avatar emoji di bawah ini.
    </p>
</div>
""", unsafe_allow_html=True)

col_upload, col_emoji = st.columns(2, gap="large")

with col_upload:
    st.markdown(f'<p style="color: {theme["text_secondary"]}; font-weight: 700; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem;">Unggah Foto (JPG / PNG)</p>', unsafe_allow_html=True)
    uploaded_photo = st.file_uploader(
        "Upload foto profil",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="profil_foto_uploader"
    )
    if uploaded_photo is not None:
        try:
            # ── Guard: hanya proses jika file benar-benar baru ────────────────
            file_bytes = uploaded_photo.read()
            file_hash  = hash(file_bytes)
            if st.session_state.get("_last_avatar_hash") != file_hash:
                st.session_state._last_avatar_hash = file_hash
                new_img = Image.open(BytesIO(file_bytes)).convert("RGB")
                st.session_state.profile_avatar_img   = new_img
                st.session_state.profile_avatar_emoji = None
                st.rerun()  # Refresh halaman agar avatar di atas langsung berubah
            st.success("✅ Foto profil berhasil diperbarui!")
        except Exception as e:
            st.error(f"❌ Gagal membaca gambar: {e}")

with col_emoji:
    st.markdown(f'<p style="color: {theme["text_secondary"]}; font-weight: 700; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem;">😊 Pilih Avatar Emoji</p>', unsafe_allow_html=True)
    emoji_options = ["👨‍🌾", "👩‍🌾", "🧑‍🌾", "👨‍💼", "👩‍💼", "🧑‍💻", "👨‍🔬", "👩‍🔬", "🌾", "🌱"]
    selected_emoji = st.selectbox(
        "Pilih emoji avatar",
        emoji_options,
        index=emoji_options.index(st.session_state.get("profile_avatar_emoji", "👨‍🌾"))
              if st.session_state.get("profile_avatar_emoji") in emoji_options else 0,
        label_visibility="collapsed",
        key="emoji_selector"
    )
    if st.button("Gunakan Emoji Ini", use_container_width=True, key="use_emoji_btn"):
        st.session_state.profile_avatar_emoji = selected_emoji
        st.session_state.profile_avatar_img = None
        st.success(f"Avatar berhasil diubah menjadi {selected_emoji}!")
        st.rerun()

# ─── Statistics Grid ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
riwayat_all = st.session_state.get("riwayat_list", [])
total_analisis = len(riwayat_all)
total_penyakit = len(set([r["disease"] for r in riwayat_all if r["status"] == "Terdeteksi"]))
avg_conf = (sum([r["confidence"] for r in riwayat_all]) / total_analisis) if total_analisis > 0 else 0.0

col_st1, col_st2, col_st3, col_st4 = st.columns(4, gap="medium")

with col_st1:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{total_analisis} Kali</div>
        <div class="stat-badge-label">Total Analisis</div>
    </div>
    """, unsafe_allow_html=True)

with col_st2:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{total_penyakit} Jenis</div>
        <div class="stat-badge-label">Penyakit Terdeteksi</div>
    </div>
    """, unsafe_allow_html=True)

with col_st3:
    chat_count = len(st.session_state.get("chat_history", []))
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{chat_count} Kali</div>
        <div class="stat-badge-label">Tanya PadiBot</div>
    </div>
    """, unsafe_allow_html=True)

with col_st4:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{avg_conf:.1f}%</div>
        <div class="stat-badge-label">Akurasi Rata-rata</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Account Information & Recent Activity ────────────────────────────────────
col_info, col_activity = st.columns(2, gap="large")

with col_info:
    phone_val  = st.session_state.get("user_phone", "-")
    email_val  = st.session_state.get("user_email", "petani@padisense.local")
    join_date  = st.session_state.get("join_date", "15 Mei 2026")
    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <h3 style="color: {theme['gold']}; margin-bottom: 1.5rem; border-bottom: 2px solid {theme['border']}; padding-bottom: 0.5rem;">Informasi Akun</h3>
        <div style="display: flex; flex-direction: column; gap: 1.2rem; font-size: 0.95rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">📧 Alamat Email:</span>
                <span style="color: {theme['text']};">{email_val}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">👤 Nama Lengkap:</span>
                <span style="color: {theme['text']};">{st.session_state.current_user}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">📱 Nomor Telepon:</span>
                <span style="color: {theme['text']};">{phone_val}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">📅 Tanggal Bergabung:</span>
                <span style="color: {theme['text']};">{join_date}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">🌍 Zona Waktu:</span>
                <span style="color: {theme['text']};">WIB (UTC+07:00)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_activity:
    riwayat_list = st.session_state.get("riwayat_list", [])
    if riwayat_list:
        last_entry   = max(riwayat_list, key=lambda x: x["date"])
        last_disease = last_entry["disease"]
        last_conf    = f"{last_entry['confidence']:.1f}%"
        last_date_str = last_entry["date"].strftime("%d %B %Y, %H:%M") + " WIB"
    else:
        last_disease  = "Belum ada analisis"
        last_conf     = "-"
        last_date_str = "-"

    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <h3 style="color: {theme['primary_light']}; margin-bottom: 1.5rem; border-bottom: 2px solid {theme['border']}; padding-bottom: 0.5rem;">Aktivitas Terakhir</h3>
        <div style="display: flex; flex-direction: column; gap: 1.2rem; font-size: 0.95rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">Analisis Terakhir:</span>
                <span style="color: {theme['text']};">{last_disease}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">Tingkat Keyakinan:</span>
                <span style="color: {theme['gold']}; font-weight: bold;">{last_conf} Confidence</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">Sesi Masuk Terakhir:</span>
                <span style="color: {theme['text']};">{last_date_str}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: {theme['text_secondary']};">Status Autentikasi:</span>
                <span style="color: {theme['primary_light']}; font-weight: bold;">✓ Aktif (Sesi Terlindungi)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Danger Zone Card ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="border: 1px solid rgba(239, 83, 80, 0.4) !important;
     background: linear-gradient(135deg, rgba(14, 24, 12, 0.8) 0%, rgba(239, 83, 80, 0.05) 100%) !important;">
    <h3 style="color: {theme['danger']}; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(239, 83, 80, 0.2); padding-bottom: 0.5rem;">
        ⚠️ Zona Peringatan Keamanan
    </h3>
""", unsafe_allow_html=True)

col_pwd, col_logout = st.columns(2, gap="medium")

with col_pwd:
    if st.button("Ubah Password Masuk Akun", use_container_width=True, key="btn_ganti_password"):
        st.switch_page("pages/ganti_password.py")

with col_logout:
    if st.button("Logout Sekarang", use_container_width=True, key="logout_profil"):
        st.session_state.is_logged_in = False
        st.session_state.chat_history = []
        st.session_state.detected_diseases = []
        st.query_params.clear()
        st.switch_page("pages/login.py")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align: center; padding: 4rem 0 2rem; border-top: 1px solid {theme['border']}; color: {theme['text_muted']}; font-size: 0.9rem;">
    🌾 <strong>PadiSense Premium v1.2</strong> | Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity: 0.65; font-size: 0.8rem;">© 2026 CAMP Batch 4 | Data Science &amp; Generative AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Tutup Wrapper