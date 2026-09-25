from pathlib import Path
import cv2
import pytesseract
import fitz

from config.config import IDIOMA_OCR


def preparar_imagen(ruta: Path):
    imagen = cv2.imread(str(ruta))

    if imagen is None:
        raise ValueError(f"No se pudo abrir la imagen: {ruta}")

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aumentamos tamaño para mejorar OCR.
    gris = cv2.resize(gris, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # Reducción de ruido.
    gris = cv2.GaussianBlur(gris, (3, 3), 0)

    # Contraste adaptativo.
    procesada = cv2.adaptiveThreshold(
        gris,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return procesada


def ocr_imagen(ruta: Path) -> str:
    imagen = preparar_imagen(ruta)

    texto = pytesseract.image_to_string(
        imagen,
        lang=IDIOMA_OCR,
        config="--psm 6"
    )

    return texto


def ocr_pdf(ruta: Path) -> str:
    textos = []

    with fitz.open(ruta) as documento:
        for pagina in documento:
            pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            imagen = pix.tobytes("png")

            import numpy as np
            array = np.frombuffer(imagen, dtype=np.uint8)
            img = cv2.imdecode(array, cv2.IMREAD_COLOR)

            gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gris = cv2.resize(gris, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            gris = cv2.GaussianBlur(gris, (3, 3), 0)

            procesada = cv2.adaptiveThreshold(
                gris, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31, 11
            )

            textos.append(
                pytesseract.image_to_string(
                    procesada,
                    lang=IDIOMA_OCR,
                    config="--psm 6"
                )
            )

    return "\n".join(textos)
