"""NVIDIA LocateAnything-3B (VLM) yükleme ve çıkarım katmanı."""
import re
import time

import streamlit as st
import torch
from PIL import Image

from smartpark.config import VLM_MODEL_ID, VLM_MAX_NEW_TOKENS


@st.cache_resource
def load_vlm_model(hf_token=None):
    """
    LocateAnything-3B modelini ve işlemcisini Hugging Face'den yükler.

    CUDA varsa model 4-bit (NF4) kuantalanarak yüklenir: bfloat16 hali (~7.8 GB)
    8 GB VRAM'i tek başına doldurup KV cache'i sistem belleğine taşırdığından
    çıkarım dakikalar sürüyordu; 4-bit ağırlıklar (~2.5 GB) ile her şey VRAM'e sığar.
    CUDA yoksa CPU üzerinde float32 kullanılır.
    """
    from transformers import AutoModel, AutoProcessor

    device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        processor = AutoProcessor.from_pretrained(
            VLM_MODEL_ID,
            trust_remote_code=True,
            token=hf_token
        )
        if device == "cuda":
            from transformers import BitsAndBytesConfig
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            model = AutoModel.from_pretrained(
                VLM_MODEL_ID,
                trust_remote_code=True,
                dtype=torch.bfloat16,
                quantization_config=quant_config,
                device_map={"": 0},
                token=hf_token
            )
        else:
            model = AutoModel.from_pretrained(
                VLM_MODEL_ID,
                trust_remote_code=True,
                dtype=torch.float32,
                token=hf_token
            ).to(device)
        return model, processor, device
    except Exception as e:
        st.error(f"LocateAnything-3B modeli yüklenirken hata oluştu: {e}")
        return None, None, device


def parse_boxes(answer: str, width: int, height: int):
    """
    LocateAnything-3B'nin <box><x1><y1><x2><y2></box> formatındaki çıktılarını
    piksel koordinatlarına çevirir. Model koordinatları [0, 1000] aralığında normalizedir.

    Model EOS üretmeden tekrar döngüsüne girebiliyor: geçerli kutulardan sonra
    aynı kutuyu token limiti dolana kadar basıyor (ör. 109 gerçek kutu + 232 kopya
    = "340 araba"). Bu yüzden yinelenen kutular ayıklanır ve aynı kutu arka arkaya
    tekrar etmeye başladığında çıktının kalanı çöp sayılıp parse durdurulur.
    """
    boxes = []
    seen = set()
    prev = None
    pattern = r"<box><(\d+)><(\d+)><(\d+)><(\d+)></box>"
    for match in re.finditer(pattern, answer):
        try:
            coords = tuple(int(g) for g in match.groups())
        except Exception:
            continue
        if coords == prev:
            break
        prev = coords
        if coords in seen:
            continue
        seen.add(coords)
        x1, y1, x2, y2 = coords
        boxes.append((
            int((x1 / 1000.0) * width),
            int((y1 / 1000.0) * height),
            int((x2 / 1000.0) * width),
            int((y2 / 1000.0) * height),
        ))
    return boxes


def run_vlm_locate(model, processor, device, image: Image.Image, prompt_text: str):
    """LocateAnything-3B ile görsel grounding çıkarımı yapar."""
    image_rgb = image.convert("RGB")
    width, height = image.size

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt_text}
            ]
        }
    ]

    start_time = time.time()

    text_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    # İşlemci, görselleri tekil nesne değil liste olarak bekler
    inputs = processor(images=[image_rgb], text=text_prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        # Modelin özel generate() metodu tokenizer'ı ve use_cache=True'yu açıkça ister
        # ve token ID yerine doğrudan çözümlenmiş metin (string) döndürür
        answer = model.generate(
            **inputs,
            tokenizer=processor.tokenizer,
            max_new_tokens=VLM_MAX_NEW_TOKENS,
            use_cache=True
        )

    inference_time_ms = (time.time() - start_time) * 1000

    return parse_boxes(answer, width, height), answer, inference_time_ms


def get_vlm_boxes(image: Image.Image, prompt_text: str):
    """VLM modelini yükleyip görsel üzerinde çıkarım çalıştırır."""
    with st.spinner("📦 NVIDIA LocateAnything-3B modeli belleğe yükleniyor (ilk seferde uzun sürebilir)..."):
        model, processor, device = load_vlm_model()

    if model is None or processor is None:
        st.error("VLM modeli yüklenemedi. Donanım veya kütüphane bağlantılarını kontrol edin.")
        st.stop()

    with st.spinner(f"⚡ LocateAnything-3B görsel çıkarımı yapılıyor ({device.upper()})..."):
        return run_vlm_locate(model, processor, device, image, prompt_text)
