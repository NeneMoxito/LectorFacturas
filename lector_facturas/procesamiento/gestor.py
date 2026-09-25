from pathlib import Path
from datetime import datetime
import pandas as pd

from config.config import EXTENSIONES_IMAGEN, EXTENSION_PDF
from procesamiento.pdf_reader import extraer_texto_pdf
from procesamiento.ocr import ocr_imagen, ocr_pdf
from extractor.fields import extraer_campos
from extractor.validator import validar_registro
from extractor.confidence import confianza_final


def obtener_archivos(carpeta: Path):
    extensiones = EXTENSIONES_IMAGEN | {EXTENSION_PDF}
    return [p for p in carpeta.rglob("*") if p.is_file() and p.suffix.lower() in extensiones]


def obtener_asignacion(archivo: Path, carpeta_raiz: Path):
    relativo = archivo.relative_to(carpeta_raiz)
    partes = relativo.parts

    # La primera carpeta debajo de la carpeta raíz es la asignación.
    if len(partes) >= 2:
        return partes[0]

    # Si el archivo está directamente en la raíz.
    return carpeta_raiz.name


def procesar_archivo(archivo: Path, carpeta_raiz: Path, umbral: int):
    asignacion = obtener_asignacion(archivo, carpeta_raiz)
    extension = archivo.suffix.lower()

    try:
        metodo = "OCR"

        if extension == EXTENSION_PDF:
            texto = extraer_texto_pdf(archivo)

            # Si el PDF no contiene suficiente texto útil, usamos OCR.
            if len(texto.strip()) >= 80:
                metodo = "PDF_TEXT"
            else:
                texto = ocr_pdf(archivo)
                metodo = "PDF_OCR"
        else:
            texto = ocr_imagen(archivo)
            metodo = "OCR"

        datos = extraer_campos(texto)
        datos["Asignacion"] = asignacion
        datos["Archivo"] = archivo.name
        datos["Ruta"] = str(archivo)
        datos["Metodo"] = metodo

        datos = validar_registro(datos)
        datos["Confianza"] = confianza_final(datos)

        if datos["Confianza"] >= umbral and datos["Valido"]:
            datos["Estado"] = "APROBADO"
        else:
            datos["Estado"] = "REVISION"

        datos["Fecha_Procesamiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return datos, None

    except Exception as e:
        return None, f"{archivo}: {e}"


def procesar_carpeta(carpeta: Path, umbral: int):
    archivos = obtener_archivos(carpeta)
    aprobadas = []
    revision = []
    errores = []

    for archivo in archivos:
        datos, error = procesar_archivo(archivo, carpeta, umbral)

        if error:
            errores.append(error)
            continue

        if datos["Estado"] == "APROBADO":
            aprobadas.append(datos)
        else:
            revision.append(datos)

    columnas = [
        "Asignacion", "Fecha", "Codigo_Postal", "Razon_Social",
        "Producto", "Cantidad", "Total", "Confianza",
        "Metodo", "Archivo", "Fecha_Procesamiento"
    ]

    salida_dir = Path("salida")
    salida_dir.mkdir(exist_ok=True)
    excel = salida_dir / "facturas_procesadas.xlsx"

    with pd.ExcelWriter(excel, engine="openpyxl") as writer:
        pd.DataFrame(aprobadas, columns=columnas).to_excel(
            writer, sheet_name="VENTAS", index=False
        )

        columnas_revision = columnas + ["Motivo", "Valido"]
        pd.DataFrame(revision, columns=columnas_revision).to_excel(
            writer, sheet_name="REVISION", index=False
        )

        pd.DataFrame(
            errores, columns=["Error"]
        ).to_excel(writer, sheet_name="ERRORES", index=False)

    return {
        "procesadas": len(aprobadas) + len(revision),
        "aprobadas": len(aprobadas),
        "revision": len(revision),
        "errores": errores,
        "excel": str(excel.resolve()),
        "revision_detalle": revision,
    }
