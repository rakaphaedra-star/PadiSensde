import streamlit as st
import theme_utils
import time

st.set_page_config(
    page_title="Ubah Password — PadiSense",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

theme_utils.check_auth()
theme    = theme_utils.THEMES[st.session_state.theme]
surf_rgb = theme["surface"]
card_rgb = theme.get("card_rgb", surf_rgb)
theme_utils.inject_theme("ganti_password")

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.main .block-container {{
    max-width: 500px !important;
    margin: 0 auto !important;
    padding: 2.5rem 1.5rem 5rem !important;
}}

/* ── Back button ── */
.stButton > button {{
    background: transparent !important;
    border: 1.5px solid {theme['border']} !important;
    color: {theme['text_muted']} !important;
    box-shadow: none !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.38rem 0.9rem !important;
    border-radius: 9px !important;
    width: auto !important;
    display: inline-block !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{
    border-color: {theme['primary_light']} !important;
    color: {theme['primary_light']} !important;
    background: rgba({surf_rgb}, 0.4) !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ── Style form as glass card ── */
[data-testid="stForm"] {{
    background: rgba({card_rgb}, 0.78) !important;
    backdrop-filter: blur(20px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
    border: 1px solid {theme['border']} !important;
    border-radius: 20px !important;
    padding: 2rem 2.2rem !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.18) !important;
    margin-top: 0.5rem !important;
}}

/* ── Form labels ── */
.stTextInput > label {{
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
    font-size: 0.9rem !important;
    padding: 0.65rem 1rem !important;
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
    padding: 0.68rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(46,125,50,0.3) !important;
    transition: all 0.22s ease !important;
    width: 100% !important;
    margin-top: 0.4rem !important;
}}
[data-testid="stFormSubmitButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 20px rgba(46,125,50,0.4) !important;
    background: linear-gradient(135deg, {theme['primary_light']} 0%, {theme['gold']} 100%) !important;
    color: #040D02 !important;
}}

/* ── Alert ── */
.stAlert {{ border-radius: 12px !important; }}
</style>
""", unsafe_allow_html=True)

# ─── Back Button ──────────────────────────────────────────────────────────────
if st.button("← Kembali ke Profil", key="back_btn"):
    st.switch_page("pages/profil.py")

# ─── Inline Header (no card, no wrapper) ──────────────────────────────────────
st.markdown(f"""
<div style="margin: 1.8rem 0 0.2rem; text-align:center;">
    <span style="font-size:2.5rem;">🔐</span>
    <h1 style="
        font-family:'Playfair Display',serif;
        font-size:1.9rem; font-weight:900;
        color:{theme['text']}; margin:0.4rem 0 0.4rem;
        letter-spacing:-0.3px;
    ">Ubah Password</h1>
    <p style="color:{theme['text_secondary']}; font-size:0.9rem;
              line-height:1.55; margin:0;">
        Perbarui kata sandi akun PadiSense Anda secara aman.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Form (CSS makes it glass card) ───────────────────────────────────────────
with st.form("form_pwd", clear_on_submit=True):
    old_pw  = st.text_input("Password Saat Ini",        type="password", placeholder="Masukkan password lama")
    new_pw  = st.text_input("Password Baru",             type="password", placeholder="Minimal 6 karakter")
    conf_pw = st.text_input("Konfirmasi Password Baru",  type="password", placeholder="Ulangi password baru")
    save    = st.form_submit_button("Simpan Password Baru →", use_container_width=True)

if save:
    cur = st.session_state.get("user_password", "")
    if not old_pw or not new_pw or not conf_pw:
        st.error("Semua kolom wajib diisi.")
    elif old_pw != cur:
        st.error("Password saat ini tidak cocok.")
    elif len(new_pw) < 6:
        st.error("Password baru minimal 6 karakter.")
    elif new_pw != conf_pw:
        st.error("Konfirmasi password tidak sesuai.")
    elif new_pw == cur:
        st.warning("Password baru tidak boleh sama dengan yang lama.")
    else:
        st.session_state.user_password = new_pw
        st.query_params.update({"user_password": new_pw})
        st.success("Password berhasil diperbarui!")
        time.sleep(1.2)
        st.switch_page("pages/profil.py")

# ─── Tips ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    margin-top: 1.5rem;
    padding: 1.3rem 1.6rem;
    background: rgba({surf_rgb}, 0.45);
    border: 1px solid {theme['border']};
    border-left: 4px solid {theme['gold']};
    border-radius: 14px;
">
    <p style="
        font-size:0.72rem; font-weight:800; text-transform:uppercase;
        letter-spacing:0.1em; color:{theme['gold']}; margin:0 0 0.75rem;
    ">💡 Tips Keamanan</p>
    <ul style="
        color:{theme['text_secondary']}; margin:0 0 0 1.1rem;
        padding:0; line-height:2.1; font-size:0.86rem;
    ">
        <li>Gunakan minimal <strong>8 karakter</strong> untuk keamanan optimal</li>
        <li>Kombinasikan huruf besar, kecil, angka, dan simbol</li>
        <li>Jangan gunakan tanggal lahir atau nama sebagai password</li>
    </ul>
</div>
""", unsafe_allow_html=True)