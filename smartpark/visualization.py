"""Tespit kutularının görsel üzerine çizimi."""
import cv2


def draw_detections(img_np, boxes, color, fill_alpha=0.14, show_index=False):
    """
    Kutuları yarı saydam dolgu + kenarlık + opsiyonel numara etiketi ile çizer.
    Kalınlık ve yazı boyutu görsel çözünürlüğüne göre ölçeklenir.
    """
    if not boxes:
        return img_np

    h, w = img_np.shape[:2]
    thickness = max(2, round(min(w, h) / 400))
    font_scale = max(0.45, min(w, h) / 1200)

    # Yarı saydam iç dolgu
    if fill_alpha > 0:
        overlay = img_np.copy()
        for (x1, y1, x2, y2) in boxes:
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
        img_np = cv2.addWeighted(overlay, fill_alpha, img_np, 1 - fill_alpha, 0)

    # Kenarlık ve numara etiketi
    for i, (x1, y1, x2, y2) in enumerate(boxes, 1):
        cv2.rectangle(img_np, (x1, y1), (x2, y2), color, thickness)
        if show_index:
            label = str(i)
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
            ly = y1 + th + 4 if y1 - th - 6 < 0 else y1 - 4
            cv2.rectangle(img_np, (x1, ly - th - 4), (x1 + tw + 8, ly + 4), color, -1)
            cv2.putText(img_np, label, (x1 + 4, ly), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, (15, 17, 26), 2, cv2.LINE_AA)

    return img_np
