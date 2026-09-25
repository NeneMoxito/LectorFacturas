from pathlib import Path

EXTENSIONES_IMAGEN = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
EXTENSION_PDF = ".pdf"

UMBRAL_CONFIANZA = 90
IDIOMA_OCR = "spa+eng"

SALIDA_DIR = Path("salida")
SALIDA_DIR.mkdir(exist_ok=True)
