"""
SmartPark AI — Otopark Doluluk & Anomali Tespit Platformu

Streamlit giriş noktası: sayfa yapılandırması, tema, sidebar ve sekme yönlendirmesi.
Uygulama mantığı smartpark/ paketindedir:
  - smartpark/config.py        : sabitler ve dosya yolları
  - smartpark/models/          : VLM (LocateAnything-3B) ve YOLO (best.pt) katmanı
  - smartpark/visualization.py : tespit kutusu çizimi
  - smartpark/ui/              : tema, bileşenler ve sekme görünümleri
"""
import streamlit as st
from PIL import Image

from smartpark.ui.theme import inject_theme
from smartpark.ui.components import render_header, render_sidebar
from smartpark.ui.views import vlm_view, yolo_view, hybrid_view

# Sayfa yapılandırması ve tema
st.set_page_config(
    page_title="SmartPark AI — Otopark Analiz Platformu",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_theme()

# Yan menü: kullanıcı seçimleri
uploaded_file, sample_path = render_sidebar()

# Görsel kaynağını belirle
img = None
file_key = None
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    file_key = f"{uploaded_file.name}-{uploaded_file.size}"
elif sample_path is not None and sample_path.exists():
    img = Image.open(sample_path)
    file_key = sample_path.name

# Görsel değiştiğinde önceki analiz sonuçlarını temizle
if st.session_state.get("active_file") != file_key:
    st.session_state["active_file"] = file_key
    st.session_state.pop("vlm_result", None)
    st.session_state.pop("hybrid_result", None)

# Başlık ve sistem durumu çipleri
render_header(has_image=img is not None)

# Sekmeler
tab1, tab2, tab3 = st.tabs([
    "🔍 Sadece VLM",
    "🎯 Sadece YOLO",
    "⚡ VLM + YOLO (Hibrit)"
])

with tab1:
    vlm_view.render(img)
with tab2:
    yolo_view.render(img)
with tab3:
    hybrid_view.render(img)
