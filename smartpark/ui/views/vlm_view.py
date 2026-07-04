"""Sekme 1 — Sadece VLM (LocateAnything-3B) görünümü."""
import numpy as np
import streamlit as st

from smartpark.config import COLOR_VLM, HEX_VLM, VLM_DEFAULT_PROMPT
from smartpark.models.vlm import get_vlm_boxes
from smartpark.ui.components import legend_html
from smartpark.visualization import draw_detections

NO_IMAGE_MSG = "👉 Analiz için sol menüden bir otopark fotoğrafı yükleyin veya **örnek görseli** etkinleştirin."


def render(img):
    st.markdown('<div class="badge badge-vlm">Visual-Language Model</div>', unsafe_allow_html=True)
    st.markdown("### Sadece VLM ile Görsel Grounding Analizi")
    st.write("Otopark fotoğrafı doğrudan **NVIDIA LocateAnything-3B** görsel grounding modeline gönderilir. "
             "Model, doğal dil istemiyle belirtilen nesneleri konumlandırır.")

    if img is None:
        st.info(NO_IMAGE_MSG)
        return

    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Analiz İstemi (Prompt)</div>', unsafe_allow_html=True)
        user_prompt = st.text_input(
            "Modele gönderilecek talimat:",
            value=VLM_DEFAULT_PROMPT,
            label_visibility="collapsed"
        )
        analyze_button = st.button("🔍 Analiz Et", key="vlm_analyze_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze_button:
        boxes, answer, inference_time_ms = get_vlm_boxes(img, user_prompt)
        st.session_state["vlm_result"] = {
            "boxes": boxes, "answer": answer,
            "time_ms": inference_time_ms, "prompt": user_prompt
        }

    result = st.session_state.get("vlm_result")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if result:
            annotated = draw_detections(
                np.array(img.convert("RGB")), result["boxes"], COLOR_VLM, show_index=True
            )
            st.image(annotated, use_container_width=True)
            st.markdown(legend_html([(HEX_VLM, f"VLM Tespiti ({len(result['boxes'])})")]),
                        unsafe_allow_html=True)
        else:
            st.image(img, caption="Yüklenen Otopark Fotoğrafı", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if result:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Tespit Sonuçları</div>', unsafe_allow_html=True)

            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Tespit Edilen Nesne", f"{len(result['boxes'])}")
            m_col2.metric("Çıkarım Süresi", f"{result['time_ms']:.0f} ms")

            st.markdown(
                """
                <div class="info-note">
                    <strong>Mimari Notu:</strong> LocateAnything-3B, <strong>Parallel Box Decoding (PBD)</strong>
                    sayesinde kutuları paralel olarak tek adımda çözer. Doğal dil ile yönlendirilebilir
                    (araç, kamyon, insan vb.) ancak özel eğitilmiş bir dedektöre göre daha ağırdır.
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("🔬 Ham Model Çıktısı"):
                st.code(result["answer"], language=None)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("İstemi düzenleyip **Analiz Et** butonuna tıklayın.")
