import streamlit as st
from datetime import datetime
import theme_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Riwayat — PadiSense",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Theme ───────────────────────────────────────────────────────
theme_utils.check_auth()
theme    = theme_utils.THEMES[st.session_state.theme]
surf_rgb = theme["surface"]
theme_utils.inject_theme("riwayat")

# ─── Navbar ──────────────────────────────────────────────────────────────────
theme_utils.render_navbar("riwayat")

# ─── Page CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
.riwayat-card {{
    background: rgba({surf_rgb}, 0.65);
    border: 1px solid {theme['border']};
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}}
.riwayat-card:hover {{
    border-color: {theme['primary_light']};
    box-shadow: 0 6px 20px rgba(46,125,50,0.12);
    transform: translateY(-2px);
}}
.badge-sehat {{
    background: linear-gradient(135deg,#1B5E20,#4CAF50);
    color:#fff; padding:0.35rem 1.1rem;
    border-radius:50px; font-size:0.8rem;
    font-weight:800; white-space:nowrap;
    box-shadow:0 3px 10px rgba(76,175,80,0.3);
}}
.badge-sakit {{
    background: linear-gradient(135deg,#B71C1C,#EF5350);
    color:#fff; padding:0.35rem 1.1rem;
    border-radius:50px; font-size:0.8rem;
    font-weight:800; white-space:nowrap;
    box-shadow:0 3px 10px rgba(239,83,80,0.3);
}}
/* Delete button style override */
div[data-testid="column"] .stButton.del-btn > button {{
    background: transparent !important;
    border: 1.5px solid rgba(239,83,80,0.35) !important;
    color: #EF5350 !important;
    padding: 0.3rem 0.7rem !important;
    font-size: 0.78rem !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    min-height: 0 !important;
}}
div[data-testid="column"] .stButton.del-btn > button:hover {{
    background: rgba(239,83,80,0.1) !important;
    border-color: #EF5350 !important;
    transform: none !important;
    box-shadow: none !important;
}}
</style>
""", unsafe_allow_html=True)

# ─── Wrapper ─────────────────────────────────────────────────────────────────
st.markdown('<div style="padding:0 2.5rem 3rem; max-width:1200px; margin:0 auto;">', unsafe_allow_html=True)

# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="padding:2.2rem 2.5rem !important;">
    <h1 style="font-size:2.2rem; margin:0 0 0.4rem; color:{theme['text']}; text-align:center;"> Riwayat Deteksi</h1>
    <p style="color:{theme['text_secondary']}; margin:0; font-size:0.95rem; line-height:1.55; text-align:center;">
        Catatan seluruh hasil analisis penyakit daun padi Anda. Kelola dan hapus riwayat sesuai kebutuhan.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Ensure session state ─────────────────────────────────────────────────────
if "riwayat_list" not in st.session_state:
    st.session_state.riwayat_list = []

history_data = st.session_state.riwayat_list

# ─── Statistics ──────────────────────────────────────────────────────────────
total      = len(history_data)
terdeteksi = sum(1 for h in history_data if h.get("status") == "Terdeteksi")
sehat      = sum(1 for h in history_data if h.get("status") == "Sehat")
avg_conf   = (sum(h.get("confidence", 0) for h in history_data) / total) if total > 0 else 0

col_s1, col_s2, col_s3, col_s4 = st.columns(4, gap="medium")
with col_s1:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{total}</div>
        <div class="stat-badge-label">Total Analisis</div>
    </div>""", unsafe_allow_html=True)
with col_s2:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{terdeteksi}</div>
        <div class="stat-badge-label">Penyakit Terdeteksi</div>
    </div>""", unsafe_allow_html=True)
with col_s3:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{sehat}</div>
        <div class="stat-badge-label">Tanaman Sehat</div>
    </div>""", unsafe_allow_html=True)
with col_s4:
    st.markdown(f"""
    <div class="stat-badge">
        <div class="stat-badge-value">{avg_conf:.0f}%</div>
        <div class="stat-badge-label">Rata-rata Confidence</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ─── Filter & Actions Bar ────────────────────────────────────────────────────
st.markdown('<div class="glass-card" style="padding:1.4rem 2rem !important; margin-bottom:1.5rem !important;">', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns([1.2, 1.2, 0.8], gap="medium")

with col_f1:
    filter_status = st.selectbox(
        "Filter Status",
        ["Semua", "Terdeteksi", "Sehat"],
        key="f_status"
    )
with col_f2:
    diseases = sorted(list(set(h.get("disease","") for h in history_data if h.get("disease"))))
    filter_disease = st.selectbox(
        "Filter Penyakit",
        ["Semua"] + diseases,
        key="f_disease"
    )
with col_f3:
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Semua", use_container_width=True, key="hapus_semua"):
        st.session_state.riwayat_list = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── Apply Filters ───────────────────────────────────────────────────────────
filtered = list(history_data)
if filter_status != "Semua":
    filtered = [h for h in filtered if h.get("status") == filter_status]
if filter_disease != "Semua":
    filtered = [h for h in filtered if h.get("disease") == filter_disease]
filtered = sorted(filtered, key=lambda x: x.get("date", datetime.min), reverse=True)

# ─── List Riwayat ─────────────────────────────────────────────────────────────
if not filtered:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; padding:4rem 2rem !important;">
        <div style="font-size:3rem; margin-bottom:1rem; opacity:0.45;">📭</div>
        <h4 style="color:{theme['text_secondary']}; font-size:1.2rem; margin:0 0 0.5rem;">
            {"Tidak ada data yang cocok" if history_data else "Belum ada riwayat deteksi"}
        </h4>
        <p style="color:{theme['text_muted']}; font-size:0.88rem; margin:0;">
            {"Coba ubah filter di atas." if history_data else "Mulai deteksi di halaman Beranda untuk melihat riwayat di sini."}
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, h in enumerate(filtered):
        # Find the original index in riwayat_list for deletion
        orig_idx = None
        for i, item in enumerate(st.session_state.riwayat_list):
            if item is h:
                orig_idx = i
                break

        disease  = h.get("disease", "Tidak Diketahui")
        conf     = h.get("confidence", 0.0)
        status   = h.get("status", "Terdeteksi")
        date_obj = h.get("date", datetime.now())
        date_str = date_obj.strftime("%d %b %Y · %H:%M") if isinstance(date_obj, datetime) else str(date_obj)

        is_sehat     = (status == "Sehat")
        name_color   = theme['primary_light'] if is_sehat else theme['danger']
        badge_html   = f'<span class="badge-sehat">🟢 Sehat</span>' if is_sehat else f'<span class="badge-sakit">🔴 Terdeteksi</span>'
        conf_color   = theme['primary_light'] if is_sehat else "#FFB74D" if conf >= 60 else theme['danger']

        col_info, col_del = st.columns([10, 1], gap="small")

        with col_info:
            st.markdown(f"""
            <div class="riwayat-card">
                <div style="flex:1; min-width:0;">
                    <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.5rem; flex-wrap:wrap;">
                        <span style="font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:800;
                                     color:{name_color}; white-space:nowrap;">
                            {"🌿" if is_sehat else "🦠"} {disease}
                        </span>
                        {badge_html}
                    </div>
                    <div style="display:flex; gap:1.8rem; flex-wrap:wrap;">
                        <span style="font-size:0.85rem; color:{theme['text_secondary']};">
                            📊 Confidence: <strong style="color:{conf_color};">{conf:.1f}%</strong>
                        </span>
                        <span style="font-size:0.85rem; color:{theme['text_muted']};">
                            📅 {date_str} WIB
                        </span>
                    </div>
                </div>
                <div>
                    <!-- confidence bar -->
                    <div style="width:90px; height:5px; background:rgba(255,255,255,0.08);
                                border-radius:99px; overflow:hidden;">
                        <div style="height:5px; width:{min(conf,100):.0f}%; background:{conf_color};
                                    border-radius:99px; transition:width 0.5s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_del:
            st.markdown("<div style='height:0.9rem'></div>", unsafe_allow_html=True)
            if st.button("🗑", key=f"del_{idx}_{id(h)}", help="Hapus entri ini"):
                if orig_idx is not None:
                    st.session_state.riwayat_list.pop(orig_idx)
                    st.rerun()

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:3.5rem 0 1.5rem; border-top:1px solid {theme['border']};
            color:{theme['text_muted']}; font-size:0.85rem; margin-top:1rem;">
    🌾 <strong>PadiSense Premium v1.2</strong> | Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity:0.6; font-size:0.78rem;">© 2026 CAMP Batch 4 | Data Science &amp; Generative AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)