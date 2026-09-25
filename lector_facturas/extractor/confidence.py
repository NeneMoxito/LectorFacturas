def confianza_final(datos):
    """
    Primera versión: confianza basada en presencia/formato de los campos.
    Posteriormente puede sustituirse por una confianza OCR + IA más avanzada.
    """

    puntuacion = 0

    if datos.get("Fecha"):
        puntuacion += 15

    if str(datos.get("Codigo_Postal", "")).isdigit() and len(str(datos.get("Codigo_Postal"))) == 5:
        puntuacion += 15

    if datos.get("Razon_Social"):
        puntuacion += 20

    if datos.get("Producto"):
        puntuacion += 20

    if datos.get("Cantidad"):
        puntuacion += 15

    if datos.get("Total"):
        puntuacion += 15

    # Si la validación completa falla, penalizamos.
    if not datos.get("Valido", False):
        puntuacion = min(puntuacion, 89)

    return puntuacion
