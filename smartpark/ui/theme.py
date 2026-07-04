"""Premium koyu tema — özel CSS enjeksiyonu."""
import streamlit as st

_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Streamlit varsayılan menü ve dekorasyonlarını gizle (kurumsal görünüm) */
    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }

    .main {
        background-color: #0f111a;
        color: #ffffff;
    }

    /* Başlık Alanı */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-align: left;
        line-height: 1.2;
    }

    .subtitle {
        font-size: 1.02rem;
        color: #94a3b8;
        margin-bottom: 0.8rem;
        font-weight: 400;
    }

    /* Durum Çipleri (Header altı sistem durumu) */
    .chip-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 1.6rem;
    }
    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.09);
        color: #cbd5e1;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-green  { background: #22c55e; box-shadow: 0 0 8px rgba(34,197,94,0.8); }
    .dot-amber  { background: #f59e0b; box-shadow: 0 0 8px rgba(245,158,11,0.8); }
    .dot-blue   { background: #4facfe; box-shadow: 0 0 8px rgba(79,172,254,0.8); }
    .dot-purple { background: #a855f7; box-shadow: 0 0 8px rgba(168,85,247,0.8); }

    /* Glassmorphic Kartlar */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(79, 172, 254, 0.35);
        box-shadow: 0 12px 40px 0 rgba(79, 172, 254, 0.12);
    }

    /* Rapor Kartı */
    .vlm-report-card {
        background: rgba(15, 23, 42, 0.6);
        border-left: 5px solid #00f2fe;
        border-radius: 8px;
        padding: 18px;
        margin-top: 15px;
    }

    /* Bölüm Etiketi (small-caps) */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 6px;
    }

    /* Butonlar */
    .stButton>button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #0f111a !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.45) !important;
        color: #ffffff !important;
    }
    .stButton>button:active { transform: translateY(1px) !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b0d14 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .sidebar-panel {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 14px;
        font-size: 0.85rem;
        color: #cbd5e1;
    }
    .sidebar-panel .row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
    }
    .sidebar-panel .key { color: #64748b; font-weight: 500; }
    .sidebar-panel .val { color: #e2e8f0; font-weight: 600; text-align: right; }

    /* Sekmeler */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 8px 8px 0px 0px;
        color: #94a3b8;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: none;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background-color: rgba(255, 255, 255, 0.06);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(79, 172, 254, 0.15) !important;
        color: #00f2fe !important;
        border-top: 2px solid #00f2fe !important;
    }

    /* Metrikler */
    div[data-testid="stMetricValue"] {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        color: #00f2fe !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.88rem !important;
        color: #94a3b8 !important;
    }

    /* Bilgi Notu */
    .info-note {
        font-size: 0.84rem;
        color: #64748b;
        border-left: 2px solid #64748b;
        padding-left: 10px;
        margin-top: 10px;
        line-height: 1.5;
    }

    /* Rozetler */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 10px;
        letter-spacing: 0.04em;
    }
    .badge-yolo   { background: rgba(34, 197, 94, 0.15);  color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.3); }
    .badge-vlm    { background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-hybrid { background: rgba(79, 172, 254, 0.15); color: #4facfe; border: 1px solid rgba(79, 172, 254, 0.3); }

    /* Lejant */
    .legend-row {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin: 8px 0 4px 0;
    }
    .legend-item {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 500;
    }
    .legend-swatch {
        width: 14px;
        height: 14px;
        border-radius: 4px;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.25);
    }

    /* Doluluk Çubuğu */
    .occupancy-wrap { margin: 10px 0 4px 0; }
    .occupancy-head {
        display: flex;
        justify-content: space-between;
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .occupancy-track {
        width: 100%;
        height: 12px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.06);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .occupancy-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.6s ease;
    }
    </style>
"""


def inject_theme():
    """Özel CSS temasını sayfaya enjekte eder."""
    st.markdown(_CSS, unsafe_allow_html=True)
