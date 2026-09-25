import fitz
from pathlib import Path

def extraer_texto_pdf(ruta: Path) -> str:
    texto = []

    with fitz.open(ruta) as documento:
        for pagina in documento:
            texto.append(pagina.get_text("text"))

    return "\n".join(texto)
