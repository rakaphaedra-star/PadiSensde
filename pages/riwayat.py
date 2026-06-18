import streamlit as st
from datetime import datetime
import theme_utils
import db_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Riwayat — PadiSense",
    page_icon="📋",
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
    border-radius:50px; font-size:0.8rem; font-weight:800;
    box-shadow:0 3px 10px rgba(76,175,80,0.3);
}}
.badge-sakit {{
    background: linear-gradient(135deg,#B71C1C,#EF5350);
    color:#fff; padding:0.35rem 1.1rem;
    border-radius:50px; font-size:0.8rem; font-weight:800;
    box-shadow:0 3px 10px rgba(239,83,80,0.3);
}}
.db-badge {{
    display:inline-flex; align-items:center; gap:0.4rem;
    font-size:0.72rem; padding:0.25rem 0.75rem;
    border-radius:20px; font-weight:700;
}}
</style>
""", unsafe_allow_html=True)

# ─── Wrapper ─────────────────────────────────────────────────────────────────
st.markdown('<div style="padding:0 2.5rem 3rem; max-width:1200px; margin:0 auto;">', unsafe_allow_html=True)

# ─── Page Header ─────────────────────────────────────────────────────────────
user_id = st.session_state.get("user_id", 0)
db_ok   = db_utils.test_connection() if user_id else False

db_badge_html = (
    '<span class="db-badge" style="background:rgba(105,240,174,0.1);'
    'border:1px solid rgba(105,240,174,0.25);color:#69F0AE;">🟢 Tersimpan di Database</span>'
    if db_ok else
    '<span class="db-badge" style="background:rgba(255,183,77,0.1);'
    'border:1px solid rgba(255,183,77,0.25);color:#FFB74D;">🟡 Mode Sesi Sementara</span>'
)

st.markdown(f"""
<div class="glass-card" style="padding:2.2rem 2.5rem !important;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
        <div>
            <h1 style="font-size:2.2rem;margin:0 0 0.4rem;color:{theme['text']};">📋 Riwayat Deteksi</h1>
            <p style="color:{theme['text_secondary']};margin:0;font-size:0.95rem;line-height:1.55;">
                Catatan seluruh hasil analisis penyakit daun padi Anda.
            </p>
        </div>
        {db_badge_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Ambil Data ───────────────────────────────────────────────────────────────
# Gabungkan sumber: DB (jika ada) + session state (fallback/tambahan)
if db_ok and user_id:
    db_stats = db_utils.get_scan_stats(user_id)
    total_scan  = db_stats["total"]
    total_sakit = db_stats["sakit"]
    total_sehat = db_stats["sehat"]
    avg_conf    = db_stats["avg_conf"]
else:
    # Hitung dari session state
    session_data = st.session_state.get("riwayat_list", [])
    total_scan  = len(session_data)
    total_sakit = sum(1 for h in session_data if h.get("status") == "Terdeteksi")
    total_sehat = sum(1 for h in session_data if h.get("status") == "Sehat")
    avg_conf    = (sum(h.get("confidence", 0) for h in session_data) / total_scan) if total_scan else 0

# ─── Statistics ──────────────────────────────────────────────────────────────
col_s1, col_s2, col_s3, col_s4 = st.columns(4, gap="medium")
for col, value, label in [
    (col_s1, total_scan,  "Total Analisis"),
    (col_s2, total_sakit, "Penyakit Terdeteksi"),
    (col_s3, total_sehat, "Tanaman Sehat"),
    (col_s4, f"{avg_conf:.0f}%", "Rata-rata Confidence"),
]:
    with col:
        st.markdown(f"""
        <div class="stat-badge">
            <div class="stat-badge-value">{value}</div>
            <div class="stat-badge-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ─── Filter Bar ──────────────────────────────────────────────────────────────
st.markdown('<div class="glass-card" style="padding:1.4rem 2rem !important; margin-bottom:1.5rem !important;">', unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns([1.2, 1.2, 0.8], gap="medium")

with col_f1:
    filter_status = st.selectbox("Filter Status", ["Semua", "Terdeteksi", "Sehat"], key="f_status")

with col_f2:
    if db_ok and user_id:
        diseases_list = db_utils.get_unique_diseases(user_id)
    else:
        session_data = st.session_state.get("riwayat_list", [])
        diseases_list = sorted(set(h.get("disease", "") for h in session_data if h.get("disease")))

    filter_disease = st.selectbox("Filter Penyakit", ["Semua"] + diseases_list, key="f_disease")

with col_f3:
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Semua", use_container_width=True, key="hapus_semua"):
        if db_ok and user_id:
            db_utils.delete_all_scans(user_id)
        st.session_state.riwayat_list = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── Ambil List Terfilter ─────────────────────────────────────────────────────
if db_ok and user_id:
    filtered_db = db_utils.get_scan_history(
        user_id,
        limit=200,
        filter_status=filter_status,
        filter_disease=filter_disease
    )
    # Konversi ke format seragam
    history_data = []
    for row in filtered_db:
        history_data.append({
            "_id":      row["id"],
            "disease":  row["disease_label"],
            "key":      row.get("disease_key", ""),
            "confidence": float(row["confidence"]),
            "status":   row["status"],
            "date":     row["scanned_at"],
            "source":   "db",
        })
else:
    # Dari session state
    raw = st.session_state.get("riwayat_list", [])
    filtered = raw
    if filter_status != "Semua":
        filtered = [h for h in filtered if h.get("status") == filter_status]
    if filter_disease != "Semua":
        filtered = [h for h in filtered if h.get("disease") == filter_disease]
    history_data = sorted(
        [{"_id": None, "disease": h.get("disease","?"), "key": "",
          "confidence": h.get("confidence", 0), "status": h.get("status","Terdeteksi"),
          "date": h.get("date", datetime.now()), "source": "session"}
         for h in filtered],
        key=lambda x: x["date"], reverse=True
    )

# ─── Render List ─────────────────────────────────────────────────────────────
if not history_data:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; padding:4rem 2rem !important;">
        <div style="font-size:3rem; margin-bottom:1rem; opacity:0.45;">📭</div>
        <h4 style="color:{theme['text_secondary']}; font-size:1.2rem; margin:0 0 0.5rem;">
            {"Tidak ada data yang cocok" if total_scan > 0 else "Belum ada riwayat deteksi"}
        </h4>
        <p style="color:{theme['text_muted']}; font-size:0.88rem; margin:0;">
            {"Coba ubah filter di atas." if total_scan > 0 else "Mulai deteksi di halaman Beranda untuk melihat riwayat di sini."}
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, h in enumerate(history_data):
        disease  = h["disease"]
        conf     = h["confidence"]
        status   = h["status"]
        date_obj = h["date"]
        date_str = date_obj.strftime("%d %b %Y · %H:%M") if isinstance(date_obj, datetime) else str(date_obj)

        is_sehat   = (status == "Sehat")
        name_color = theme['primary_light'] if is_sehat else theme['danger']
        badge_html = (
            '<span class="badge-sehat">🟢 Sehat</span>' if is_sehat
            else '<span class="badge-sakit">🔴 Terdeteksi</span>'
        )
        conf_color = theme['primary_light'] if is_sehat else ("#FFB74D" if conf >= 60 else theme['danger'])

        col_info, col_del = st.columns([10, 1], gap="small")

        with col_info:
            src_tag = (
                '<span style="font-size:0.65rem;color:#69F0AE;opacity:0.7;">💾 DB</span>'
                if h["source"] == "db" else
                '<span style="font-size:0.65rem;color:#FFB74D;opacity:0.7;">⚡ Sesi</span>'
            )
            st.markdown(f"""
            <div class="riwayat-card">
                <div style="flex:1; min-width:0;">
                    <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.5rem; flex-wrap:wrap;">
                        <span style="font-family:'Playfair Display',serif; font-size:1.1rem;
                                     font-weight:800; color:{name_color}; white-space:nowrap;">
                            {"🌿" if is_sehat else "🦠"} {disease}
                        </span>
                        {badge_html}
                        {src_tag}
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
                    <div style="width:90px; height:5px; background:rgba(255,255,255,0.08);
                                border-radius:99px; overflow:hidden;">
                        <div style="height:5px; width:{min(conf,100):.0f}%; background:{conf_color};
                                    border-radius:99px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_del:
            st.markdown("<div style='height:0.9rem'></div>", unsafe_allow_html=True)
            if st.button("🗑", key=f"del_{idx}_{h.get('_id','x')}", help="Hapus entri ini"):
                if h["source"] == "db" and h["_id"] and db_ok:
                    db_utils.delete_scan(h["_id"], user_id)
                else:
                    # Hapus dari session state
                    ss = st.session_state.get("riwayat_list", [])
                    st.session_state.riwayat_list = [
                        r for r in ss
                        if not (r.get("disease") == disease and
                                abs(r.get("confidence", 0) - conf) < 0.1)
                    ]
                st.rerun()

# ─── Login History Section ────────────────────────────────────────────────────
if db_ok and user_id:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.8rem; margin:1.5rem 0 1rem;">
        <div style="flex:1; height:1px; background:linear-gradient(90deg,{theme['border']},transparent);"></div>
        <span style="font-size:0.7rem; font-weight:800; text-transform:uppercase;
                     letter-spacing:0.15em; color:{theme['text_muted']};">Riwayat Login</span>
        <div style="flex:1; height:1px; background:linear-gradient(90deg,transparent,{theme['border']});"></div>
    </div>
    """, unsafe_allow_html=True)

    login_history = db_utils.get_login_history(user_id, limit=10)
    if login_history:
        st.markdown('<div class="glass-card" style="padding:1.4rem 1.8rem !important;">', unsafe_allow_html=True)
        for lh in login_history:
            action   = lh["action"]
            login_at = lh["login_at"]
            date_str = login_at.strftime("%d %b %Y · %H:%M") if isinstance(login_at, datetime) else str(login_at)
            icon     = "🔑" if action == "login" else "🚪"
            color    = "#69F0AE" if action == "login" else "#FFB74D"
            label    = "Masuk" if action == "login" else "Keluar"
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:0.6rem 0; border-bottom:1px solid {theme['border']};">
                <span style="font-size:0.88rem; color:{color}; font-weight:700;">
                    {icon} {label}
                </span>
                <span style="font-size:0.82rem; color:{theme['text_muted']};">📅 {date_str} WIB</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:3.5rem 0 1.5rem; border-top:1px solid {theme['border']};
            color:{theme['text_muted']}; font-size:0.85rem; margin-top:1rem;">
    🌾 <strong>PadiSense Premium v1.2</strong> | Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity:0.6; font-size:0.78rem;">© 2026 CAMP Batch 4 | Data Science &amp; Generative AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
