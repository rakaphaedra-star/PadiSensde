import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta, date
import theme_utils
import db_utils

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Grafik — PadiSense",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Theme ───────────────────────────────────────────────────────
theme_utils.check_auth()
theme    = theme_utils.THEMES[st.session_state.theme]
surf_rgb = theme["surface"]
card_rgb = theme.get("card_rgb", surf_rgb)
is_dark  = st.session_state.get("theme", "dark") == "dark"
theme_utils.inject_theme("grafik")

# ─── Plotly base template sesuai tema ────────────────────────────────────────
PLOTLY_TEMPLATE  = "plotly_dark" if is_dark else "plotly_white"
BG_COLOR         = theme["bg"]
PAPER_BG         = "rgba(14,24,12,0.0)" if is_dark else "rgba(240,247,236,0.0)"
GRID_COLOR       = "rgba(46,125,50,0.15)"
FONT_COLOR       = theme["text"]
COLOR_SEHAT      = "#4CAF50"
COLOR_SAKIT      = "#EF5350"
COLOR_GOLD       = theme["gold"]
COLOR_SECONDARY  = "#42A5F5"

# Palet warna untuk distribusi penyakit
DISEASE_COLORS = [
    "#EF5350","#FF7043","#FFB74D","#FFCA28",
    "#66BB6A","#26C6DA","#42A5F5","#7E57C2","#EC407A","#8D6E63",
]

# ─── Navbar ──────────────────────────────────────────────────────────────────
theme_utils.render_navbar("grafik")

# ─── Wrapper ─────────────────────────────────────────────────────────────────
st.markdown('<div style="padding:0 2.5rem 3rem; max-width:1300px; margin:0 auto;">', unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
user_id = st.session_state.get("user_id", 0)
db_ok   = db_utils.test_connection() if user_id else False

db_badge = (
    '<span style="background:rgba(105,240,174,0.1);border:1px solid rgba(105,240,174,0.25);'
    'color:#69F0AE;padding:0.3rem 0.9rem;border-radius:20px;font-size:0.72rem;font-weight:700;">🟢 Live DB</span>'
    if db_ok else
    '<span style="background:rgba(255,183,77,0.1);border:1px solid rgba(255,183,77,0.25);'
    'color:#FFB74D;padding:0.3rem 0.9rem;border-radius:20px;font-size:0.72rem;font-weight:700;">🟡 Sesi Sementara</span>'
)

st.markdown(f"""
<div class="glass-card" style="padding:2rem 2.5rem !important;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
        <div>
            <h1 style="font-size:2.2rem;margin:0 0 0.35rem;color:{theme['text']};">
                📈 Grafik Perkembangan Tanaman
            </h1>
            <p style="color:{theme['text_secondary']};margin:0;font-size:0.95rem;">
                Pantau tren kesehatan padi Anda — mingguan, bulanan, dan distribusi penyakit secara visual.
            </p>
        </div>
        {db_badge}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Periode Selector ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card" style="padding:1.2rem 2rem !important; margin-bottom:1.5rem !important;">
    <span style="font-size:0.8rem;font-weight:800;text-transform:uppercase;
                 letter-spacing:0.08em;color:{theme['text_secondary']};">⚙️ Rentang Waktu</span>
</div>
""", unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns([1,1,2], gap="medium")
with col_p1:
    periode = st.selectbox(
        "Pilih Periode",
        ["7 Hari Terakhir", "14 Hari Terakhir", "30 Hari Terakhir", "3 Bulan Terakhir"],
        key="periode_grafik",
        label_visibility="collapsed"
    )
with col_p2:
    periode_map = {
        "7 Hari Terakhir":   7,
        "14 Hari Terakhir":  14,
        "30 Hari Terakhir":  30,
        "3 Bulan Terakhir":  90,
    }
    n_days = periode_map[periode]
    st.markdown(
        f'<div style="padding:0.6rem 1rem;background:rgba(46,125,50,0.12);'
        f'border-radius:12px;font-size:0.88rem;color:{theme["text_secondary"]};margin-top:0.1rem;">'
        f'📅 {n_days} hari ke belakang dari hari ini</div>',
        unsafe_allow_html=True
    )

# ─── Ambil Data ──────────────────────────────────────────────────────────────
def get_trend_data(user_id, n_days, db_ok):
    """Ambil trend data dari DB atau session state sebagai fallback."""
    if db_ok and user_id:
        raw = db_utils.get_weekly_trend(user_id, n_days)
        rows = []
        for r in raw:
            rows.append({
                "tanggal": r["tanggal"] if isinstance(r["tanggal"], date) else r["tanggal"],
                "sehat":   int(r["sehat"] or 0),
                "sakit":   int(r["sakit"] or 0),
                "total":   int(r["total"] or 0),
            })
        return rows
    else:
        # Fallback dari session state
        cutoff = datetime.now() - timedelta(days=n_days)
        riwayat = [r for r in st.session_state.get("riwayat_list", [])
                   if r.get("date") and r["date"] >= cutoff]
        daily = {}
        for r in riwayat:
            d = r["date"].date() if hasattr(r["date"], "date") else r["date"]
            if d not in daily:
                daily[d] = {"sehat": 0, "sakit": 0, "total": 0}
            if r.get("status") == "Sehat":
                daily[d]["sehat"] += 1
            else:
                daily[d]["sakit"] += 1
            daily[d]["total"] += 1
        return [{"tanggal": k, "sehat": v["sehat"], "sakit": v["sakit"], "total": v["total"]}
                for k, v in sorted(daily.items())]

def get_disease_data(user_id, n_days, db_ok):
    """Ambil distribusi penyakit."""
    if db_ok and user_id:
        raw = db_utils.get_disease_distribution(user_id, n_days)
        return [{"disease_label": r["disease_label"], "jumlah": int(r["jumlah"])} for r in raw]
    else:
        cutoff = datetime.now() - timedelta(days=n_days)
        riwayat = [r for r in st.session_state.get("riwayat_list", [])
                   if r.get("date") and r["date"] >= cutoff
                   and r.get("status") == "Terdeteksi"]
        counts = {}
        for r in riwayat:
            d = r.get("disease", "Tidak Diketahui")
            counts[d] = counts.get(d, 0) + 1
        return [{"disease_label": k, "jumlah": v}
                for k, v in sorted(counts.items(), key=lambda x: -x[1])]

def get_summary_data(user_id, db_ok):
    """Ringkasan minggu ini vs minggu lalu."""
    if db_ok and user_id:
        return db_utils.get_weekly_summary(user_id)
    else:
        now = datetime.now()
        wk_start = now - timedelta(days=7)
        wk2_start = now - timedelta(days=14)
        riwayat = st.session_state.get("riwayat_list", [])
        def count_status(lst, start, end, status):
            return sum(1 for r in lst
                       if r.get("date") and start <= r["date"] <= end
                       and r.get("status") == status)
        return {
            "minggu_ini_sehat":  count_status(riwayat, wk_start, now, "Sehat"),
            "minggu_ini_sakit":  count_status(riwayat, wk_start, now, "Terdeteksi"),
            "minggu_lalu_sehat": count_status(riwayat, wk2_start, wk_start, "Sehat"),
            "minggu_lalu_sakit": count_status(riwayat, wk2_start, wk_start, "Terdeteksi"),
        }

trend_rows   = get_trend_data(user_id, n_days, db_ok)
disease_rows = get_disease_data(user_id, n_days, db_ok)
summary      = get_summary_data(user_id, db_ok)

# ─── Helper: fill date gaps ───────────────────────────────────────────────────
def fill_date_range(rows, n_days):
    """Isi tanggal yang kosong dengan nilai 0 agar grafik tidak terputus."""
    today = date.today()
    all_dates = {today - timedelta(days=i): {"sehat": 0, "sakit": 0, "total": 0}
                 for i in range(n_days - 1, -1, -1)}
    for r in rows:
        d = r["tanggal"] if isinstance(r["tanggal"], date) else r["tanggal"]
        if d in all_dates:
            all_dates[d] = {"sehat": r["sehat"], "sakit": r["sakit"], "total": r["total"]}
    return [{"tanggal": k, **v} for k, v in sorted(all_dates.items())]

trend_full = fill_date_range(trend_rows, n_days)
df_trend   = pd.DataFrame(trend_full)

# ─── KPI Ringkasan Mingguan ──────────────────────────────────────────────────
st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

def delta_badge(now_val, prev_val, good_direction="up"):
    """Buat badge perubahan % minggu vs minggu lalu."""
    if prev_val == 0:
        return '<span style="color:#FFB74D;font-size:0.78rem;font-weight:700;">— Baru</span>'
    delta = now_val - prev_val
    pct   = abs(delta / prev_val * 100)
    if delta == 0:
        return f'<span style="color:#90A4AE;font-size:0.78rem;font-weight:700;">→ Sama</span>'
    arrow  = "↑" if delta > 0 else "↓"
    is_good = (delta > 0) == (good_direction == "up")
    color  = COLOR_SEHAT if is_good else COLOR_SAKIT
    return f'<span style="color:{color};font-size:0.78rem;font-weight:800;">{arrow} {pct:.0f}% vs minggu lalu</span>'

total_sehat_period = df_trend["sehat"].sum()
total_sakit_period = df_trend["sakit"].sum()
total_all_period   = df_trend["total"].sum()
pct_sehat = (total_sehat_period / total_all_period * 100) if total_all_period > 0 else 0

kpi_cols = st.columns(4, gap="medium")
kpi_data = [
    ("🌿", str(summary.get("minggu_ini_sehat", 0)), "Sehat Minggu Ini",
     delta_badge(summary.get("minggu_ini_sehat",0), summary.get("minggu_lalu_sehat",0), "up"),
     COLOR_SEHAT),
    ("🦠", str(summary.get("minggu_ini_sakit", 0)), "Sakit Minggu Ini",
     delta_badge(summary.get("minggu_ini_sakit",0), summary.get("minggu_lalu_sakit",0), "down"),
     COLOR_SAKIT),
    ("📊", str(int(total_all_period)), f"Total Scan ({n_days}h)",
     f'<span style="color:{theme["text_muted"]};font-size:0.78rem;">dalam periode ini</span>',
     COLOR_GOLD),
    ("✅", f"{pct_sehat:.1f}%", "Rasio Tanaman Sehat",
     f'<span style="color:{theme["text_muted"]};font-size:0.78rem;">dari semua scan</span>',
     COLOR_SECONDARY),
]

for col, (icon, val, label, badge, accent) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="stat-badge" style="border-left:4px solid {accent} !important;
             padding:1.4rem 1.2rem !important; text-align:left !important;">
            <div style="font-size:1.5rem;margin-bottom:0.3rem;">{icon}</div>
            <div style="font-family:'Playfair Display',serif;font-size:2rem;
                        font-weight:900;color:{accent};line-height:1.1;">{val}</div>
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.08em;color:{theme['text_secondary']};
                        margin:0.3rem 0 0.4rem;">{label}</div>
            {badge}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─── CHART 1: Line Chart Sehat vs Sakit ──────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.8rem;margin:0.5rem 0 1rem;">
    <div style="width:4px;height:28px;background:linear-gradient(180deg,{COLOR_SEHAT},{COLOR_GOLD});
                border-radius:2px;"></div>
    <h3 style="margin:0;font-size:1.3rem;color:{theme['text']};">
        Tren Harian: Tanaman Sehat vs Sakit
    </h3>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="glass-card" style="padding:1.5rem 1.8rem !important;">', unsafe_allow_html=True)

if df_trend["total"].sum() == 0:
    st.markdown(f"""
    <div style="text-align:center;padding:4rem 2rem;">
        <div style="font-size:3rem;opacity:0.35;margin-bottom:1rem;">📭</div>
        <p style="color:{theme['text_muted']};font-size:0.95rem;">
            Belum ada data scan dalam periode ini.<br>
            Mulai deteksi tanaman padi di halaman Beranda!
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Format label tanggal
    labels = [d.strftime("%d %b") for d in df_trend["tanggal"]]

    fig_line = go.Figure()

    # Area Sehat
    fig_line.add_trace(go.Scatter(
        x=labels, y=df_trend["sehat"].tolist(),
        name="🌿 Sehat",
        mode="lines+markers",
        line=dict(color=COLOR_SEHAT, width=3, shape="spline"),
        marker=dict(size=7, color=COLOR_SEHAT,
                    line=dict(color="white", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(76,175,80,0.12)",
        hovertemplate="<b>%{x}</b><br>Sehat: %{y} tanaman<extra></extra>",
    ))

    # Area Sakit
    fig_line.add_trace(go.Scatter(
        x=labels, y=df_trend["sakit"].tolist(),
        name="🦠 Terdeteksi Penyakit",
        mode="lines+markers",
        line=dict(color=COLOR_SAKIT, width=3, shape="spline"),
        marker=dict(size=7, color=COLOR_SAKIT,
                    line=dict(color="white", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(239,83,80,0.10)",
        hovertemplate="<b>%{x}</b><br>Sakit: %{y} tanaman<extra></extra>",
    ))

    fig_line.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PAPER_BG,
        height=340,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0,
            font=dict(color=FONT_COLOR, size=12),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=theme["text_muted"], size=11),
            tickangle=-30 if n_days > 14 else 0,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            tickfont=dict(color=theme["text_muted"], size=11),
            rangemode="tozero",
        ),
        hoverlabel=dict(
            bgcolor="rgba(14,24,12,0.9)",
            font=dict(color="white", size=12),
            bordercolor=COLOR_SEHAT,
        ),
        font=dict(family="Plus Jakarta Sans, sans-serif", color=FONT_COLOR),
    )
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

st.markdown('</div>', unsafe_allow_html=True)

# ─── CHART 2 & 3: Pie + Bar berdampingan ─────────────────────────────────────
col_left, col_right = st.columns([1, 1.2], gap="large")

# ── Pie Chart Distribusi Penyakit ─────────────────────────────────────────────
with col_left:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.8rem;margin:0.5rem 0 1rem;">
        <div style="width:4px;height:28px;background:linear-gradient(180deg,{COLOR_SAKIT},#FF7043);
                    border-radius:2px;"></div>
        <h3 style="margin:0;font-size:1.15rem;color:{theme['text']};">
            Distribusi Jenis Penyakit
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="glass-card" style="padding:1.5rem 1.5rem !important;">', unsafe_allow_html=True)

    if not disease_rows:
        st.markdown(f"""
        <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:2.5rem;opacity:0.35;margin-bottom:0.8rem;">🦠</div>
            <p style="color:{theme['text_muted']};font-size:0.88rem;margin:0;">
                Belum ada penyakit terdeteksi<br>dalam periode ini.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        labels_pie = [r["disease_label"] for r in disease_rows]
        values_pie = [r["jumlah"] for r in disease_rows]
        colors_pie = DISEASE_COLORS[:len(labels_pie)]

        fig_pie = go.Figure(go.Pie(
            labels=labels_pie,
            values=values_pie,
            hole=0.52,
            marker=dict(colors=colors_pie,
                        line=dict(color="rgba(255,255,255,0.06)", width=2)),
            textinfo="percent",
            textfont=dict(size=11, color="white"),
            hovertemplate="<b>%{label}</b><br>%{value} kasus (%{percent})<extra></extra>",
            pull=[0.04 if i == 0 else 0 for i in range(len(labels_pie))],
        ))

        fig_pie.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=PAPER_BG,
            height=320,
            margin=dict(l=0, r=0, t=10, b=10),
            showlegend=True,
            legend=dict(
                orientation="v", x=1.01, y=0.5,
                font=dict(color=FONT_COLOR, size=10),
                bgcolor="rgba(0,0,0,0)",
            ),
            annotations=[dict(
                text=f"<b>{sum(values_pie)}</b><br><span style='font-size:9px'>Kasus</span>",
                x=0.5, y=0.5, font=dict(size=16, color=FONT_COLOR),
                showarrow=False,
            )],
            font=dict(family="Plus Jakarta Sans, sans-serif", color=FONT_COLOR),
            hoverlabel=dict(bgcolor="rgba(14,24,12,0.9)", font=dict(color="white", size=12)),
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    st.markdown('</div>', unsafe_allow_html=True)

# ── Bar Chart Top Penyakit ────────────────────────────────────────────────────
with col_right:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.8rem;margin:0.5rem 0 1rem;">
        <div style="width:4px;height:28px;background:linear-gradient(180deg,{COLOR_GOLD},{COLOR_SECONDARY});
                    border-radius:2px;"></div>
        <h3 style="margin:0;font-size:1.15rem;color:{theme['text']};">
            Ranking Penyakit Terbanyak
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="glass-card" style="padding:1.5rem 1.5rem !important;">', unsafe_allow_html=True)

    if not disease_rows:
        st.markdown(f"""
        <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:2.5rem;opacity:0.35;margin-bottom:0.8rem;">📊</div>
            <p style="color:{theme['text_muted']};font-size:0.88rem;margin:0;">
                Tidak ada data penyakit<br>untuk ditampilkan.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Top 7 penyakit
        top_rows = disease_rows[:7]
        bar_labels = [r["disease_label"] for r in top_rows]
        bar_values = [r["jumlah"] for r in top_rows]
        bar_colors = DISEASE_COLORS[:len(bar_labels)]

        # Bar horizontal
        fig_bar = go.Figure(go.Bar(
            y=bar_labels,
            x=bar_values,
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(color="rgba(255,255,255,0.0)", width=0),
            ),
            text=[str(v) + " kasus" for v in bar_values],
            textposition="outside",
            textfont=dict(color=FONT_COLOR, size=11),
            hovertemplate="<b>%{y}</b><br>%{x} kasus terdeteksi<extra></extra>",
        ))

        fig_bar.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor=PAPER_BG,
            plot_bgcolor=PAPER_BG,
            height=320,
            margin=dict(l=0, r=60, t=10, b=10),
            xaxis=dict(
                showgrid=True, gridcolor=GRID_COLOR,
                tickfont=dict(color=theme["text_muted"], size=10),
                zeroline=False,
            ),
            yaxis=dict(
                tickfont=dict(color=FONT_COLOR, size=10),
                autorange="reversed",
            ),
            font=dict(family="Plus Jakarta Sans, sans-serif", color=FONT_COLOR),
            hoverlabel=dict(bgcolor="rgba(14,24,12,0.9)", font=dict(color="white", size=12)),
            bargap=0.28,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown('</div>', unsafe_allow_html=True)

# ─── CHART 4: Stacked Bar per Minggu ─────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.8rem;margin:0.5rem 0 1rem;">
    <div style="width:4px;height:28px;background:linear-gradient(180deg,{COLOR_SECONDARY},{COLOR_SEHAT});
                border-radius:2px;"></div>
    <h3 style="margin:0;font-size:1.3rem;color:{theme['text']};">
        Perbandingan Mingguan (Stacked Bar)
    </h3>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="glass-card" style="padding:1.5rem 1.8rem !important;">', unsafe_allow_html=True)

# Agregasi per minggu
if df_trend["total"].sum() == 0:
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 2rem;">
        <div style="font-size:2.5rem;opacity:0.35;margin-bottom:0.8rem;">📅</div>
        <p style="color:{theme['text_muted']};font-size:0.88rem;">
            Belum cukup data untuk ditampilkan dalam grafik mingguan.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Buat kolom minggu
    df_trend_copy = df_trend.copy()
    df_trend_copy["tanggal"] = pd.to_datetime(df_trend_copy["tanggal"])
    df_trend_copy["minggu"]  = df_trend_copy["tanggal"].dt.to_period("W").apply(
        lambda p: f"Mgg {p.start_time.strftime('%d/%m')}"
    )
    df_weekly = df_trend_copy.groupby("minggu", sort=False).agg(
        sehat=("sehat", "sum"),
        sakit=("sakit", "sum"),
    ).reset_index()

    fig_stack = go.Figure()

    fig_stack.add_trace(go.Bar(
        name="🌿 Sehat",
        x=df_weekly["minggu"].tolist(),
        y=df_weekly["sehat"].tolist(),
        marker_color=COLOR_SEHAT,
        marker_line=dict(color="rgba(255,255,255,0.05)", width=1),
        hovertemplate="<b>%{x}</b><br>Sehat: %{y} tanaman<extra></extra>",
    ))

    fig_stack.add_trace(go.Bar(
        name="🦠 Sakit",
        x=df_weekly["minggu"].tolist(),
        y=df_weekly["sakit"].tolist(),
        marker_color=COLOR_SAKIT,
        marker_line=dict(color="rgba(255,255,255,0.05)", width=1),
        hovertemplate="<b>%{x}</b><br>Sakit: %{y} tanaman<extra></extra>",
    ))

    fig_stack.update_layout(
        barmode="group",
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PAPER_BG,
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(color=FONT_COLOR, size=12),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=theme["text_muted"], size=11),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            tickfont=dict(color=theme["text_muted"], size=11),
            rangemode="tozero",
        ),
        bargap=0.2,
        bargroupgap=0.08,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=FONT_COLOR),
        hoverlabel=dict(bgcolor="rgba(14,24,12,0.9)", font=dict(color="white", size=12)),
    )
    st.plotly_chart(fig_stack, use_container_width=True, config={"displayModeBar": False})

st.markdown('</div>', unsafe_allow_html=True)

# ─── CHART 5: Tabel Ringkasan Periode ────────────────────────────────────────
if df_trend["total"].sum() > 0:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.8rem;margin:0.5rem 0 1rem;">
        <div style="width:4px;height:28px;background:linear-gradient(180deg,{COLOR_GOLD},{COLOR_SAKIT});
                    border-radius:2px;"></div>
        <h3 style="margin:0;font-size:1.3rem;color:{theme['text']};">
            Tabel Detail Harian
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="glass-card" style="padding:1.2rem 1.5rem !important;">', unsafe_allow_html=True)

    # Hanya tampilkan hari yang ada datanya
    df_show = df_trend[df_trend["total"] > 0].copy()
    df_show["tanggal_str"] = pd.to_datetime(df_show["tanggal"]).dt.strftime("%A, %d %B %Y")
    df_show["rasio_sehat"] = df_show.apply(
        lambda r: f"{r['sehat']/r['total']*100:.0f}%" if r["total"] > 0 else "—", axis=1
    )
    df_show = df_show.rename(columns={
        "tanggal_str": "📅 Tanggal",
        "sehat":       "🌿 Sehat",
        "sakit":       "🦠 Sakit",
        "total":       "📊 Total",
        "rasio_sehat": "✅ Rasio Sehat",
    })[["📅 Tanggal", "🌿 Sehat", "🦠 Sakit", "📊 Total", "✅ Rasio Sehat"]]

    # Tampilkan hanya 10 baris terakhir
    st.dataframe(
        df_show.tail(14).iloc[::-1].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Insight Card ────────────────────────────────────────────────────────────
if df_trend["total"].sum() > 0:
    total_s  = int(df_trend["sehat"].sum())
    total_k  = int(df_trend["sakit"].sum())
    top_penyakit = disease_rows[0]["disease_label"] if disease_rows else "—"
    insight_color = COLOR_SEHAT if total_s >= total_k else COLOR_SAKIT
    insight_icon  = "🌿" if total_s >= total_k else "⚠️"
    insight_msg   = (
        f"Kondisi tanaman Anda <strong>cukup baik</strong> dalam {n_days} hari terakhir. "
        f"Dari <strong>{total_s + total_k}</strong> scan, <strong>{total_s}</strong> menunjukkan tanaman sehat "
        f"({pct_sehat:.0f}%). Tetap pantau perkembangan secara rutin!"
        if total_s >= total_k else
        f"Perhatian! Dalam {n_days} hari terakhir, <strong>{total_k}</strong> dari <strong>{total_s + total_k}</strong> scan "
        f"mendeteksi penyakit ({100-pct_sehat:.0f}%). Penyakit dominan: <strong>{top_penyakit}</strong>. "
        f"Segera konsultasikan dengan PadiBot!"
    )

    st.markdown(f"""
    <div class="glass-card" style="
        border-left: 5px solid {insight_color} !important;
        background: linear-gradient(135deg, rgba(14,24,12,0.8) 0%, rgba(46,125,50,0.05) 100%) !important;
        padding:1.5rem 2rem !important;">
        <div style="display:flex;align-items:flex-start;gap:1rem;">
            <div style="font-size:2rem;line-height:1;">{insight_icon}</div>
            <div>
                <p style="font-size:0.82rem;font-weight:800;text-transform:uppercase;
                           letter-spacing:0.1em;color:{insight_color};margin:0 0 0.4rem;">
                    💡 Insight Otomatis
                </p>
                <p style="color:{theme['text_secondary']};line-height:1.65;margin:0;font-size:0.95rem;">
                    {insight_msg}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:3rem 0 1.5rem;border-top:1px solid {theme['border']};
            color:{theme['text_muted']};font-size:0.85rem;margin-top:1rem;">
    🌾 <strong>PadiSense Premium v1.2</strong> | Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity:0.6;font-size:0.78rem;">© 2026 CAMP Batch 4 | Data Science &amp; Generative AI</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
