import streamlit as st
import theme_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tema - PadiSense Premium",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Theme ───────────────────────────────────────────────────────
theme_utils.check_auth()
theme = theme_utils.THEMES[st.session_state.theme]
theme_utils.inject_theme("tema")

# ─── Navbar ──────────────────────────────────────────────────────────────────
theme_utils.render_navbar("")

# ─── Main Wrapper ─────────────────────────────────────────────────────────────
st.markdown('<div style="padding: 0 2.5rem 3rem; max-width: 1100px; margin: 0 auto;">', unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 2.5rem !important;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨 Pengaturan Tema Warna</h1>
    <p style="color: {theme['text_secondary']}; margin: 0; font-size: 1.05rem;">
        Sesuaikan tampilan visual antarmuka PadiSense agar paling nyaman digunakan dalam berbagai kondisi cahaya.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Current Theme Status ─────────────────────────────────────────────────────
is_dark  = st.session_state.get("theme", "dark") == "dark"
is_light = not is_dark

active_theme_label = "🌙 Dark Mode (Malam Moss)" if is_dark else "☀️ Light Mode (Embun Pagi)"
active_border      = theme['primary'] if is_dark else theme['gold']
glow_bg            = "rgba(46,125,50,0.08)" if is_dark else "rgba(249,168,37,0.08)"

st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: 1.5rem !important; border-left: 5px solid {active_border};">
    <span style="font-size: 1rem; color: {theme['text_secondary']}; font-weight: bold;">
        Tema Aktif Saat Ini:
    </span>
    <span style="font-size: 1.1rem; color: {theme['gold']}; font-weight: 800; margin-left: 0.5rem;">
        {active_theme_label}
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Theme Picker Cards ───────────────────────────────────────────────────────
col_dark, col_light = st.columns(2, gap="large")

# --- Dark Mode Card ---
with col_dark:
    dark_border = f"3px solid {theme['primary']}" if is_dark else f"1px solid {theme['border']}"
    dark_bg     = "background: linear-gradient(135deg, rgba(14, 24, 12, 0.9) 0%, rgba(249, 168, 37, 0.05) 100%) !important;"

    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 3rem 2rem !important; border: {dark_border}; {dark_bg if is_dark else ''}">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌙</div>
        <h3 style="font-size: 1.6rem; color: {theme['text']}; margin-bottom: 0.8rem;">Dark Mode</h3>
        <p style="color: {theme['text_secondary']}; line-height: 1.6; font-size: 0.92rem; min-height: 50px; margin-bottom: 1.5rem;">
            Mengadopsi palet warna gelap lumut sawah yang lembut di mata. Pilihan tepat untuk mengurangi kelelahan mata di malam hari.
        </p>
        {'<span style="background: ' + theme["primary"] + '; color: #070C06; padding: 0.4rem 1.2rem; border-radius: 50px; font-size: 0.8rem; font-weight: 800;">🟢 SEDANG AKTIF</span>' if is_dark else ''}
    </div>
    """, unsafe_allow_html=True)

    if not is_dark:
        if st.button("🌙 Aktifkan Dark Mode", key="btn_dark", use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()
    else:
        st.markdown(f'<div style="text-align:center; color:{theme["text_muted"]}; font-size:0.85rem; margin-top:0.5rem;">✓ Sedang digunakan</div>', unsafe_allow_html=True)

# --- Light Mode Card ---
with col_light:
    light_border = f"3px solid {theme['gold']}" if is_light else f"1px solid {theme['border']}"
    light_bg     = "background: linear-gradient(135deg, #FFFFFF 0%, rgba(46, 125, 50, 0.05) 100%) !important;"

    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 3rem 2rem !important; border: {light_border}; {light_bg if is_light else ''}">
        <div style="font-size: 4rem; margin-bottom: 1rem;">☀️</div>
        <h3 style="font-size: 1.6rem; color: {theme['text']}; margin-bottom: 0.8rem;">Light Mode</h3>
        <p style="color: {theme['text_secondary']}; line-height: 1.6; font-size: 0.92rem; min-height: 50px; margin-bottom: 1.5rem;">
            Menyuguhkan kesegaran warna putih embun pagi dengan aksen hijau emerald sawah rimbun. Optimal digunakan di bawah terik matahari siang.
        </p>
        {'<span style="background: ' + theme["gold"] + '; color: #FFFFFF; padding: 0.4rem 1.2rem; border-radius: 50px; font-size: 0.8rem; font-weight: 800;">🟢 SEDANG AKTIF</span>' if is_light else ''}
    </div>
    """, unsafe_allow_html=True)

    if not is_light:
        if st.button("☀️ Aktifkan Light Mode", key="btn_light", use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()
    else:
        st.markdown(f'<div style="text-align:center; color:{theme["text_muted"]}; font-size:0.85rem; margin-top:0.5rem;">✓ Sedang digunakan</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align: center; padding: 4rem 0 2rem; border-top: 1px solid {theme['border']}; color: {theme['text_muted']}; font-size: 0.9rem;">
    🌾 <strong>PadiSense Premium v1.2</strong> | Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity: 0.65; font-size: 0.8rem;">© 2026 CAMP Batch 4 | Data Science &amp; Generative AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
