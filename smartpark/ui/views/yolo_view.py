"""Sekme 2 — Sadece YOLO (best.pt) görünümü."""
import numpy as np
import streamlit as st

from smartpark.config import (COLOR_EMPTY, COLOR_OCCUPIED, HEX_EMPTY,
                              HEX_OCCUPIED, YOLO_DEFAULT_CONF)
from smartpark.models.yolo import load_yolo_model, run_yolo_detection
from smartpark.ui.components import legend_html, occupancy_bar_html
from smartpark.visualization import draw_detections
from smartpark.ui.views.vlm_view import NO_IMAGE_MSG


def render(img):
    st.markdown('<div class="badge badge-yolo">YOLO26 — best.pt</div>', unsafe_allow_html=True)
    st.markdown("### Sadece YOLO ile Boş/Dolu Park Yeri Tespiti")
    st.write("**PKLot veri setiyle eğitilmiş YOLO26 modeli (`best.pt`)**, boş (`space-empty`) ve dolu "
             "(`space-occupied`) park yerlerini doğrudan sınıflandırarak tespit eder.")

    if img is None:
        st.info(NO_IMAGE_MSG)
        return

    yolo_model = load_yolo_model()
    if yolo_model is None:
        return

    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Tespit Ayarları</div>', unsafe_allow_html=True)
        conf_threshold = st.slider(
            "Güven Eşiği (Confidence)",
            min_value=0.05, max_value=0.90, value=YOLO_DEFAULT_CONF, step=0.05,
            help="Düşük eşik daha fazla tespit üretir ancak hatalı pozitif riski artar."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner("🎯 YOLO26 (best.pt) çıkarımı yapılıyor..."):
        empty_boxes, occupied_boxes, inference_time_ms = run_yolo_detection(
            yolo_model, img, conf=conf_threshold
        )

    total_spots = len(empty_boxes) + len(occupied_boxes)
    occupancy_rate = (len(occupied_boxes) / total_spots * 100) if total_spots > 0 else 0.0

    annotated = np.array(img.convert("RGB"))
    annotated = draw_detections(annotated, empty_boxes, COLOR_EMPTY)
    annotated = draw_detections(annotated, occupied_boxes, COLOR_OCCUPIED)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.image(annotated, use_container_width=True)
        st.markdown(legend_html([
            (HEX_EMPTY, f"Boş Park Yeri ({len(empty_boxes)})"),
            (HEX_OCCUPIED, f"Dolu Park Yeri ({len(occupied_boxes)})"),
        ]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Tespit Sonuçları</div>', unsafe_allow_html=True)

        m_col1, m_col2 = st.columns(2)
        m_col1.metric("🟢 Boş", f"{len(empty_boxes)}")
        m_col2.metric("🔴 Dolu", f"{len(occupied_boxes)}")
        m_col1.metric("Toplam Park Yeri", f"{total_spots}")
        m_col2.metric("Çıkarım Süresi", f"{inference_time_ms:.0f} ms")

        st.markdown(occupancy_bar_html(occupancy_rate), unsafe_allow_html=True)

        st.markdown(
            """
            <div class="info-note">
                <strong>Hız Notu:</strong> Özel eğitilmiş YOLO modeli tek görevine odaklandığı için
                VLM'e kıyasla kat kat hızlıdır ve gerçek zamanlı video akışında dahi çalışabilir.
                Ancak yalnızca eğitildiği sınıfları tanır; istemle yönlendirilemez.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
