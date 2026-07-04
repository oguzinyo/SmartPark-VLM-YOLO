"""Sekme 3 — VLM + YOLO (Hibrit) görünümü."""
import numpy as np
import streamlit as st

from smartpark.config import (COLOR_EMPTY, COLOR_OCCUPIED, COLOR_VLM, HEX_EMPTY,
                              HEX_OCCUPIED, HEX_VLM, VLM_DEFAULT_PROMPT)
from smartpark.models.vlm import get_vlm_boxes
from smartpark.models.yolo import load_yolo_model, run_yolo_detection
from smartpark.ui.components import legend_html, occupancy_bar_html
from smartpark.visualization import draw_detections
from smartpark.ui.views.vlm_view import NO_IMAGE_MSG


def _consistency_message(diff: int) -> str:
    """YOLO ve VLM sayımları arasındaki farka göre uyum mesajı üretir."""
    if diff == 0:
        return ("✅ İki model **tam uyumlu**: VLM araç sayısı, YOLO'nun dolu park yeri "
                "sayısıyla birebir örtüşüyor.")
    if diff <= 3:
        return (f"🟡 Modeller arasında **küçük bir fark ({diff} araç)** var. Bu, park yeri "
                "dışına (yol/geçiş alanı) park etmiş araçlardan veya kısmi görünen "
                "araçlardan kaynaklanabilir.")
    return (f"🔴 Modeller arasında **belirgin bir fark ({diff} araç)** var. Görselde park "
            "yeri dışında araçlar olabilir veya modellerden biri hatalı tespit yapıyor "
            "olabilir. Manuel kontrol önerilir.")


def render(img):
    st.markdown('<div class="badge badge-hybrid">VLM + YOLO Hybrid</div>', unsafe_allow_html=True)
    st.markdown("### YOLO ve LocateAnything-3B Hibrit Mimari")
    st.write("Önce **YOLO (best.pt)** boş/dolu park yerlerini milisaniyeler içinde sayar. Ardından "
             "**LocateAnything-3B** araçları bağımsız olarak konumlandırır ve iki modelin sonuçları "
             "çapraz doğrulanır.")

    if img is None:
        st.info(NO_IMAGE_MSG)
        return

    yolo_model = load_yolo_model()
    if yolo_model is None:
        return

    # 1. ADIM: YOLO ile hızlı doluluk analizi (her zaman gerçek model)
    with st.spinner("🎯 1. Adım: YOLO26 (best.pt) doluluk analizi yapılıyor..."):
        empty_boxes, occupied_boxes, yolo_time_ms = run_yolo_detection(yolo_model, img)

    total_spots = len(empty_boxes) + len(occupied_boxes)
    occupancy_rate = (len(occupied_boxes) / total_spots * 100) if total_spots > 0 else 0.0

    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">1. Adım — YOLO Hızlı Sayım</div>', unsafe_allow_html=True)

        m_col1, m_col2 = st.columns(2)
        m_col1.metric("🟢 Boş", f"{len(empty_boxes)}")
        m_col2.metric("🔴 Dolu", f"{len(occupied_boxes)}")

        st.markdown(occupancy_bar_html(occupancy_rate), unsafe_allow_html=True)
        st.caption(f"YOLO çıkarım süresi: **{yolo_time_ms:.0f} ms**")

        st.markdown("---")
        st.markdown('<div class="section-label">2. Adım — VLM Çapraz Doğrulama</div>', unsafe_allow_html=True)
        st.write("LocateAnything-3B araçları bağımsız konumlandırır; sonuçlar YOLO sayımıyla karşılaştırılır.")
        hybrid_button = st.button("⚡ VLM Doğrulamasını Başlat", key="hybrid_vlm_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if hybrid_button:
        vlm_boxes, vlm_answer, vlm_time_ms = get_vlm_boxes(img, VLM_DEFAULT_PROMPT)
        st.session_state["hybrid_result"] = {
            "vlm_boxes": vlm_boxes, "vlm_answer": vlm_answer, "vlm_time_ms": vlm_time_ms
        }

    hybrid = st.session_state.get("hybrid_result")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        annotated = np.array(img.convert("RGB"))
        annotated = draw_detections(annotated, empty_boxes, COLOR_EMPTY)
        annotated = draw_detections(annotated, occupied_boxes, COLOR_OCCUPIED)

        legend_items = [
            (HEX_EMPTY, f"Boş — YOLO ({len(empty_boxes)})"),
            (HEX_OCCUPIED, f"Dolu — YOLO ({len(occupied_boxes)})"),
        ]
        if hybrid:
            annotated = draw_detections(annotated, hybrid["vlm_boxes"], COLOR_VLM, fill_alpha=0.0)
            legend_items.append((HEX_VLM, f"Araç — VLM ({len(hybrid['vlm_boxes'])})"))

        st.image(annotated, use_container_width=True)
        st.markdown(legend_html(legend_items), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if hybrid:
        # Çapraz doğrulama raporu (gerçek sayılar üzerinden hesaplanır)
        vlm_car_count = len(hybrid["vlm_boxes"])
        yolo_occupied = len(occupied_boxes)
        vlm_time_ms = hybrid["vlm_time_ms"]
        diff = abs(vlm_car_count - yolo_occupied)
        agreement = (
            min(vlm_car_count, yolo_occupied) / max(vlm_car_count, yolo_occupied) * 100
            if max(vlm_car_count, yolo_occupied) > 0 else 100.0
        )
        speedup = (vlm_time_ms / yolo_time_ms) if yolo_time_ms > 0 else 0.0

        with col2:
            st.markdown('<div class="vlm-report-card">', unsafe_allow_html=True)
            st.markdown(f"""
🤖 **Hibrit Çapraz Doğrulama Raporu**

| Kaynak | Sayım |
|---|---|
| YOLO — Dolu Park Yeri | **{yolo_occupied}** |
| YOLO — Boş Park Yeri | **{len(empty_boxes)}** |
| VLM — Tespit Edilen Araç | **{vlm_car_count}** |

* **Model Uyum Oranı:** %{agreement:.1f}
* {_consistency_message(diff)}
* **Hız:** YOLO **{yolo_time_ms:.0f} ms** · VLM **{vlm_time_ms:.0f} ms** (**{speedup:.1f}x** fark)
* **Hibrit Avantajı:** Sürekli izleme YOLO ile maliyetsiz yapılırken, VLM yalnızca doğrulama
  gerektiğinde tetiklenerek işlem maliyeti düşürülür.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
