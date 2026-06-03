import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import tempfile
import os
from datetime import datetime
from google import genai
import theme_utils

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PadiSense — Beranda",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Auth Guard & Theme ───────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "detected_diseases" not in st.session_state:
    st.session_state.detected_diseases = []
if "riwayat_list" not in st.session_state:
    st.session_state.riwayat_list = []

# ─── Page-level CSS ───────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Upload zone ── */
[data-testid="stFileUploader"] {{
    background: rgba({surf_rgb}, 0.45) !important;
    border: 2px dashed {theme['border']} !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    transition: all 0.25s ease !important;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: {theme['primary_light']} !important;
    background: rgba({surf_rgb}, 0.65) !important;
}}
[data-testid="stFileUploader"] label   {{ color: {theme['text_secondary']} !important; }}
[data-testid="stFileUploader"] section {{ background: transparent !important; border: none !important; }}
[data-testid="stFileUploader"] button  {{
    background: rgba({surf_rgb}, 0.9) !important;
    color: {theme['primary_light']} !important;
    border: 1px solid {theme['border']} !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] label {{
    color: {theme['text_secondary']} !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}}

/* ── Image ── */
[data-testid="stImage"] img {{
    border-radius: 14px !important;
    border: 1px solid {theme['border']} !important;
}}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: {theme['primary_light']} !important; }}

/* ── Caption ── */
.stCaption, [data-testid="stCaptionContainer"] p {{
    color: {theme['text_muted']} !important;
    font-size: 0.74rem !important;
}}

/* ── Disease cards ── */
.dcard {{
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 0.9rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease;
}}
.dcard::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 5px; height: 100%;
    border-radius: 5px 0 0 5px;
}}
.dcard:hover {{ transform: translateX(5px); }}
.dcard.danger  {{ background: rgba(239,83,80,0.08);   border: 1px solid rgba(239,83,80,0.22); }}
.dcard.warning {{ background: rgba(255,183,77,0.08);  border: 1px solid rgba(255,183,77,0.22); }}
.dcard.healthy {{ background: rgba(105,240,174,0.08); border: 1px solid rgba(105,240,174,0.22); }}
.dcard.danger::before  {{ background: #EF5350; box-shadow: 0 0 8px rgba(239,83,80,0.55); }}
.dcard.warning::before {{ background: #FFB74D; box-shadow: 0 0 8px rgba(255,183,77,0.55); }}
.dcard.healthy::before {{ background: #69F0AE; box-shadow: 0 0 8px rgba(105,240,174,0.55); }}

.dcard-name {{ font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; }}
.dcard.danger  .dcard-name {{ color: #EF5350; }}
.dcard.warning .dcard-name {{ color: #FFB74D; }}
.dcard.healthy .dcard-name {{ color: #69F0AE; }}

.dcard-conf {{
    font-size: 0.76rem; padding: 0.2rem 0.6rem;
    border-radius: 6px; font-weight: 700;
}}
.dcard.danger  .dcard-conf {{ background: rgba(239,83,80,0.15);   color: #EF5350; }}
.dcard.warning .dcard-conf {{ background: rgba(255,183,77,0.15);  color: #FFB74D; }}
.dcard.healthy .dcard-conf {{ background: rgba(105,240,174,0.15); color: #69F0AE; }}

.pbar-bg {{
    background: rgba(255,255,255,0.06);
    border-radius: 99px; height: 5px;
    margin: 0.55rem 0 0.75rem; overflow: hidden;
}}
.pbar-fill {{ height: 5px; border-radius: 99px; transition: width 0.6s ease; }}
.danger  .pbar-fill {{ background: linear-gradient(90deg,#B71C1C,#EF5350); }}
.warning .pbar-fill {{ background: linear-gradient(90deg,#E65100,#FFB74D); }}
.healthy .pbar-fill {{ background: linear-gradient(90deg,#1B5E20,#69F0AE); }}

.dcard-desc {{ color: {theme['text_secondary']}; font-size: 0.87rem; line-height: 1.65; margin-bottom: 0.75rem; }}
.dcard-treatment {{
    border-radius: 10px; padding: 0.7rem 1rem;
    font-size: 0.84rem; line-height: 1.6;
}}
.danger  .dcard-treatment {{ background:rgba(239,83,80,0.07);  border:1px solid rgba(239,83,80,0.18);  color:#FFCDD2; }}
.warning .dcard-treatment {{ background:rgba(255,183,77,0.07); border:1px solid rgba(255,183,77,0.18); color:#FFE0B2; }}
.healthy .dcard-treatment {{ background:rgba(105,240,174,0.07);border:1px solid rgba(105,240,174,0.18);color:#B9F6CA; }}
.dcard-treatment b {{ font-weight: 700; display: block; margin-bottom: 0.2rem; }}

/* ── Section label ── */
.sec-label {{
    font-size: 0.7rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.13em;
    color: {theme['text_muted']};
    display: flex; align-items: center; gap: 0.45rem;
    margin-bottom: 0.75rem;
}}
.sec-label::before {{
    content: ''; display: inline-block;
    width: 20px; height: 2px;
    background: {theme['primary_light']}; border-radius: 2px;
}}

/* ── Chat bubbles ── */
.chat-wrap {{
    background: rgba({surf_rgb}, 0.4);
    border: 1px solid {theme['border']};
    border-radius: 18px; padding: 1.4rem;
    margin-top: 0.5rem;
}}
.msg-user {{
    background: linear-gradient(135deg,{theme['primary']} 0%,{theme['primary_light']} 100%);
    border-radius: 14px 14px 2px 14px;
    padding: 0.8rem 1.1rem; margin: 0.4rem 0 0.4rem 2.5rem;
    color: white; font-size: 0.9rem; line-height: 1.6;
}}
.msg-bot {{
    background: rgba({card_rgb}, 0.85);
    border: 1px solid {theme['border']};
    border-radius: 14px 14px 14px 2px;
    padding: 0.8rem 1.1rem; margin: 0.4rem 2.5rem 0.4rem 0;
    color: {theme['text']}; font-size: 0.9rem; line-height: 1.6;
}}
.msg-label {{
    font-size: 0.65rem; color: {theme['text_muted']};
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 0.2rem; font-weight: 700;
}}

/* ── Hero stats chip ── */
.hero-chip {{
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba({surf_rgb}, 0.6);
    border: 1px solid {theme['border']};
    border-radius: 50px; padding: 0.3rem 0.85rem;
    font-size: 0.78rem; color: {theme['text_secondary']};
    font-weight: 600;
}}

/* ── Feature pill ── */
.feat-pill {{
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: rgba(46,125,50,0.12);
    border: 1px solid rgba(46,125,50,0.28);
    border-radius: 8px; padding: 0.45rem 0.85rem;
    font-size: 0.82rem; font-weight: 600;
    color: {theme['primary_light']};
    margin: 0 0.3rem 0.3rem 0;
}}

/* ── Empty state ── */
.empty-state {{
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 3.5rem 1.5rem; text-align: center;
    background: rgba({surf_rgb}, 0.3);
    border: 2px dashed {theme['border']};
    border-radius: 18px;
    min-height: 280px;
}}
</style>
""", unsafe_allow_html=True)

# ─── Disease Info Database ────────────────────────────────────────────────────
DISEASE_INFO = {
    'Rice__BacterialLeafBlight': {
        'label': 'Hawar Daun Bakteri',
        'severity': 'danger',
        'desc': 'Infeksi bakteri Xanthomonas oryzae pv. oryzae yang menyebabkan daun menguning dan mengering dari tepi.',
        'treatment': 'Gunakan varietas tahan, kurangi penggunaan pupuk nitrogen, semprot bakterisida berbahan tembaga (copper oxychloride).',
    },
    'Rice__BrownSpot': {
        'label': 'Bercak Coklat',
        'severity': 'warning',
        'desc': 'Disebabkan jamur Bipolaris oryzae, muncul bercak oval coklat di daun. Sering terjadi pada lahan kekurangan nutrisi.',
        'treatment': 'Perbaiki nutrisi tanah (terutama kalium), semprot fungisida berbahan mancozeb atau iprodione.',
    },
    'Rice__Healthy': {
        'label': 'Tanaman Sehat',
        'severity': 'healthy',
        'desc': 'Daun padi terlihat sehat, tidak menunjukkan gejala penyakit.',
        'treatment': 'Pertahankan kondisi lahan: irigasi teratur, pemupukan sesuai dosis, dan pemantauan rutin.',
    },
    'Rice__Hispa': {
        'label': 'Hispa (Kumbang Daun)',
        'severity': 'warning',
        'desc': 'Serangan hama Dicladispa armigera yang mengikis jaringan daun, meninggalkan bekas putih memanjang.',
        'treatment': 'Cabut dan musnahkan daun terserang, semprotkan insektisida karbofuran atau klorpirifos pada pagi hari.',
    },
    'Rice__LeafBlast': {
        'label': 'Blast Daun',
        'severity': 'danger',
        'desc': 'Penyakit jamur Magnaporthe oryzae yang sangat merusak, membentuk bercak berlian abu-abu di daun.',
        'treatment': 'Gunakan varietas tahan blast, semprot fungisida propikonazol atau trisiklazol sesegera mungkin.',
    },
    'Rice__LeafScald': {
        'label': 'Gosong Daun',
        'severity': 'warning',
        'desc': 'Disebabkan jamur Microdochium oryzae, daun terlihat terbakar/gosong dari ujung ke pangkal.',
        'treatment': 'Semprot fungisida berbahan aktif iprodione, hindari kelebihan pupuk nitrogen.',
    },
    'Rice__LeafSmut': {
        'label': 'Gosong Palsu Daun',
        'severity': 'warning',
        'desc': 'Penyakit jamur yang membentuk massa spora hitam kecil di permukaan daun.',
        'treatment': 'Semprot fungisida berbahan tembaga, pastikan drainase lahan baik untuk mengurangi kelembaban.',
    },
    'Rice__NarrowBrownLeafSpot': {
        'label': 'Bercak Sempit Coklat',
        'severity': 'warning',
        'desc': 'Bercak coklat sempit dan panjang akibat jamur Cercospora janseana, umumnya pada fase pengisian bulir.',
        'treatment': 'Semprot fungisida propikonazol, jaga sirkulasi air lahan tetap baik.',
    },
    'Rice__NeckBlast': {
        'label': 'Blast Leher Malai',
        'severity': 'danger',
        'desc': 'Serangan blast paling kritis — menyerang leher malai sehingga bulir menjadi hampa dan gagal panen.',
        'treatment': 'SEGERA semprot trisiklazol atau isoprothiolane. Ini darurat — penanganan terlambat bisa gagal panen total.',
    },
}

# ─── Load Model ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# ─── Gemini Config ───────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBsFZF6UtgNqMLh9XPC5SdPhTYAl7iDN8w")

def get_system_prompt(detected_diseases: list) -> str:
    if not detected_diseases:
        base_context = "Belum ada penyakit yang terdeteksi. User mungkin belum upload gambar."
    else:
        disease_list = "\n".join([f"- {d}" for d in detected_diseases])
        base_context = f"Penyakit yang terdeteksi pada gambar:\n{disease_list}"
    return f"""Kamu adalah asisten ahli pertanian padi bernama PadiBot, bagian dari sistem PadiSense.
Tugasmu membantu petani atau peneliti memahami dan menangani penyakit tanaman padi.

Konteks deteksi saat ini:
{base_context}

Panduan menjawab:
- Jawab dalam Bahasa Indonesia yang jelas dan mudah dipahami petani
- Fokus pada penyakit yang terdeteksi di atas
- Berikan informasi praktis: penyebab, gejala, pencegahan, penanganan
- Kalau ditanya soal pestisida/fungisida, sebutkan nama bahan aktifnya
- Jaga jawaban tetap ringkas tapi lengkap (maks 3-4 paragraf)
- Gunakan format list/bullet kalau membantu kejelasan"""

def chat_with_gemini(user_message: str, detected_diseases: list) -> str:
    if not GEMINI_API_KEY:
        return "⚠️ API key Gemini belum diset."
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        system_prompt = get_system_prompt(detected_diseases)
        history_text = ""
        for msg in st.session_state.chat_history:
            role = "User" if msg["role"] == "user" else "PadiBot"
            history_text += f"{role}: {msg['content']}\n"
        full_prompt = f"{system_prompt}\n\n{history_text}User: {user_message}\nPadiBot:"
        response = client.models.generate_content(model="gemini-2.5-flash", contents=full_prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "API_KEY_INVALID" in err or "API key not valid" in err:
            return "⚠️ API key tidak valid. Cek kembali di aistudio.google.com"
        elif "quota" in err.lower() or "429" in err:
            return "⚠️ Rate limit tercapai. Tunggu 1 menit lalu coba lagi."
        else:
            return f"⚠️ Error: {err}"

# ═══════════════════════════════════════════════════════════════════════════════
# ─── NAVBAR ───────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
theme_utils.render_navbar("beranda")

# ─── Outer wrapper ───────────────────────────────────────────────────────────
st.markdown('<div style="padding:0 2rem 4rem; max-width:1440px; margin:0 auto;">', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── HERO SECTION ─────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
col_hero, col_stats = st.columns([1.6, 1], gap="large")

with col_hero:
    _hero = (
        f'<div class="glass-card" style="padding:2.4rem 2.6rem !important;'
        f'background:linear-gradient(135deg,rgba({surf_rgb},0.9) 0%,rgba(46,125,50,0.07) 100%) !important;min-height:235px;">'
        f'<div style="display:inline-block;background:rgba(46,125,50,0.15);border:1px solid {theme["border"]};'
        f'color:{theme["primary_light"]};font-size:0.64rem;letter-spacing:0.16em;padding:0.22rem 0.8rem;'
        f'border-radius:20px;margin-bottom:1rem;font-weight:800;text-transform:uppercase;">'
        f'YOLOv8n &nbsp;&middot;&nbsp; Computer Vision &nbsp;&middot;&nbsp; Agritech AI</div>'
        f'<h1 style="font-family:Playfair Display,serif;font-size:2.6rem;font-weight:900;'
        f'margin:0 0 0.45rem;line-height:1.08;color:{theme["text"]};">'
        f'&#127806; Padi<span style="color:{theme["gold"]};">Sense</span></h1>'
        f'<p style="color:{theme["text_secondary"]};font-size:0.95rem;line-height:1.65;margin:0 0 1.5rem;max-width:470px;">'
        f'Sistem deteksi penyakit daun padi berbasis <strong>deep learning</strong> &mdash; '
        f'upload foto, dapatkan diagnosis instan &amp; rekomendasi penanganan dari pakar AI.</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
        f'<span class="feat-pill">&#128300; 9 Kelas Penyakit</span>'
        f'<span class="feat-pill">&#128202; 63.4% mAP@50</span>'
        f'<span class="feat-pill">&#129302; PadiBot AI</span>'
        f'<span class="feat-pill">&#9889; Real-time</span>'
        f'</div></div>'
    )
    st.markdown(_hero, unsafe_allow_html=True)

with col_stats:
    riwayat_all = st.session_state.get("riwayat_list", [])
    total_scan  = len(riwayat_all)
    total_sakit = sum(1 for r in riwayat_all if r.get("status") == "Terdeteksi")
    total_sehat = sum(1 for r in riwayat_all if r.get("status") == "Sehat")
    user_name   = st.session_state.get("current_user", "Petani")
    # Pre-compute to avoid nested f-string (causes HTML render-as-text bug)
    avg_conf_str = (str(round(sum(r.get("confidence", 0) for r in riwayat_all) / total_scan)) + "%") if total_scan else "\u2014"

    st.markdown(f"""
    <div class="glass-card" style="padding:1.8rem !important; min-height:240px;">
        <p style="font-size:0.68rem; font-weight:800; text-transform:uppercase;
                  letter-spacing:0.13em; color:{theme['text_muted']}; margin:0 0 1.2rem;">
            \U0001f4cb Aktivitas Sesi &nbsp;&middot;&nbsp; {user_name}
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.9rem;">
            <div style="background:rgba({surf_rgb},0.5); border:1px solid {theme['border']};
                        border-radius:14px; padding:1rem; text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:1.8rem;
                            font-weight:900; color:{theme['gold']}; line-height:1;">{total_scan}</div>
                <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.08em; color:{theme['text_muted']}; margin-top:0.3rem;">Total Scan</div>
            </div>
            <div style="background:rgba({surf_rgb},0.5); border:1px solid {theme['border']};
                        border-radius:14px; padding:1rem; text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:1.8rem;
                            font-weight:900; color:#EF5350; line-height:1;">{total_sakit}</div>
                <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.08em; color:{theme['text_muted']}; margin-top:0.3rem;">Penyakit</div>
            </div>
            <div style="background:rgba({surf_rgb},0.5); border:1px solid {theme['border']};
                        border-radius:14px; padding:1rem; text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:1.8rem;
                            font-weight:900; color:#69F0AE; line-height:1;">{total_sehat}</div>
                <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.08em; color:{theme['text_muted']}; margin-top:0.3rem;">Sehat</div>
            </div>
            <div style="background:rgba({surf_rgb},0.5); border:1px solid {theme['border']};
                        border-radius:14px; padding:1rem; text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:1.8rem;
                            font-weight:900; color:{theme['primary_light']}; line-height:1;">{avg_conf_str}</div>
                <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.08em; color:{theme['text_muted']}; margin-top:0.3rem;">Avg Conf</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── DETECTION SECTION ────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.8rem; margin:0.5rem 0 1rem;">
    <div style="flex:1; height:1px; background:linear-gradient(90deg,{theme['border']},transparent);"></div>
    <span style="font-size:0.7rem; font-weight:800; text-transform:uppercase;
                 letter-spacing:0.15em; color:{theme['text_muted']};">Analisis Gambar</span>
    <div style="flex:1; height:1px; background:linear-gradient(90deg,transparent,{theme['border']});"></div>
</div>
""", unsafe_allow_html=True)

col_upload, col_result = st.columns([1, 1.35], gap="large")

# ──────────────────────────────────── LEFT: Upload ────────────────────────────
with col_upload:
    st.markdown('<div class="sec-label">📁 Upload Gambar</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload foto daun padi",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )

    st.markdown(f"""
    <p style="font-size:0.75rem; color:{theme['text_muted']}; margin:0.4rem 0 1.2rem;
              line-height:1.5;">
        Format: JPG · PNG · JPEG &nbsp;|&nbsp; Resolusi min. 640×480px<br>
        Pastikan foto close-up & pencahayaan cukup.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">⚙️ Sensitivitas Deteksi</div>', unsafe_allow_html=True)
    conf_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.05, max_value=0.60,
        value=0.15, step=0.05,
        help="Turunkan jika penyakit tidak terdeteksi. Naikkan untuk mengurangi false positive.",
        label_visibility="collapsed"
    )

    # Threshold indicator
    if conf_threshold < 0.20:
        thr_label, thr_color = "🔴 Sensitif Tinggi", "#EF5350"
    elif conf_threshold < 0.40:
        thr_label, thr_color = "🟡 Seimbang", "#FFB74D"
    else:
        thr_label, thr_color = "🟢 Selektif", "#69F0AE"

    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                font-size:0.78rem; margin-top:0.3rem; margin-bottom:0.8rem;">
        <span style="color:{theme['text_muted']};">Threshold: <strong>{conf_threshold:.2f}</strong></span>
        <span style="color:{thr_color}; font-weight:700;">{thr_label}</span>
    </div>
    """, unsafe_allow_html=True)

    if uploaded_file:
        st.markdown('<div class="sec-label">🖼️ Preview</div>', unsafe_allow_html=True)
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, use_container_width=True)

# ──────────────────────────────────── RIGHT: Result ───────────────────────────
with col_result:
    st.markdown('<div class="sec-label">🔬 Hasil Analisis</div>', unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown(f"""
        <div class="empty-state">
            <div style="font-size:3.2rem; margin-bottom:1rem; opacity:0.55;">🌾</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.05rem;
                        color:{theme['text_secondary']}; margin-bottom:0.45rem;">
                Belum ada gambar diupload
            </div>
            <div style="font-size:0.82rem; color:{theme['text_muted']}; max-width:260px; line-height:1.55;">
                Upload foto close-up daun padi di panel kiri untuk memulai deteksi AI
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Menganalisis dengan YOLOv8..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                image.save(tmp.name)
                temp_path = tmp.name
            results = model.predict(temp_path, conf=conf_threshold, verbose=False)
            os.unlink(temp_path)

        boxes = results[0].boxes

        if boxes is None or len(boxes) == 0:
            st.session_state.detected_diseases = []
            st.markdown(f"""
            <div style="background:rgba(255,183,77,0.08); border:1px solid rgba(255,183,77,0.25);
                        border-radius:12px; padding:0.9rem 1.1rem; font-size:0.87rem;
                        color:#FFB74D; margin-bottom:1rem; line-height:1.6;">
                ⚠️ <strong>Tidak ada penyakit terdeteksi</strong> pada threshold ini.<br>
                Coba turunkan sensitivitas, atau pastikan foto close-up & fokus.
            </div>
            """, unsafe_allow_html=True)
            annotated = results[0].plot()
            st.image(annotated, caption="output deteksi · tidak ada objek", use_container_width=True)
        else:
            detections   = []
            seen         = set()
            disease_labels = []

            for box in boxes:
                cls_id = int(box.cls[0])
                conf   = float(box.conf[0])
                name   = model.names[cls_id]
                if name not in seen:
                    seen.add(name)
                    detections.append((name, conf))
                    info = DISEASE_INFO.get(name, {})
                    disease_labels.append(info.get('label', name))

            detections.sort(key=lambda x: x[1], reverse=True)
            st.session_state.detected_diseases = disease_labels

            # Save to riwayat
            for name, conf in detections:
                info   = DISEASE_INFO.get(name, {})
                status = "Sehat" if name == "Rice__Healthy" else "Terdeteksi"
                entry  = {
                    "disease":    info.get("label", name),
                    "confidence": conf * 100,
                    "status":     status,
                    "date":       datetime.now(),
                }
                if "riwayat_list" not in st.session_state:
                    st.session_state.riwayat_list = []
                st.session_state.riwayat_list.append(entry)

            # Render disease cards
            for name, conf in detections:
                info = DISEASE_INFO.get(name, {
                    'label': name, 'severity': 'warning',
                    'desc': 'Tidak ada deskripsi tersedia.',
                    'treatment': 'Hubungi penyuluh pertanian setempat.',
                })
                sev = info['severity']
                st.markdown(f"""
                <div class="dcard {sev}">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.4rem;">
                        <div class="dcard-name">{info['label']}</div>
                        <div class="dcard-conf">{conf*100:.1f}%</div>
                    </div>
                    <div class="pbar-bg">
                        <div class="pbar-fill" style="width:{conf*100:.0f}%"></div>
                    </div>
                    <div class="dcard-desc">{info['desc']}</div>
                    <div class="dcard-treatment">
                        <b>💊 Penanganan</b>{info['treatment']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f'<div class="sec-label" style="margin-top:0.8rem;">📸 Output · {len(boxes)} objek</div>', unsafe_allow_html=True)
            annotated = results[0].plot()
            st.image(annotated, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── CHATBOT SECTION ──────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.8rem; margin:0.8rem 0 1rem;">
    <div style="flex:1; height:1px; background:linear-gradient(90deg,{theme['border']},transparent);"></div>
    <span style="font-size:0.7rem; font-weight:800; text-transform:uppercase;
                 letter-spacing:0.15em; color:{theme['text_muted']};">Konsultasi AI</span>
    <div style="flex:1; height:1px; background:linear-gradient(90deg,transparent,{theme['border']});"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card" style="padding:1.8rem 2rem !important;">', unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:1.4rem;
            padding-bottom:1rem; border-bottom:1px solid {theme['border']};">
    <div style="width:40px; height:40px; border-radius:12px;
                background:linear-gradient(135deg,{theme['primary']},{theme['primary_light']});
                display:flex; align-items:center; justify-content:center;
                font-size:1.2rem; box-shadow:0 4px 12px rgba(46,125,50,0.3);">🤖</div>
    <div>
        <div style="font-family:'Playfair Display',serif; font-size:1.05rem;
                    font-weight:700; color:{theme['text']};">PadiBot — Asisten Pertanian</div>
        <div style="font-size:0.76rem; color:{theme['text_muted']};">
            Didukung Gemini AI · Tanya seputar penyakit & penanganan padi
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick questions
if st.session_state.detected_diseases:
    disease_str = ", ".join(st.session_state.detected_diseases)
    st.markdown(f'<div class="sec-label">⚡ Pertanyaan Cepat · {disease_str}</div>', unsafe_allow_html=True)
    qcols = st.columns(3)
    quick_questions = [
        f"Apa penyebab utama {st.session_state.detected_diseases[0]}?",
        f"Bagaimana cara mencegah {st.session_state.detected_diseases[0]}?",
        "Berapa lama pengobatan yang diperlukan?",
        "Apakah penyakit ini menular ke tanaman lain?",
        "Pestisida apa yang paling efektif?",
        "Kapan waktu terbaik untuk menyemprot?",
    ]
    for i, q in enumerate(quick_questions[:6]):
        with qcols[i % 3]:
            if st.button(q, key=f"quick_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": q})
                with st.spinner("PadiBot sedang berpikir..."):
                    reply = chat_with_gemini(q, st.session_state.detected_diseases)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# Chat history
if st.session_state.chat_history:
    st.markdown('<div class="sec-label">💬 Riwayat Percakapan</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div>
                <div class="msg-label">Kamu</div>
                <div class="msg-user">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div>
                <div class="msg-label">PadiBot</div>
                <div class="msg-bot">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("🗑 Hapus Riwayat Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

# Chat input
st.markdown('<div class="sec-label">✏️ Ketik Pertanyaan</div>', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col_inp, col_btn = st.columns([5, 1], gap="small")
    with col_inp:
        user_input = st.text_input(
            "Pesan",
            placeholder="Contoh: Apa gejala blast daun? Bagaimana cara pengobatannya?",
            label_visibility="collapsed"
        )
    with col_btn:
        send = st.form_submit_button("Kirim ➤", use_container_width=True)

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
    with st.spinner("PadiBot sedang berpikir..."):
        reply = chat_with_gemini(user_input.strip(), st.session_state.detected_diseases)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:3rem 0 1.5rem; margin-top:1rem;
            border-top:1px solid {theme['border']};
            color:{theme['text_muted']}; font-size:0.85rem;">
    🌾 <strong>PadiSense Premium v1.2</strong>
    &nbsp;|&nbsp; Diagnosis Cerdas untuk Kelestarian Pangan Nusantara<br>
    <span style="opacity:0.6; font-size:0.75rem;">
        © 2026 CAMP Batch 4 &nbsp;·&nbsp; Data Science &amp; Generative AI
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # outer wrapper