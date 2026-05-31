import streamlit as st
import theme_utils
import re

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Daftar — PadiSense",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Session Init ─────────────────────────────────────────────────────────────
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if st.session_state.is_logged_in:
    st.switch_page("app.py")

theme    = theme_utils.THEMES[st.session_state.theme]
surf_rgb = theme["surface"]
card_rgb = theme.get("card_rgb", surf_rgb)
theme_utils.inject_theme("register")

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.main .block-container {{
    max-width: 480px !important;
    margin: 0 auto !important;
    padding: 10vh 1.5rem 4rem !important;
}}

/* ── Brand centered ── */
.reg-brand {{
    text-align: center;
    margin-bottom: 1.8rem;
}}
.reg-brand-name {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 900;
    color: {theme['text']}; letter-spacing: -0.5px;
    display: block;
}}
.reg-brand-name em {{ font-style: normal; color: {theme['gold']}; }}
.reg-brand-sub {{
    font-size: 0.85rem; color: {theme['text_secondary']};
    margin-top: 0.35rem; display: block; line-height: 1.5;
}}

/* ── Form as glass card ── */
[data-testid="stForm"] {{
    background: rgba({card_rgb}, 0.80) !important;
    backdrop-filter: blur(22px) saturate(170%) !important;
    -webkit-backdrop-filter: blur(22px) saturate(170%) !important;
    border: 1px solid {theme['border']} !important;
    border-radius: 22px !important;
    padding: 2rem 2.2rem 1.8rem !important;
    box-shadow: 0 16px 50px rgba(0,0,0,0.25) !important;
}}

/* ── Labels ── */
.stTextInput > label, .stCheckbox > label {{
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    color: {theme['text_secondary']} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}}

/* ── Inputs ── */
.stTextInput input {{
    background: rgba({surf_rgb}, 0.55) !important;
    border: 1.5px solid {theme['border']} !important;
    border-radius: 12px !important;
    color: {theme['text']} !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput input:focus {{
    border-color: {theme['gold']} !important;
    box-shadow: 0 0 0 3px rgba(249,168,37,0.13) !important;
}}

/* ── Submit button ── */
[data-testid="stFormSubmitButton"] > button {{
    background: linear-gradient(135deg, {theme['primary']} 0%, {theme['primary_light']} 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1.4rem !important;
    box-shadow: 0 4px 16px rgba(46,125,50,0.32) !important;
    transition: all 0.22s ease !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
}}
[data-testid="stFormSubmitButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(46,125,50,0.42) !important;
    background: linear-gradient(135deg, {theme['primary_light']} 0%, {theme['gold']} 100%) !important;
    color: #040D02 !important;
}}

/* ── Login button ── */
.stButton > button {{
    background: rgba({surf_rgb}, 0.45) !important;
    color: {theme['text_secondary']} !important;
    border: 1.5px solid {theme['border']} !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{
    border-color: {theme['primary_light']} !important;
    color: {theme['primary_light']} !important;
    background: rgba({surf_rgb}, 0.7) !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ── Alert ── */
.stAlert {{ border-radius: 12px !important; }}

/* ── Divider ── */
.reg-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, {theme['border']} 50%, transparent 100%);
    margin: 1.5rem 0 1.2rem;
}}
.reg-foot {{
    text-align: center;
    font-size: 0.82rem;
    color: {theme['text_muted']};
    margin-bottom: 0.6rem;
}}
</style>
""", unsafe_allow_html=True)

# ─── Brand (centered, no wrapper div) ────────────────────────────────────────
st.markdown(f"""
<div class="reg-brand">
    <span style="font-size:1.8rem; display:block; margin-bottom:0.3rem;">🌾</span>
    <span class="reg-brand-name">Padi<em>Sense</em></span>
    <span class="reg-brand-sub">Bergabunglah dengan Komunitas PadiSense<br>untuk Perlindungan Tanaman Padi yang Cerdas</span>
</div>
""", unsafe_allow_html=True)

# ─── Register Form ────────────────────────────────────────────────────────────
with st.form("register_form"):
    full_name    = st.text_input("Nama Lengkap",          placeholder="Masukkan nama lengkap Anda...")
    email        = st.text_input("Alamat Email",           placeholder="contoh@email.com")
    phone        = st.text_input("Nomor Telepon",          placeholder="08xx-xxxx-xxxx")
    password     = st.text_input("Password Baru",          type="password", placeholder="Minimal 8 karakter...")
    confirm_pass = st.text_input("Konfirmasi Password",    type="password", placeholder="Masukkan ulang password...")
    agree        = st.checkbox("Saya menyetujui Ketentuan Layanan & Kebijakan Privasi PadiSense")
    submitted    = st.form_submit_button("Daftarkan Akun Baru →", use_container_width=True)

if submitted:
    errors = []
    if not all([full_name, email, phone, password, confirm_pass]):
        errors.append("Seluruh kolom data wajib diisi!")
    if full_name and len(full_name) < 3:
        errors.append("Nama lengkap minimal 3 karakter!")
    if email and ("@" not in email or "." not in email):
        errors.append("Format alamat email tidak valid!")
    if password and len(password) < 8:
        errors.append("Password minimal harus 8 karakter!")
    if password and confirm_pass and password != confirm_pass:
        errors.append("Konfirmasi password tidak cocok!")
    phone_clean = phone.replace("-", "").replace(" ", "") if phone else ""
    if phone and (not phone_clean.isdigit() or len(phone_clean) < 10):
        errors.append("Nomor telepon tidak valid!")
    if not agree:
        errors.append("Anda harus menyetujui Ketentuan Layanan terlebih dahulu!")

    if errors:
        for err in errors:
            st.error(f"❌ {err}")
    else:
        st.session_state.is_logged_in  = True
        st.session_state.current_user  = full_name
        st.session_state.user_email    = email
        st.session_state.user_phone    = phone
        st.session_state.user_password = password
        st.query_params.update({
            "logged_in":            "true",
            "current_user":         full_name,
            "user_email":           email,
            "user_phone":           phone,
            "user_password":        password,
            "profile_avatar_emoji": "👨‍🌾",
        })
        st.success("🎉 Registrasi berhasil! Selamat datang di PadiSense.")
        st.switch_page("app.py")

# ─── Login Link ───────────────────────────────────────────────────────────────
st.markdown('<div class="reg-divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="reg-foot">Sudah memiliki akun?</p>', unsafe_allow_html=True)

if st.button("Masuk dengan Akun Lama", use_container_width=True, key="go_login"):
    st.switch_page("pages/login.py")

st.markdown(f"""
<p style="text-align:center; font-size:0.72rem; color:{theme['text_muted']};
          margin-top:1.8rem; opacity:0.65;">
    © 2026 CAMP Batch 4 &nbsp;·&nbsp; Data Science & Generative AI
</p>
""", unsafe_allow_html=True)
