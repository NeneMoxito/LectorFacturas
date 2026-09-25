import re


def validar_registro(datos):
    problemas = []

    if not datos.get("Fecha"):
        problemas.append("Fecha no encontrada")

    cp = str(datos.get("Codigo_Postal", ""))
    if not re.fullmatch(r"\d{5}", cp):
        problemas.append("Código postal inválido")

    if not datos.get("Razon_Social"):
        problemas.append("Razón Social no encontrada")

    if not datos.get("Producto"):
        problemas.append("Producto no encontrado")

    try:
        cantidad = float(str(datos.get("Cantidad", "")).replace(",", ""))
        if cantidad <= 0:
            problemas.append("Cantidad inválida")
    except Exception:
        problemas.append("Cantidad inválida")

    try:
        total = float(str(datos.get("Total", "")).replace(",", ""))
        if total < 0:
            problemas.append("Total inválido")
    except Exception:
        problemas.append("Total inválido")

    datos["Valido"] = len(problemas) == 0
    datos["Motivo"] = "; ".join(problemas)

    return datos
