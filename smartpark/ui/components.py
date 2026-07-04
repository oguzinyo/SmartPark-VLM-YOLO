"""Tekrar kullanılabilir arayüz bileşenleri (lejant, doluluk çubuğu, durum çipleri, sidebar)."""
import streamlit as st
import torch

from smartpark.config import SAMPLE_GALLERY


def legend_html(items):
    """[(renk_hex, etiket), ...] listesinden lejant HTML'i üretir."""
    spans = "".join(
        f'<span class="legend-item"><span class="legend-swatch" style="background:{color}"></span>{label}</span>'
        for color, label in items
    )
    return f'<div class="legend-row">{spans}</div>'


def occupancy_bar_html(rate: float):
    """Doluluk oranını renk kodlu yatay bar olarak üretir."""
    if rate < 50:
        color = "#22c55e"
    elif rate < 80:
        color = "#f59e0b"
    else:
        color = "#ef4444"
    return f"""
    <div class="occupancy-wrap">
        <div class="occupancy-head"><span>Doluluk Oranı</span><span style="color:{color}">%{rate:.1f}</span></div>
        <div class="occupancy-track">
            <div class="occupancy-fill" style="width:{min(rate, 100):.1f}%; background:{color};"></div>
        </div>
    </div>
    """


def render_header(has_image: bool):
    """Ana başlık ve sistem durumu çiplerini çizer."""
    cuda_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_available else None

    st.markdown('<h1 class="main-title">Otopark Doluluk & Anomali Tespit Platformu</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Üç farklı yapay zeka mimarisinin performansını ve '
                'analiz yeteneğini karşılaştırın.</p>', unsafe_allow_html=True)

    device_chip = (
        f'<span class="status-chip"><span class="status-dot dot-green"></span>CUDA Aktif · {gpu_name}</span>'
        if cuda_available else
        '<span class="status-chip"><span class="status-dot dot-amber"></span>CPU Modu (CUDA bulunamadı)</span>'
    )
    mode_chip = '<span class="status-chip"><span class="status-dot dot-purple"></span>VLM: LocateAnything-3B</span>'
    img_chip = (
        '<span class="status-chip"><span class="status-dot dot-blue"></span>Görsel Hazır</span>'
        if has_image else
        '<span class="status-chip"><span class="status-dot dot-amber"></span>Görsel Bekleniyor</span>'
    )
    st.markdown(f'<div class="chip-row">{device_chip}{mode_chip}{img_chip}</div>',
                unsafe_allow_html=True)


def render_sidebar():
    """
    Yan menüyü çizer; kullanıcının seçimlerini döndürür.

    Returns:
        (uploaded_file, sample_path: Path | None)
    """
    cuda_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_available else None

    st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 18px;">
            <h2 style="color: #00f2fe; margin-bottom: 4px;">🚗 SmartPark AI</h2>
            <p style="color: #64748b; font-size: 0.85rem;">Otopark Doluluk ve Anomali Analizi</p>
        </div>
    """, unsafe_allow_html=True)

    # Sistem Durumu Paneli
    st.sidebar.markdown('<div class="section-label">Sistem Durumu</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f"""
        <div class="sidebar-panel">
            <div class="row"><span class="key">Cihaz</span><span class="val">{'🟢 ' + gpu_name if cuda_available else '🟡 CPU'}</span></div>
            <div class="row"><span class="key">PyTorch</span><span class="val">{torch.__version__}</span></div>
            <div class="row"><span class="key">YOLO Modeli</span><span class="val">best.pt (PKLot)</span></div>
            <div class="row"><span class="key">VLM Modeli</span><span class="val">LocateAnything-3B</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="section-label" style="margin-top:14px;">Görsel Kaynağı</div>',
                        unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader(
        "Bir otopark fotoğrafı seçin",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )
    sample_choice = st.sidebar.selectbox(
        "Veya örnek görsel seçin:",
        options=["(Örnek görsel seçilmedi)"] + list(SAMPLE_GALLERY),
        disabled=uploaded_file is not None,
        help="📷 işaretli görseller PKLot veri setinden gerçek otopark kamerası kareleridir; "
             "YOLO (best.pt) bu perspektifle eğitildiğinden en iyi sonucu bunlarda verir."
    )
    sample_path = SAMPLE_GALLERY.get(sample_choice)

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.6;">
            <strong style="color:#cbd5e1;">💡 Kıyaslanan 3 Yaklaşım</strong><br>
            <span style="color:#a855f7;">●</span> <strong>Sadece VLM:</strong> Doğal dil istemiyle esnek tespit; ağır model.<br>
            <span style="color:#22c55e;">●</span> <strong>Sadece YOLO:</strong> Özel eğitilmiş, milisaniye hızında boş/dolu tespiti.<br>
            <span style="color:#4facfe;">●</span> <strong>Hibrit:</strong> YOLO sayar, VLM çapraz doğrular.
        </div>
    """, unsafe_allow_html=True)

    return uploaded_file, sample_path
