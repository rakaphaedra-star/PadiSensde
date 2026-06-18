import streamlit as st
import os
from datetime import datetime, timedelta

# ─── Theme Definitions ────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":            "#090E07",
        "surface":       "11, 19, 8",
        "primary":       "#2E7D32",
        "primary_light": "#4CAF50",
        "gold":          "#F9A825",
        "border":        "rgba(46, 125, 50, 0.28)",
        "border_light":  "rgba(46, 125, 50, 0.13)",
        "text":          "#E8F5E9",
        "text_secondary":"#A5D6A7",
        "text_muted":    "#5A8060",
        "danger":        "#EF5350",
        "card_rgb":      "14, 24, 12",
    },
    "light": {
        "bg":            "#F0F7EC",
        "surface":       "240, 247, 236",
        "primary":       "#2E7D32",
        "primary_light": "#388E3C",
        "gold":          "#F57F17",
        "border":        "rgba(46, 125, 50, 0.22)",
        "border_light":  "rgba(46, 125, 50, 0.10)",
        "text":          "#1B5E20",
        "text_secondary":"#388E3C",
        "text_muted":    "#558B2F",
        "danger":        "#C62828",
        "card_rgb":      "255, 255, 255",
    },
}

# ─── Auth Guard ───────────────────────────────────────────────────────────────
def check_auth():
    """Initialize session state and redirect to login if not authenticated."""
    # Initialize defaults
    if "is_logged_in"          not in st.session_state: st.session_state.is_logged_in          = False
    if "theme"                 not in st.session_state: st.session_state.theme                 = "dark"
    if "current_user"          not in st.session_state: st.session_state.current_user          = ""
    if "user_email"            not in st.session_state: st.session_state.user_email            = "petani@padisense.local"
    if "user_phone"            not in st.session_state: st.session_state.user_phone            = "-"
    if "user_password"         not in st.session_state: st.session_state.user_password         = ""
    if "join_date"             not in st.session_state: st.session_state.join_date             = datetime.now().strftime("%d %B %Y")
    if "chat_history"          not in st.session_state: st.session_state.chat_history          = []
    if "detected_diseases"     not in st.session_state: st.session_state.detected_diseases     = []
    if "riwayat_list"          not in st.session_state: st.session_state.riwayat_list          = []
    if "profile_avatar_emoji"  not in st.session_state: st.session_state.profile_avatar_emoji  = "👨‍🌾"
    if "profile_avatar_img"    not in st.session_state: st.session_state.profile_avatar_img    = None

    # Restore session from query params (persists across refresh & page navigation)
    if not st.session_state.is_logged_in:
        params = st.query_params
        if params.get("logged_in") == "true":
            st.session_state.is_logged_in         = True
            st.session_state.current_user         = params.get("current_user", "Pengguna")
            st.session_state.user_email           = params.get("user_email", "petani@padisense.local")
            st.session_state.user_phone           = params.get("user_phone", "-")
            st.session_state.user_password        = params.get("user_password", "")
            st.session_state.profile_avatar_emoji = params.get("profile_avatar_emoji", "👨‍🌾")
            st.session_state.user_id              = int(params.get("user_id", 0))  # ← TAMBAH INI
            
    # If logged in, always keep query params in sync so they survive navigation
    if st.session_state.is_logged_in:
        current_params = dict(st.query_params)
        if current_params.get("logged_in") != "true":
            st.query_params.update({
                "logged_in":           "true",
                "current_user":        st.session_state.current_user,
                "user_email":          st.session_state.user_email,
                "user_phone":          st.session_state.user_phone,
                "user_password":       st.session_state.user_password,
                "profile_avatar_emoji": st.session_state.profile_avatar_emoji,
                "user_id":              str(st.session_state.get("user_id", 0)),  # ← TAMBAH INI
            })
        return  # authenticated

    # Not logged in → redirect
    st.switch_page("pages/login.py")


# ─── CSS Injection ────────────────────────────────────────────────────────────
def inject_theme(page_name: str = ""):
    """Inject global CSS theme styles."""
    theme    = THEMES[st.session_state.get("theme", "dark")]
    surf_rgb = theme["surface"]
    card_rgb = theme.get("card_rgb", surf_rgb)

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* ── Reset & Base ── */
    *, *::before, *::after {{ box-sizing: border-box; }}

    html, body, .stApp {{
        background: {theme['bg']} !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: {theme['text']} !important;
        transition: background 0.4s ease, color 0.4s ease;
    }}

    /* Hide Streamlit chrome */
    #MainMenu, footer, header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {{ display: none !important; }}

    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Playfair Display', serif !important;
    }}

    /* ── Glass Card ── */
    .glass-card {{
        background: rgba({card_rgb}, 0.72) !important;
        backdrop-filter: blur(18px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(160%) !important;
        border: 1px solid {theme['border']} !important;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.18), 0 1px 4px rgba(46,125,50,0.08) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin-bottom: 1.8rem !important;
        transition: transform 0.3s cubic-bezier(0.16,1,0.3,1),
                    box-shadow 0.3s ease,
                    border-color 0.3s ease !important;
    }}
    .glass-card:hover {{
        transform: translateY(-3px) !important;
        border-color: {theme['primary_light']} !important;
        box-shadow: 0 12px 36px 0 rgba(46,125,50,0.18) !important;
    }}

    /* ── Navbar ── */
    .navbar-container {{
        background: rgba({surf_rgb}, 0.88) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-bottom: 1px solid {theme['border']} !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 2px 20px rgba(0,0,0,0.12) !important;
        margin-bottom: 1.5rem !important;
        position: sticky;
        top: 0;
        z-index: 999;
    }}
    .nav-logo {{
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 900;
        color: {theme['text']};
        display: flex;
        align-items: center;
        gap: 0.4rem;
        letter-spacing: -0.3px;
    }}
    .nav-logo span {{ color: {theme['gold']}; }}

    /* ── Buttons ── */
    .stButton > button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['primary_light']} 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 3px 12px rgba(46,125,50,0.3) !important;
        transition: all 0.25s cubic-bezier(0.16,1,0.3,1) !important;
        letter-spacing: 0.01em !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(46,125,50,0.4) !important;
        background: linear-gradient(135deg, {theme['primary_light']} 0%, {theme['gold']} 100%) !important;
        color: #050D03 !important;
    }}
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ── Form Inputs ── */
    .stTextInput input, .stTextArea textarea {{
        background: rgba({surf_rgb}, 0.55) !important;
        border: 1.5px solid {theme['border']} !important;
        color: {theme['text']} !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.92rem !important;
        padding: 0.7rem 1rem !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {theme['gold']} !important;
        box-shadow: 0 0 0 3px rgba(249,168,37,0.15) !important;
        outline: none !important;
    }}
    .stTextInput > label, .stTextArea > label {{
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: {theme['text_secondary']} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }}

    /* ── Selectbox ── */
    .stSelectbox [data-baseweb="select"] {{
        background: rgba({surf_rgb}, 0.55) !important;
        border: 1.5px solid {theme['border']} !important;
        border-radius: 12px !important;
        color: {theme['text']} !important;
    }}
    .stSelectbox label {{
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: {theme['text_secondary']} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }}

    /* ── Checkbox ── */
    .stCheckbox > label {{
        color: {theme['text_secondary']} !important;
        font-size: 0.88rem !important;
    }}

    /* ── Stat Badge ── */
    .stat-badge {{
        background: linear-gradient(135deg, rgba({surf_rgb}, 0.85) 0%, rgba({surf_rgb}, 0.45) 100%);
        border: 1px solid {theme['border']};
        border-radius: 18px;
        padding: 1.6rem 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .stat-badge:hover {{
        transform: translateY(-4px);
        border-color: {theme['gold']};
        box-shadow: 0 8px 24px rgba(249,168,37,0.18);
    }}
    .stat-badge-value {{
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 900;
        color: {theme['gold']};
        line-height: 1;
    }}
    .stat-badge-label {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: {theme['text_secondary']};
        margin-top: 0.35rem;
    }}

    /* ── Disease Items ── */
    .disease-item-premium {{
        background: rgba({surf_rgb}, 0.6);
        border-left: 4px solid {theme['primary']};
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1rem;
        border-top: 1px solid {theme['border_light']};
        border-right: 1px solid {theme['border_light']};
        border-bottom: 1px solid {theme['border_light']};
        transition: all 0.25s ease;
    }}
    .disease-item-premium:hover {{
        border-left-color: {theme['gold']};
        transform: translateX(4px);
    }}

    /* ── Chat Bubbles ── */
    .chat-bubble-custom {{
        max-width: 78%;
        padding: 0.85rem 1.2rem;
        border-radius: 18px;
        font-size: 0.92rem;
        line-height: 1.65;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .chat-bubble-user {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['primary_light']} 100%) !important;
        color: white !important;
        border-bottom-right-radius: 4px;
        box-shadow: 0 3px 12px rgba(46,125,50,0.25);
    }}
    .chat-bubble-bot {{
        background: rgba({card_rgb}, 0.88) !important;
        border: 1px solid {theme['border']} !important;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {theme['bg']}; }}
    ::-webkit-scrollbar-thumb {{ background: {theme['primary']}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {theme['primary_light']}; }}

    /* ── Dataframe ── */
    .stDataFrame {{ border-radius: 12px !important; overflow: hidden !important; }}

    /* ── Divider ── */
    hr {{ border-color: {theme['border']} !important; margin: 1.5rem 0 !important; }}

    /* ── Alert ── */
    .stAlert {{ border-radius: 12px !important; }}

    /* ── Spinner ── */
    .stSpinner > div {{ border-top-color: {theme['primary_light']} !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ─── PATCH untuk theme_utils.py ──────────────────────────────────────────────
# Ganti fungsi render_navbar() yang lama dengan ini
# Perubahan: tambah kolom "Grafik" di navbar

def render_navbar(active_page: str = ""):
    """Render the floating glassmorphism navigation bar."""
    theme = THEMES[st.session_state.get("theme", "dark")]

    st.markdown('<div class="navbar-container">', unsafe_allow_html=True)

    # ← Tambah kolom grafik di sini (ubah rasio kolom)
    col_logo, col_beranda, col_riwayat, col_grafik, col_panduan, col_tentang, col_actions = st.columns(
        [2, 1.1, 1.1, 1.1, 1.1, 1.1, 1.4], gap="small"
    )

    with col_logo:
        st.markdown(
            f'<div class="nav-logo">🌾 Padi<span>Sense</span></div>',
            unsafe_allow_html=True
        )

    with col_beranda:
        lbl = "**Beranda**" if active_page == "beranda" else "Beranda"
        if st.button(lbl, key="nav_beranda", use_container_width=True):
            st.switch_page("app.py")

    with col_riwayat:
        lbl = "**Riwayat**" if active_page == "riwayat" else "Riwayat"
        if st.button(lbl, key="nav_riwayat", use_container_width=True):
            st.switch_page("pages/riwayat.py")

    with col_grafik:
        # ← BARU: tombol Grafik
        lbl = "**📈 Grafik**" if active_page == "grafik" else "📈 Grafik"
        if st.button(lbl, key="nav_grafik", use_container_width=True):
            st.switch_page("pages/grafik.py")

    with col_panduan:
        lbl = "**Panduan**" if active_page == "panduan" else "Panduan"
        if st.button(lbl, key="nav_panduan", use_container_width=True):
            st.switch_page("pages/panduan.py")

    with col_tentang:
        lbl = "**Tentang**" if active_page == "tentang" else "Tentang"
        if st.button(lbl, key="nav_tentang", use_container_width=True):
            st.switch_page("pages/tentang.py")

    with col_actions:
        ac1, ac2 = st.columns(2, gap="small")
        with ac1:
            if st.button("👤", key="nav_profil", use_container_width=True, help="Profil Saya"):
                st.switch_page("pages/profil.py")
        with ac2:
            lbl_theme = "🌙" if st.session_state.get("theme", "dark") == "dark" else "☀️"
            if st.button(lbl_theme, key="nav_theme", use_container_width=True, help="Ganti Tema"):
                st.switch_page("pages/theme.py")

    st.markdown('</div>', unsafe_allow_html=True)