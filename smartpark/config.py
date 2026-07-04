"""Proje genelinde kullanılan sabitler ve dosya yolları."""
from pathlib import Path

# Proje kök dizini (smartpark/ paketinin bir üstü)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Model ve varlık yolları
YOLO_WEIGHTS = ROOT_DIR / "weights" / "best.pt"
SAMPLE_IMAGE = ROOT_DIR / "assets" / "otopark_sample.png"
SAMPLES_DIR = ROOT_DIR / "assets" / "samples"

# Örnek görsel galerisi. PKLot kareleri gerçek otopark kameralarından alındığından
# (best.pt'nin eğitim alanı) YOLO en iyi sonuçları bunlarda verir; kareler 48 adaylık
# havuzdan model güveni + COCO çapraz sayım uyumu + görsel denetimle seçildi ve
# doluluk yelpazesini (%0 → %100) kapsar. Yapay havadan görsel ise eğitim alanı
# dışında kaldığından zorlu senaryo örneğidir.
SAMPLE_GALLERY = {
    "📷 Tamamen boş — geniş otopark": SAMPLES_DIR / "pklot_tamamen_bos.jpg",
    "📷 Az dolu (~%30)": SAMPLES_DIR / "pklot_az_dolu.jpg",
    "📷 Yarı dolu (~%50)": SAMPLES_DIR / "pklot_yari_dolu.jpg",
    "📷 Yağmurlu, kısmen dolu": SAMPLES_DIR / "pklot_yagmurlu_kismi.jpg",
    "📷 Yoğun (~%80)": SAMPLES_DIR / "pklot_yogun_dolu.jpg",
    "📷 Tamamen dolu": SAMPLES_DIR / "pklot_tamamen_dolu.jpg",
    "🛰️ Yapay görsel — Havadan geniş açı (zorlu)": SAMPLE_IMAGE,
}

# VLM (Görsel-Dil Modeli)
VLM_MODEL_ID = "nvidia/LocateAnything-3B"
VLM_DEFAULT_PROMPT = "Locate all the cars in the image."
# Her kutu ~6 token tuttuğundan 2048 token ~340 tespite yeter;
# daha yüksek limit VRAM'i zorlayıp çıkarımı yavaşlatır. Model tekrar
# döngüsüne girerse limit dolana kadar üretir; tekrarlar parse_boxes'ta ayıklanır.
VLM_MAX_NEW_TOKENS = 2048

# YOLO varsayılanları
# 640'ta yüksek çözünürlüklü görsellerde araçlar ~15 piksele küçülüp kayboluyordu;
# 1920 örnek görselde tespiti ~5x artırdı (GPU'da çıkarım hâlâ <100 ms)
YOLO_IMG_SIZE = 1920
YOLO_DEFAULT_CONF = 0.25

# Tespit renkleri (RGB)
COLOR_EMPTY = (34, 197, 94)     # Yeşil  — boş park yeri
COLOR_OCCUPIED = (239, 68, 68)  # Kırmızı — dolu park yeri
COLOR_VLM = (168, 85, 247)      # Mor    — VLM tespiti

# Lejant için hex karşılıkları
HEX_EMPTY = "#22c55e"
HEX_OCCUPIED = "#ef4444"
HEX_VLM = "#a855f7"
