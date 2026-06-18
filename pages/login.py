import streamlit as st
import theme_utils
import db_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Masuk — PadiSense",
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

# ─── Setup DB (buat tabel kalau belum ada) ────────────────────────────────────
db_utils.setup_tables()

theme    = theme_utils.THEMES[st.session_state.theme]
surf_rgb = theme["surface"]
card_rgb = theme.get("card_rgb", surf_rgb)
theme_utils.inject_theme("login")

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.main .block-container {{
    max-width: 460px !important;
    margin: 0 auto !important;
    padding: 10vh 1.5rem 4rem !important;
}}
.login-brand {{ text-align: center; margin-bottom: 1.8rem; }}
.login-brand-name {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 900;
    color: {theme['text']}; display: block;
}}
.login-brand-name em {{ font-style: normal; color: {theme['gold']}; }}
.login-brand-sub {{
    font-size: 0.85rem; color: {theme['text_secondary']};
    margin-top: 0.35rem; display: block; line-height: 1.5;
}}
[data-testid="stForm"] {{
    background: rgba({card_rgb}, 0.80) !important;
    backdrop-filter: blur(22px) saturate(170%) !important;
    border: 1px solid {theme['border']} !important;
    border-radius: 22px !important;
    padding: 2rem 2.2rem 1.8rem !important;
    box-shadow: 0 16px 50px rgba(0,0,0,0.25) !important;
}}
.stTextInput > label {{
    font-size: 0.74rem !important; font-weight: 700 !important;
    color: {theme['text_secondary']} !important;
    text-transform: uppercase !important; letter-spacing: 0.09em !important;
}}
.stTextInput input {{
    background: rgba({surf_rgb}, 0.55) !important;
    border: 1.5px solid {theme['border']} !important;
    border-radius: 12px !important; color: {theme['text']} !important;
    font-size: 0.88rem !important; padding: 0.6rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput input:focus {{
    border-color: {theme['gold']} !important;
    box-shadow: 0 0 0 3px rgba(249,168,37,0.13) !important;
}}
[data-testid="stFormSubmitButton"] > button {{
    background: linear-gradient(135deg, {theme['primary']} 0%, {theme['primary_light']} 100%) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 0.9rem !important; padding: 0.7rem 1.4rem !important;
    box-shadow: 0 4px 16px rgba(46,125,50,0.32) !important;
    width: 100% !important; margin-top: 0.5rem !important;
    transition: all 0.22s ease !important;
}}
[data-testid="stFormSubmitButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(46,125,50,0.42) !important;
    background: linear-gradient(135deg, {theme['primary_light']} 0%, {theme['gold']} 100%) !important;
    color: #040D02 !important;
}}
.stButton > button {{
    background: rgba({surf_rgb}, 0.45) !important;
    color: {theme['text_secondary']} !important;
    border: 1.5px solid {theme['border']} !important;
    border-radius: 12px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; box-shadow: none !important;
}}
.stButton > button:hover {{
    border-color: {theme['primary_light']} !important;
    color: {theme['primary_light']} !important;
    background: rgba({surf_rgb}, 0.7) !important;
}}
.db-status {{
    font-size: 0.72rem; padding: 0.3rem 0.8rem;
    border-radius: 8px; text-align: center;
    margin-bottom: 1rem; font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# ─── Status Koneksi DB ────────────────────────────────────────────────────────
db_ok = db_utils.test_connection()
if db_ok:
    st.markdown(
        '<div class="db-status" style="background:rgba(105,240,174,0.1);'
        'border:1px solid rgba(105,240,174,0.3);color:#69F0AE;">'
        '🟢 Database terhubung</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="db-status" style="background:rgba(239,83,80,0.1);'
        'border:1px solid rgba(239,83,80,0.3);color:#EF5350;">'
        '🔴 Database tidak terhubung — mode sesi sementara</div>',
        unsafe_allow_html=True
    )

# ─── Brand ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="login-brand">
    <span style="font-size:1.8rem; display:block; margin-bottom:0.3rem;">🌾</span>
    <span class="login-brand-name">Padi<em>Sense</em></span>
    <span class="login-brand-sub">Selamat datang kembali, Petani Modern</span>
</div>
""", unsafe_allow_html=True)

# ─── Login Form ───────────────────────────────────────────────────────────────
with st.form("login_form"):
    email    = st.text_input("Alamat Email",  placeholder="contoh@email.com")
    password = st.text_input("Password",      type="password", placeholder="Masukkan password...")
    submitted = st.form_submit_button("Masuk ke PadiSense →", use_container_width=True)

if submitted:
    if not email or not password:
        st.error("❌ Email dan password wajib diisi!")
    elif db_ok:
        # ── Login via database ────────────────────────────────────────────────
        result = db_utils.login_user(email, password)
        if result["success"]:
            user = result["user"]
            # Set session state
            st.session_state.is_logged_in       = True
            st.session_state.user_id            = user["id"]
            st.session_state.current_user       = user["full_name"]
            st.session_state.user_email         = user["email"]
            st.session_state.user_phone         = user.get("phone", "")
            st.session_state.profile_avatar_emoji = user.get("avatar_emoji", "👨‍🌾")
            join_dt = user.get("created_at")
            st.session_state.join_date = (
                join_dt.strftime("%d %B %Y") if join_dt else "—"
            )
            # Kosongkan riwayat sesi lama, akan diisi dari DB
            st.session_state.riwayat_list      = []
            st.session_state.chat_history      = []
            st.session_state.detected_diseases = []

            # Catat login ke DB
            db_utils.log_login(user["id"], user["email"], user["full_name"], "login")

            st.success("🎉 Login berhasil! Mengarahkan ke beranda...")
            st.switch_page("app.py")
        else:
            st.error(f"❌ {result['message']}")
    else:
        # ── Fallback: mode sesi sementara (DB mati) ──────────────────────────
        st.session_state.is_logged_in       = True
        st.session_state.user_id            = 0
        st.session_state.current_user       = email.split("@")[0]
        st.session_state.user_email         = email
        st.session_state.user_phone         = ""
        st.session_state.profile_avatar_emoji = "👨‍🌾"
        st.session_state.riwayat_list       = []
        st.session_state.chat_history       = []
        st.session_state.detected_diseases  = []
        st.warning("⚠️ Database offline — login sesi sementara (data tidak tersimpan)")
        st.switch_page("app.py")

# ─── Daftar Link ──────────────────────────────────────────────────────────────
st.markdown(f'<hr style="border-color:{theme["border"]};margin:1.5rem 0 1.2rem;">', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center;font-size:0.82rem;color:{theme["text_muted"]};">Belum punya akun?</p>', unsafe_allow_html=True)

if st.button("Daftar Akun Baru", use_container_width=True):
    st.switch_page("pages/register.py")

st.markdown(f"""
<p style="text-align:center;font-size:0.72rem;color:{theme['text_muted']};margin-top:1.8rem;opacity:0.65;">
    © 2026 CAMP Batch 4 &nbsp;·&nbsp; Data Science & Generative AI
</p>
""", unsafe_allow_html=True)
