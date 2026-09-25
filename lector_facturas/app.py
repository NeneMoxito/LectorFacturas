import streamlit as st
from pathlib import Path
from procesamiento.gestor import procesar_carpeta
from config.config import UMBRAL_CONFIANZA

st.set_page_config(page_title="Lector de Facturas", page_icon="📄", layout="wide")

st.title("📄 Lector inteligente de facturas")
st.write("Procesa PDF e imágenes, identifica los 6 campos y exporta automáticamente los registros confiables a Excel.")

carpeta = st.text_input(
    "Ruta de la carpeta principal",
    value=str(Path("entrada").resolve()),
    help="Dentro de esta carpeta, cada subcarpeta se considera una asignación. Ejemplo: entrada/JUAN_PEREZ/factura01.jpg"
)

umbral = st.slider(
    "Umbral mínimo de confianza (%)",
    min_value=50,
    max_value=100,
    value=UMBRAL_CONFIANZA,
    step=1
)

if st.button("🚀 Procesar facturas", type="primary"):
    ruta = Path(carpeta)

    if not ruta.exists() or not ruta.is_dir():
        st.error("La carpeta indicada no existe.")
    else:
        with st.spinner("Procesando facturas..."):
            resultado = procesar_carpeta(ruta, umbral)

        st.success("Proceso terminado.")

        c1, c2, c3 = st.columns(3)
        c1.metric("Procesadas", resultado["procesadas"])
        c2.metric("Aprobadas", resultado["aprobadas"])
        c3.metric("Revisión", resultado["revision"])

        if resultado["excel"]:
            st.info(f"Excel generado: {resultado['excel']}")

        if resultado["errores"]:
            st.subheader("Errores")
            for error in resultado["errores"]:
                st.warning(error)

        if resultado["revision_detalle"]:
            st.subheader("Facturas que requieren revisión")
            st.dataframe(resultado["revision_detalle"], use_container_width=True)
