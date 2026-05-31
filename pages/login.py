import streamlit as st
import theme_utils

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

if not st.session_state.is_logged_in:
    if st.query_params.get("logged_in") == "true":
        theme_utils.check_auth()

if st.session_state.is_logged_in:
    st.switch_page("app.py")

theme    = theme_utils.THEMES[st.session_state.theme]
surf_rgb = theme["surface"]
card_rgb = theme.get("card_rgb", surf_rgb)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, .stApp {{
    background: {theme['bg']} !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    min-height: 100vh;
}}

/* Hide all chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{ display: none !important; }}

/* Center the whole page */
.main .block-container {{
    max-width: 420px !important;
    margin: 0 auto !important;
    padding: 15vh 1.5rem 4rem !important;
}}

/* Subtle radial glow */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 70% -5%, rgba(46,125,50,0.15) 0%, transparent 65%),
        radial-gradient(ellipse 50% 40% at -5% 95%, rgba(249,168,37,0.07) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}}

/* ── Brand (above form) ── */
.brand-block {{
    text-align: center;
    margin-bottom: 1.8rem;
}}
.brand-icon {{ font-size: 2rem; display: block; margin-bottom: 0.3rem; }}
.brand-name {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 900;
    color: {theme['text']}; letter-spacing: -0.5px;
    display: block;
}}
.brand-name em {{ font-style: normal; color: {theme['gold']}; }}
.brand-sub {{
    font-size: 0.85rem; color: {theme['text_muted']};
    margin-top: 0.3rem; display: block; line-height: 1.5;
}}

/* ── Style Streamlit form as glass card ── */
[data-testid="stForm"] {{
    background: rgba({card_rgb}, 0.82) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border: 1px solid {theme['border']} !important;
    border-radius: 22px !important;
    padding: 2rem 2.2rem 1.8rem !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.05) !important;
}}

/* ── Inputs ── */
.stTextInput > label {{
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    color: {theme['text_secondary']} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}}
.stTextInput input {{
    background: rgba({surf_rgb}, 0.6) !important;
    border: 1.5px solid {theme['border']} !important;
    border-radius: 12px !important;
    color: {theme['text']} !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput input:focus {{
    border-color: {theme['gold']} !important;
    box-shadow: 0 0 0 3px rgba(249,168,37,0.14) !important;
}}

/* ── Submit button ── */
[data-testid="stFormSubmitButton"] > button {{
    background: linear-gradient(135deg, {theme['primary']} 0%, {theme['primary_light']} 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 1.4rem !important;
    box-shadow: 0 4px 16px rgba(46,125,50,0.32) !important;
    transition: all 0.22s ease !important;
    width: 100% !important;
    margin-top: 0.4rem !important;
}}
[data-testid="stFormSubmitButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(46,125,50,0.42) !important;
    background: linear-gradient(135deg, {theme['primary_light']} 0%, {theme['gold']} 100%) !important;
    color: #040D02 !important;
}}

/* ── Register button (secondary) ── */
.stButton > button {{
    background: rgba({surf_rgb}, 0.5) !important;
    color: {theme['text_secondary']} !important;
    border: 1.5px solid {theme['border']} !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.4rem !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}}
.stButton > button:hover {{
    border-color: {theme['primary_light']} !important;
    color: {theme['primary_light']} !important;
    background: rgba({surf_rgb}, 0.75) !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ── Alert ── */
.stAlert {{ border-radius: 12px !important; margin-top: 0.5rem !important; }}

/* ── Divider ── */
.login-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, {theme['border']} 50%, transparent 100%);
    margin: 1.5rem 0 1.2rem;
}}
.login-foot {{
    text-align: center;
    font-size: 0.82rem;
    color: {theme['text_muted']};
    margin-bottom: 0.6rem;
}}
</style>
""", unsafe_allow_html=True)

# ─── Brand (centered, above form) ────────────────────────────────────────────
st.markdown(f"""
<div class="brand-block">
    <span class="brand-icon">🌾</span>
    <span class="brand-name">Padi<em>Sense</em></span>
    <span class="brand-sub">Sistem cerdas diagnosa penyakit daun padi berbasis AI</span>
</div>
""", unsafe_allow_html=True)

# ─── Login Form (styled as glass card via CSS) ────────────────────────────────
with st.form("login_form", clear_on_submit=False):
    email    = st.text_input("Email", placeholder="nama@email.com")
    password = st.text_input("Password", type="password", placeholder="Masukkan password Anda")
    submitted = st.form_submit_button("Masuk ke PadiSense →", use_container_width=True)

if submitted:
    if not email or not password:
        st.error("Email dan password wajib diisi.")
    elif "@" not in email or "." not in email:
        st.error("Format email tidak valid.")
    elif len(password) < 6:
        st.error("Password minimal 6 karakter.")
    else:
        st.session_state.is_logged_in  = True
        st.session_state.current_user  = email.split("@")[0].capitalize()
        st.session_state.user_email    = email
        st.session_state.user_password = password
        st.query_params.update({
            "logged_in":            "true",
            "current_user":         st.session_state.current_user,
            "user_email":           email,
            "user_password":        password,
            "user_phone":           "-",
            "profile_avatar_emoji": "👨‍🌾",
        })
        st.switch_page("app.py")

# ─── Register Link ────────────────────────────────────────────────────────────
st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="login-foot">Belum punya akun?</p>', unsafe_allow_html=True)

if st.button("Daftar Sekarang", use_container_width=True, key="go_register"):
    st.switch_page("pages/register.py")

st.markdown(f"""
<p style="text-align:center; font-size:0.72rem; color:{theme['text_muted']};
          margin-top:1.8rem; opacity:0.65;">
    © 2026 CAMP Batch 4 &nbsp;·&nbsp; Data Science & Generative AI
</p>
""", unsafe_allow_html=True)