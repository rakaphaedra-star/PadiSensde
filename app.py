import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import tempfile
import os
from google import genai

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PadiSense",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Figtree:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg:         #080F06;
    --surface:    #0F1D0C;
    --card:       #162114;
    --card-hover: #1C2B19;
    --border:     #243520;
    --border-lit: #3A5530;
    --accent:     #A3D860;
    --accent-dim: #6B9E3A;
    --accent-glow:rgba(163,216,96,0.18);
    --danger:     #FF5252;
    --danger-bg:  #1F0A0A;
    --danger-glow:rgba(255,82,82,0.15);
    --warning:    #FFB74D;
    --warning-bg: #1F1408;
    --warning-glow:rgba(255,183,77,0.15);
    --healthy:    #69F0AE;
    --healthy-bg: #071A11;
    --healthy-glow:rgba(105,240,174,0.15);
    --text:       #D8EDD0;
    --text-muted: #6E8C66;
    --text-dim:   #4A6344;
    --radius:     14px;
    --radius-sm:  8px;
}

html, body, [class*="css"], .stApp {
    font-family: 'Figtree', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

.main .block-container {
    background-color: var(--bg);
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

.hero-wrap {
    position: relative;
    background: linear-gradient(135deg, #0B1E08 0%, #112A0D 50%, #162E10 100%);
    border: 1px solid var(--border-lit);
    border-radius: 20px;
    padding: 2.8rem 3rem;
    margin-bottom: 2rem;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(163,216,96,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-wrap::after {
    content: '⬡ ⬡ ⬡';
    position: absolute;
    bottom: 1rem; right: 2rem;
    font-size: 1.6rem;
    color: var(--border-lit);
    letter-spacing: 0.5rem;
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    background: var(--accent-glow);
    border: 1px solid var(--accent-dim);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3rem;
    font-weight: 800;
    color: var(--text) !important;
    margin: 0 0 0.5rem;
    line-height: 1.1;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 400;
    max-width: 520px;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    gap: 2.5rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.hero-stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    color: var(--accent);
    font-weight: 700;
}
.hero-stat-label {
    font-size: 0.75rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}

.panel-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-label::before {
    content: '';
    display: inline-block;
    width: 18px; height: 2px;
    background: var(--accent-dim);
    border-radius: 2px;
}

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border-lit) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] label { color: var(--text-muted) !important; }
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploader"] button {
    background: var(--card) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border-lit) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Figtree', sans-serif !important;
    font-weight: 600 !important;
}
[data-testid="stFileUploader"] p { color: var(--text-muted) !important; }
[data-testid="stFileUploader"] small { color: var(--text-dim) !important; }

[data-testid="stSlider"] label {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
}
[data-testid="stSlider"] > div > div > div {
    background: var(--border-lit) !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}

[data-testid="stImage"] img {
    border-radius: var(--radius);
    border: 1px solid var(--border);
}
[data-testid="stImage"] > div > small {
    color: var(--text-dim) !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
}

.stSpinner > div { border-top-color: var(--accent) !important; }
[data-testid="stSpinner"] p { color: var(--text-muted) !important; }

.stAlert {
    background: var(--warning-bg) !important;
    border: 1px solid rgba(255,183,77,0.3) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--warning) !important;
}
.stAlert p { color: var(--warning) !important; }

.dcard {
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.1rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s;
}
.dcard::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.dcard:hover { transform: translateX(3px); }

.dcard.danger  { background: var(--danger-bg);  box-shadow: 0 0 24px var(--danger-glow); }
.dcard.warning { background: var(--warning-bg); box-shadow: 0 0 24px var(--warning-glow); }
.dcard.healthy { background: var(--healthy-bg); box-shadow: 0 0 24px var(--healthy-glow); }

.dcard.danger::before  { background: var(--danger); box-shadow: 0 0 10px var(--danger); }
.dcard.warning::before { background: var(--warning); box-shadow: 0 0 10px var(--warning); }
.dcard.healthy::before { background: var(--healthy); box-shadow: 0 0 10px var(--healthy); }

.dcard-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.8rem;
}
.dcard-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.dcard.danger  .dcard-name { color: var(--danger); }
.dcard.warning .dcard-name { color: var(--warning); }
.dcard.healthy .dcard-name { color: var(--healthy); }

.dcard-conf {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-weight: 700;
}
.dcard.danger  .dcard-conf { background: rgba(255,82,82,0.15);   color: var(--danger); }
.dcard.warning .dcard-conf { background: rgba(255,183,77,0.15);  color: var(--warning); }
.dcard.healthy .dcard-conf { background: rgba(105,240,174,0.15); color: var(--healthy); }

.pbar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    height: 5px;
    margin-bottom: 1rem;
    overflow: hidden;
}
.pbar-fill {
    height: 5px;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.danger  .pbar-fill { background: linear-gradient(90deg, #B71C1C, #FF5252); }
.warning .pbar-fill { background: linear-gradient(90deg, #E65100, #FFB74D); }
.healthy .pbar-fill { background: linear-gradient(90deg, #1B5E20, #69F0AE); }

.dcard-desc {
    color: var(--text-muted);
    font-size: 0.88rem;
    line-height: 1.65;
    margin-bottom: 0.9rem;
}

.dcard-treatment {
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    line-height: 1.6;
}
.danger  .dcard-treatment { background: rgba(255,82,82,0.08);  border: 1px solid rgba(255,82,82,0.2); color: #FFCDD2; }
.warning .dcard-treatment { background: rgba(255,183,77,0.08); border: 1px solid rgba(255,183,77,0.2); color: #FFE0B2; }
.healthy .dcard-treatment { background: rgba(105,240,174,0.08);border: 1px solid rgba(105,240,174,0.2); color: #B9F6CA; }

.dcard-treatment b { font-weight: 600; display: block; margin-bottom: 0.2rem; }

.empty-state {
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: var(--radius);
    padding: 3.5rem 2rem;
    text-align: center;
}
.empty-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    display: block;
    filter: grayscale(0.4);
}
.empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.empty-sub {
    font-size: 0.82rem;
    color: var(--text-dim);
    font-family: 'Space Mono', monospace;
}

.tip-box {
    background: rgba(163,216,96,0.06);
    border: 1px solid rgba(163,216,96,0.2);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: var(--accent);
    margin-top: 0.6rem;
}

/* ── Chatbot Styles ── */
.chat-section {
    background: var(--surface);
    border: 1px solid var(--border-lit);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2.5rem;
}
.chat-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.chat-icon {
    font-size: 1.5rem;
}
.chat-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
}
.chat-subtitle {
    font-size: 0.8rem;
    color: var(--text-dim);
    font-family: 'Space Mono', monospace;
}
.msg-user {
    background: var(--accent-glow);
    border: 1px solid rgba(163,216,96,0.25);
    border-radius: 12px 12px 2px 12px;
    padding: 0.8rem 1rem;
    margin: 0.6rem 0 0.6rem 3rem;
    color: var(--text);
    font-size: 0.9rem;
    line-height: 1.6;
}
.msg-bot {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px 12px 12px 2px;
    padding: 0.8rem 1rem;
    margin: 0.6rem 3rem 0.6rem 0;
    color: var(--text);
    font-size: 0.9rem;
    line-height: 1.6;
}
.msg-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-dim);
    margin-bottom: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.quick-btn-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.stButton > button {
    background: var(--card) !important;
    border: 1px solid var(--border-lit) !important;
    color: var(--text-muted) !important;
    border-radius: 20px !important;
    font-size: 0.82rem !important;
    padding: 0.3rem 0.9rem !important;
    font-family: 'Figtree', sans-serif !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

.app-footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.app-footer .left {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--accent);
}
.app-footer .right {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 0.05em;
}

hr { border-color: var(--border) !important; }
.stCaption, [data-testid="stCaptionContainer"] p {
    color: var(--text-dim) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Disease Info Database ───────────────────────────────────────────────────
DISEASE_INFO = {
    'Rice__BacterialLeafBlight': {
        'label': 'Hawar Daun Bakteri',
        'severity': 'danger',
        'desc': 'Infeksi bakteri Xanthomonas oryzae pv. oryzae yang menyebabkan daun menguning dan mengering dari tepi.',
        'treatment': 'Gunakan varietas tahan, kurangi penggunaan pupuk nitrogen, semprot bakterisida berbahan tembaga (copper oxychloride).',
        'icon': '◈'
    },
    'Rice__BrownSpot': {
        'label': 'Bercak Coklat',
        'severity': 'warning',
        'desc': 'Disebabkan jamur Bipolaris oryzae, muncul bercak oval coklat di daun. Sering terjadi pada lahan kekurangan nutrisi.',
        'treatment': 'Perbaiki nutrisi tanah (terutama kalium), semprot fungisida berbahan mancozeb atau iprodione.',
        'icon': '◈'
    },
    'Rice__Healthy': {
        'label': 'Tanaman Sehat',
        'severity': 'healthy',
        'desc': 'Daun padi terlihat sehat, tidak menunjukkan gejala penyakit.',
        'treatment': 'Pertahankan kondisi lahan: irigasi teratur, pemupukan sesuai dosis, dan pemantauan rutin.',
        'icon': '◈'
    },
    'Rice__Hispa': {
        'label': 'Hispa (Kumbang Daun)',
        'severity': 'warning',
        'desc': 'Serangan hama Dicladispa armigera yang mengikis jaringan daun, meninggalkan bekas putih memanjang.',
        'treatment': 'Cabut dan musnahkan daun terserang, semprotkan insektisida karbofuran atau klorpirifos pada pagi hari.',
        'icon': '◈'
    },
    'Rice__LeafBlast': {
        'label': 'Blast Daun',
        'severity': 'danger',
        'desc': 'Penyakit jamur Magnaporthe oryzae yang sangat merusak, membentuk bercak berlian abu-abu di daun.',
        'treatment': 'Gunakan varietas tahan blast, semprot fungisida propikonazol atau trisiklazol sesegera mungkin.',
        'icon': '◈'
    },
    'Rice__LeafScald': {
        'label': 'Gosong Daun',
        'severity': 'warning',
        'desc': 'Disebabkan jamur Microdochium oryzae, daun terlihat terbakar/gosong dari ujung ke pangkal.',
        'treatment': 'Semprot fungisida berbahan aktif iprodione, hindari kelebihan pupuk nitrogen.',
        'icon': '◈'
    },
    'Rice__LeafSmut': {
        'label': 'Gosong Palsu Daun',
        'severity': 'warning',
        'desc': 'Penyakit jamur yang membentuk massa spora hitam kecil di permukaan daun.',
        'treatment': 'Semprot fungisida berbahan tembaga, pastikan drainase lahan baik untuk mengurangi kelembaban.',
        'icon': '◈'
    },
    'Rice__NarrowBrownLeafSpot': {
        'label': 'Bercak Sempit Coklat',
        'severity': 'warning',
        'desc': 'Bercak coklat sempit dan panjang akibat jamur Cercospora janseana, umumnya pada fase pengisian bulir.',
        'treatment': 'Semprot fungisida propikonazol, jaga sirkulasi air lahan tetap baik.',
        'icon': '◈'
    },
    'Rice__NeckBlast': {
        'label': 'Blast Leher Malai',
        'severity': 'danger',
        'desc': 'Serangan blast paling kritis — menyerang leher malai sehingga bulir menjadi hampa dan gagal panen.',
        'treatment': 'SEGERA semprot trisiklazol atau isoprothiolane. Ini darurat — penanganan terlambat bisa gagal panen total.',
        'icon': '◈'
    },
}

# ─── Load Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# ─── Session State Init ──────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "detected_diseases" not in st.session_state:
    st.session_state.detected_diseases = []

# ─── Gemini Client ────────────────────────────────────────────────────────────
# Cara 1: Pakai environment variable (RECOMMENDED)
#   Windows  → set GEMINI_API_KEY=AIza...
#   Linux/Mac → export GEMINI_API_KEY=AIza...
# Cara 2: Isi langsung di bawah (untuk testing lokal, jangan di-push ke GitHub)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBsFZF6UtgNqMLh9XPC5SdPhTYAl7iDN8w")  # ganti "AIza..." kalau mau hardcode

def get_system_prompt(detected_diseases: list) -> str:
    """Buat system prompt berdasarkan penyakit yang terdeteksi."""
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
- Kalau tidak relevan dengan penyakit padi, arahkan kembali ke topik pertanian padi
- Gunakan format list/bullet kalau membantu kejelasan"""

def chat_with_gemini(user_message: str, detected_diseases: list) -> str:
    """Kirim pesan ke Gemini dan dapat balasan."""
    if not GEMINI_API_KEY:
        return "⚠️ API key Gemini belum diset. Isi GEMINI_API_KEY di baris yang tersedia di kode."

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Bangun history chat dalam format Gemini baru
        system_prompt = get_system_prompt(detected_diseases)
        history_text = ""
        for msg in st.session_state.chat_history:
            role = "User" if msg["role"] == "user" else "PadiBot"
            history_text += f"{role}: {msg['content']}\n"

        full_prompt = f"{system_prompt}\n\n{history_text}User: {user_message}\nPadiBot:"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        return response.text

    except Exception as e:
        err = str(e)
        if "API_KEY_INVALID" in err or "API key not valid" in err:
            return "⚠️ API key tidak valid. Cek kembali di aistudio.google.com"
        elif "quota" in err.lower() or "429" in err:
            return "⚠️ Rate limit tercapai. Tunggu 1 menit lalu coba lagi."
        elif "not found" in err.lower() or "404" in err:
            return "⚠️ Model tidak ditemukan. Pastikan library google-genai sudah terinstall: pip install google-genai"
        else:
            return f"⚠️ Error: {err}"

# ─── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">YOLOv8n · COMPUTER VISION · AGRITECH</div>
    <h1 class="hero-title">Padi<span>Sense</span></h1>
    <p class="hero-sub">Sistem deteksi penyakit daun padi berbasis deep learning — upload foto, dapatkan diagnosis dan rekomendasi penanganan secara instan.</p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-num">9</div>
            <div class="hero-stat-label">Kelas Penyakit</div>
        </div>
        <div>
            <div class="hero-stat-num">63.4%</div>
            <div class="hero-stat-label">mAP@50</div>
        </div>
        <div>
            <div class="hero-stat-num">YOLOv8n</div>
            <div class="hero-stat-label">Arsitektur Model</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Main Layout ─────────────────────────────────────────────────────────────
col_upload, col_result = st.columns([1, 1.3], gap="large")

with col_upload:
    st.markdown('<div class="panel-label">Input Gambar</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload foto daun padi (JPG, PNG, JPEG)",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Sensitivitas Deteksi</div>', unsafe_allow_html=True)
    conf_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.05,
        max_value=0.60,
        value=0.15,
        step=0.05,
        help="Turunkan jika penyakit tidak terdeteksi. Naikkan untuk mengurangi false positive.",
        label_visibility="collapsed"
    )
    st.caption(f"Threshold aktif: {conf_threshold:.2f} — {'sensitif tinggi' if conf_threshold < 0.20 else 'seimbang' if conf_threshold < 0.40 else 'selektif'}")

    if uploaded_file:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="panel-label">Preview Input</div>', unsafe_allow_html=True)
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, use_container_width=True)

with col_result:
    st.markdown('<div class="panel-label">Hasil Analisis</div>', unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-icon">🌾</span>
            <div class="empty-title">Belum ada gambar diupload</div>
            <div class="empty-sub">upload foto close-up daun padi untuk memulai</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Menganalisis gambar dengan YOLOv8..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                image.save(tmp.name)
                temp_path = tmp.name

            results = model.predict(temp_path, conf=conf_threshold, verbose=False)
            os.unlink(temp_path)

        boxes = results[0].boxes

        if boxes is None or len(boxes) == 0:
            st.session_state.detected_diseases = []
            st.markdown("""
            <div class="tip-box">
                ⚠️ <b>Tidak ada penyakit terdeteksi</b> pada confidence threshold ini.<br>
                Coba turunkan slider sensitivitas, atau pastikan foto close-up satu daun dengan pencahayaan baik.
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            annotated = results[0].plot()
            st.image(annotated, caption="output deteksi · tidak ada objek", use_container_width=True)
        else:
            # Kumpulkan deteksi unik
            detections = []
            seen = set()
            disease_labels = []  # untuk chatbot context

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]
                if name not in seen:
                    seen.add(name)
                    detections.append((name, conf))
                    info = DISEASE_INFO.get(name, {})
                    disease_labels.append(info.get('label', name))

            detections.sort(key=lambda x: x[1], reverse=True)

            # Update session state dengan penyakit yang terdeteksi
            st.session_state.detected_diseases = disease_labels

            for name, conf in detections:
                info = DISEASE_INFO.get(name, {
                    'label': name,
                    'severity': 'warning',
                    'desc': 'Tidak ada deskripsi tersedia.',
                    'treatment': 'Hubungi penyuluh pertanian setempat.',
                    'icon': '◈'
                })
                sev = info['severity']
                st.markdown(f"""
                <div class="dcard {sev}">
                    <div class="dcard-header">
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

            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="panel-label">Output Deteksi · {len(boxes)} objek ditemukan</div>', unsafe_allow_html=True)
            annotated = results[0].plot()
            st.image(annotated, use_container_width=True)

# ─── Chatbot Section ─────────────────────────────────────────────────────────
st.markdown('<div class="chat-section">', unsafe_allow_html=True)
st.markdown("""
<div class="chat-header">
    <span class="chat-icon">🤖</span>
    <div>
        <div class="chat-title">PadiBot — Asisten Pertanian</div>
        <div class="chat-subtitle">tanya apa saja soal penyakit dan penanganan padi</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick questions — muncul kalau ada penyakit terdeteksi
if st.session_state.detected_diseases:
    disease_str = ", ".join(st.session_state.detected_diseases)
    st.markdown(f'<div class="panel-label">Pertanyaan cepat · terdeteksi: {disease_str}</div>', unsafe_allow_html=True)

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
        col_idx = i % 3
        with qcols[col_idx]:
            if st.button(q, key=f"quick_{i}"):
                # Tambah ke history dan langsung proses
                st.session_state.chat_history.append({"role": "user", "content": q})
                with st.spinner("PadiBot sedang berpikir..."):
                    reply = chat_with_gemini(q, st.session_state.detected_diseases)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# Tampilkan history chat
if st.session_state.chat_history:
    st.markdown('<div class="panel-label">Riwayat Percakapan</div>', unsafe_allow_html=True)
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

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Tombol hapus history
    if st.button("🗑 Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Input chat
st.markdown('<div class="panel-label">Ketik Pertanyaan</div>', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    cols = st.columns([5, 1])
    with cols[0]:
        user_input = st.text_input(
            "Tanya PadiBot...",
            placeholder="Contoh: Apa yang harus saya lakukan setelah menyemprot fungisida?",
            label_visibility="collapsed"
        )
    with cols[1]:
        submitted = st.form_submit_button("Kirim", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner("PadiBot sedang berpikir..."):
            reply = chat_with_gemini(user_input.strip(), st.session_state.detected_diseases)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="left">🌾 PadiSense</div>
    <div class="right">YOLOv8n &nbsp;·&nbsp; 9 Kelas &nbsp;·&nbsp; mAP@50: 0.634 &nbsp;·&nbsp; Sistem Deteksi Penyakit Padi</div>
</div>
""", unsafe_allow_html=True)