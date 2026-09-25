# Lector inteligente de facturas

## 1. Requisitos

- Python 3.12 recomendado
- Visual Studio Code
- Tesseract OCR instalado en Windows

Después de instalar Tesseract, si no está en PATH, edita `procesamiento/ocr.py` y agrega:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Para OCR en español, instala el paquete de idioma `spa`.

## 2. Crear entorno virtual

En la terminal de VS Code:

```bash
python -m venv .venv
```

Activar en Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 3. Estructura de entrada

```text
entrada/
├── JUAN_PEREZ/
│   ├── factura01.pdf
│   └── factura02.jpg
├── MARIA_GARCIA/
│   ├── factura03.png
│   └── factura04.pdf
```

El nombre de la primera carpeta será usado como `Asignacion`.

## 4. Ejecutar

```bash
streamlit run app.py
```

## 5. Salida

Se crea:

```text
salida/facturas_procesadas.xlsx
```

Hojas:

- VENTAS: facturas que superaron el umbral.
- REVISION: facturas que requieren revisión.
- ERRORES: archivos que no pudieron procesarse.

## Nota

Esta es una primera versión funcional. La extracción de campos usa reglas y expresiones regulares. Para producción conviene añadir un segundo nivel de IA/multimodal para facturas difíciles y mejorar el cálculo de confianza.
