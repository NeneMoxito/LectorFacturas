import re
from datetime import datetime


def limpiar_texto(texto):
    texto = texto.replace("\r", "\n")
    texto = re.sub(r"[ \t]+", " ", texto)
    return texto


def buscar_fecha(texto):
    patrones = [
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",
    ]

    for patron in patrones:
        m = re.search(patron, texto)
        if m:
            valor = m.group(1)
            try:
                for formato in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y",
                                "%d-%m-%y", "%Y-%m-%d", "%Y/%m/%d"):
                    try:
                        return datetime.strptime(valor, formato).strftime("%Y-%m-%d")
                    except ValueError:
                        pass
            except Exception:
                pass

    return ""


def buscar_cp(texto):
    patrones = [
        r"(?:c\.?\s*p\.?|c[oó]digo\s+postal)\s*[:#-]?\s*(\d{5})",
        r"\b(\d{5})\b"
    ]

    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)

    return ""


def buscar_total(texto):
    patrones = [
        r"(?:total(?:\s+a\s+pagar)?|importe\s+total)\s*[:$]?\s*\$?\s*([\d,]+\.\d{2})",
        r"\btotal\b[^\d$]{0,20}\$?\s*([\d,]+\.\d{2})",
    ]

    encontrados = []
    for patron in patrones:
        encontrados.extend(re.findall(patron, texto, re.IGNORECASE))

    if encontrados:
        return encontrados[-1].replace(",", "")

    # Fallback: último importe con dos decimales.
    importes = re.findall(r"\$?\s*([\d,]+\.\d{2})", texto)
    return importes[-1].replace(",", "") if importes else ""


def buscar_cantidad(texto):
    patrones = [
        r"(?:cantidad|cant\.?|qty|unidades?)\s*[:#]?\s*(\d+(?:\.\d+)?)",
        r"(?:cant\.?|cantidad)\s*\n?\s*(\d+(?:\.\d+)?)"
    ]

    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)

    return ""


def buscar_razon_social(texto):
    patrones = [
        r"(?:raz[oó]n\s+social)\s*[:\-]?\s*(.+)",
        r"(?:cliente|receptor)\s*[:\-]?\s*(.+)",
    ]

    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            valor = m.group(1).strip()
            if valor:
                return valor[:150]

    # Fallback: buscar una línea que contenga SA/S.A./SC.
    for linea in texto.splitlines():
        linea = linea.strip()
        if re.search(r"\bS\.?\s*A\.?\b|\bS\.?\s*C\.?\b|\bS\.?\s*DE\s*C\.?\b", linea, re.I):
            if len(linea) > 5:
                return linea[:150]

    return ""


def buscar_producto(texto):
    etiquetas = [
        "descripcion", "descripción", "producto", "concepto", "articulo", "artículo"
    ]

    lineas = [x.strip() for x in texto.splitlines() if x.strip()]

    for i, linea in enumerate(lineas):
        if any(etiqueta in linea.lower() for etiqueta in etiquetas):
            if i + 1 < len(lineas):
                candidato = lineas[i + 1]

                # Evitamos devolver encabezados obvios.
                if not re.search(
                    r"cantidad|cant\.?|precio|importe|subtotal|total",
                    candidato,
                    re.I
                ):
                    return candidato[:200]

    return ""


def extraer_campos(texto):
    texto = limpiar_texto(texto)

    return {
        "Fecha": buscar_fecha(texto),
        "Codigo_Postal": buscar_cp(texto),
        "Razon_Social": buscar_razon_social(texto),
        "Producto": buscar_producto(texto),
        "Cantidad": buscar_cantidad(texto),
        "Total": buscar_total(texto),
    }
