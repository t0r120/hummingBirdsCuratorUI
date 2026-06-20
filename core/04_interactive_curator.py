import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from datetime import datetime

from PIL import Image
from pathlib import Path


# ==============================================================================
# PROJECT: Trochilidae Knowledge Graph (TKG)
# STEP 04: Interactive data curator
# Input files:
# if there_is_species_range:
#   -> tkg_hummingbirds_research_grade_193_383.csv"
#   -> color_dictionary_hbw_wikidata.csv
# else:
#   -> tkg_hummingbirds_research_grade.csv"
#   -> color_dictionary_hbw_wikidata.csv
# SYSTEM ARCHITECT: Isra | BIO-CURATION LEAD: Layla
# ==============================================================================

# ============================
# Initial setup
# ============================
st.set_page_config(page_title="Curador Visual TKG", layout="wide")

# ============================
# Curator user data
# ============================
with st.sidebar:
    st.header("👤 Sesión de Curaduría")
    # Se inicializa un input con un nombre predeterminado
    curador = st.text_input("Nombre del Curador", value="Jair")

    session_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.write(f"**Inicio:** {session_time}")

    # El archivo de salida guarda tus datos curados
    ARCHIVO_SALIDA = 'data/TKG_Curation_Progress_193_383.csv'
    st.caption(f"Guardando en: {ARCHIVO_SALIDA}")

# ==========================================
# 1. LOAD AND DATA PROCESSING
# ==========================================
DIRECTORIO_ACTUAL = Path(__file__).parent
RAIZ_PROYECTO = DIRECTORIO_ACTUAL.parent

@st.cache_data
def cargar_datos():
    # 1. Cargar todas las observaciones
    RUTA_OBSERVACIONES = RAIZ_PROYECTO / 'data' / 'tkg_hummingbirds_research_grade.csv'
    RUTA_COLORES = RAIZ_PROYECTO / 'data' / 'color_dictionary_hbw_wikidata.csv'

    df_obs_full = pd.read_csv(RUTA_OBSERVACIONES)

    # 2. Cargar el Diccionario HBW respetando sus encabezados
    df_colors = pd.read_csv(RUTA_COLORES)

    # Renombramos 'hbw_name' a 'color_name' para el código visual
    df_colors.rename(columns={'hbw_name': 'color_name'}, inplace=True)

    # 3. Limpieza de Hexadecimales
    # Llenamos vacíos con un gris temporal (por si alguna fila no tiene codigo)
    df_colors['hex'] = df_colors['hex'].fillna('CCCCCC').astype(str).str.strip()

    # Le agregamos el '#' solo a los que no lo tienen
    df_colors['hex'] = df_colors['hex'].apply(lambda x: '#' + x if not x.startswith('#') else x)

    # Preparamos el texto para los menús desplegables
    df_colors['color_name'] = df_colors['color_name'].fillna('Desconocido')

    # --- AGREGAR 'DATA DEFICIENT' AL INICIO ---
    if not (df_colors['wikidata_qid'] == 'Q106512361').any():
        dd_row = pd.DataFrame([{
            'color_name': 'Data Deficient',
            'wikidata_qid': 'Q106512361',
            'hex': '#000000',  # Negro/Vacío visualmente
            'type': 'NA'
        }])
        df_colors = pd.concat([dd_row, df_colors], ignore_index=True)

    df_colors['display'] = df_colors['color_name'] + " [" + df_colors['wikidata_qid'].astype(str) + "]"

    # 4. batch filtering
    especies_unicas = list(df_obs_full['scientific_name'].unique())

    #
    try:
        especie_historial = pd.read_csv('data/TKG_Curation_Progress_193_383.csv')
        nombre_inicio_lote = especie_historial['scientific_name'].iat[0]
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Fallback de seguridad si el archivo aún no existe
        nombre_inicio_lote = especies_unicas[0]

    if nombre_inicio_lote in especies_unicas:
        idx_inicio = especies_unicas.index(nombre_inicio_lote)
        lote_especies = especies_unicas[idx_inicio:]
    else:
        lote_especies = especies_unicas

    df_lote = df_obs_full[df_obs_full['scientific_name'].isin(lote_especies)]

    return df_lote, lote_especies, df_colors


df_obs, lista_especies, df_colors = cargar_datos()
total_especies = len(lista_especies)
# ==========================================
# =                                        =
# ==========================================


# ==========================================
# 2. MEMORY STATE MANAGEMENT (AUTOSAVE)
# ==========================================
if 'indice_especie' not in st.session_state:
    try:
        # Read historial
        especie_historial = pd.read_csv(ARCHIVO_SALIDA)
        ultima_especie = especie_historial['scientific_name'].iat[-1]

        # Buscamos dónde está esa especie en la lista COMPLETA
        if ultima_especie in lista_especies:
            idx_reanudar = lista_especies.index(ultima_especie) + 1
            # Prevención por si ya terminaste toda la lista
            if idx_reanudar >= total_especies:
                idx_reanudar = total_especies - 1

            st.session_state.indice_especie = idx_reanudar
        else:
            st.session_state.indice_especie = 0

    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError):
        # Si el archivo no existe o está vacío, empezamos desde 0
        st.session_state.indice_especie = 0


def especie_siguiente():
    if st.session_state.indice_especie < total_especies - 1:
        st.session_state.indice_especie += 1


def especie_anterior():
    if st.session_state.indice_especie > 0:
        st.session_state.indice_especie -= 1


# ==========================================
# =                                        =
# ==========================================


# ==========================================
# 3. USER INTERFACE (UX OPTIMIZADO)
# ==========================================

especie_actual = lista_especies[st.session_state.indice_especie]
datos_especie = df_obs[df_obs['scientific_name'] == especie_actual]

# --- PALETA VISUAL EN EL SIDEBAR ---
with st.sidebar:
    st.markdown("---")
    st.subheader("🎨 Buscador de Colores")

    busqueda = st.text_input("🔍 Buscar color (ej. 'green')...", "").lower().strip()

    if busqueda:
        df_filtrado = df_colors[df_colors['color_name'].str.lower().str.contains(busqueda, na=False)]
        if df_filtrado.empty:
            st.warning("No se encontraron colores.")
    else:
        st.info("Muestra:")
        df_filtrado = df_colors.head(15)

    # HTML ajustado a 100% de ancho para adaptarse al sidebar
    html_colores = "<div style='font-family: sans-serif; padding: 5px;'>"
    for _, fila in df_filtrado.iterrows():
        color_hex = fila['hex']
        nombre = fila['color_name']
        qid = fila['wikidata_qid']

        html_colores += f"""
        <div style='display: flex; align-items: center; margin-bottom: 10px; width: 100%;'>
            <div style='min-width: 30px; height: 30px; background-color: {color_hex}; border: 1px solid #aaa; border-radius: 4px; margin-right: 12px;'></div>
            <div style='overflow: hidden; text-overflow: ellipsis;'>
                <span style='font-size: 13px; color: white; font-weight: bold;'>{nombre}</span><br>
                <span style='font-size: 10px; color: #666;'>{qid} | {color_hex}</span>
            </div>
        </div>
        """
    html_colores += "</div>"
    components.html(html_colores, height=400, scrolling=True)

# --- MAIN SECTION ---
col_visor, col_preguntas = st.columns([1.5, 1], gap="large")

with col_visor:
    st.markdown(f"### 📷 {especie_actual}")
    st.write(datos_especie.head(3))
    st.progress((st.session_state.indice_especie + 1) / total_especies)
    st.caption(f"Progreso: Especie {st.session_state.indice_especie + 1} de {total_especies}")
    if st.session_state.indice_especie == 174:
        st.markdown(f'HAZ CURADO TODAS LAS ESPECIES 🐦!!! {st.session_state.indice_especie}')
    URLs_fotos = datos_especie['image_url'].tolist()[:3]

    if URLs_fotos:
        for idx, url in enumerate(URLs_fotos):
            try:
                st.image(url, use_container_width=True, caption=f"Evidencia {idx + 1}")
            except Exception:
                st.error(f"⚠️ URL rota o inválida para imagen {idx + 1}")
    else:
        st.warning("No hay fotos en grado de investigación para esta especie.")

    st.write("---")
    # NAV BUTTONS
    c1, c2 = st.columns(2)
    with c1:
        st.button("⬅️ Anterior", on_click=especie_anterior, use_container_width=True)
    with c2:
        st.button("Siguiente ➡️", on_click=especie_siguiente, use_container_width=True)

    # ANATOMY IMAGE REFERENCE
    try:
        RUTA_IMAGEN = RAIZ_PROYECTO / 'img' / 'colibri.png'
        img = Image.open(RUTA_IMAGEN)
        st.image(img, caption="Anatomía de referencia", use_container_width=True)
    except FileNotFoundError:
        st.warning(f"No se encontró la imagen de referencia en: {RUTA_IMAGEN}")

with col_preguntas:
    st.subheader("📝 Matriz Fenotípica")

    with st.form("form_curaduria", clear_on_submit=False):
        sexo = st.selectbox("Sexo (P21)", ["Unknown", "Male", "Female", "Juvenile"])
        st.write("---")

        mapa_regiones = {
            "Crown": "Corona", "Crest": "Cresta", "Nape": "Nuca", "Chin": "Barbilla",
            "Bill": "Pico", "Gorget": "Gorguera", "Breast": "Pecho", "Belly": "Vientre",
            "Flanks": "Flancos", "Back": "Dorso", "Rump": "Rabadilla",
            "Tail_coverts": "Coberteras caudales", "Rectrices": "Rectrices", "Remiges": "Rémiges"
        }

        anotaciones = {}
        for reg_en, reg_es in mapa_regiones.items():
            anotaciones[reg_en] = st.selectbox(f"{reg_es} / {reg_en}", options=df_colors['display'].tolist())

        st.write("---")
        st.markdown("**Evaluación de Evidencia**")
        q1 = st.selectbox("Nitidez / Distancia", ["Alta: Acercamiento y nítido", "Media: Distante o algo borroso",
                                                  "Baja: Muy borroso o pixelado"])
        q2 = st.selectbox("Iluminación", ["Óptima: Luz natural directa", "Promedio: Algunas sombras o contraluz",
                                          "Pobre: Sombra pesada / Sobreexpuesto"])
        q3 = st.selectbox("Visibilidad", ["Total: Todas las regiones claras", "Parcial: Mayoría de regiones claras",
                                          "Mínima: Oclusión significativa"])

        submit = st.form_submit_button("💾 Guardar Especie", use_container_width=True)
        # SCORE
        if submit:
            puntos = 0
            if q1.startswith("Alta"):
                puntos += 2
            elif q1.startswith("Media"):
                puntos += 1

            if q2.startswith("Óptima"):
                puntos += 2
            elif q2.startswith("Promedio"):
                puntos += 1

            if q3.startswith("Total"): puntos += 1

            confianza_final = max(1, puntos)
            id_referencia = datos_especie.iloc[0]['id'] if not datos_especie.empty else "N/A"
            metadata_str = f"User: {curador} | Session: {session_time}"

            datos_guardar = {
                'observation_id_ref': id_referencia,
                'scientific_name': especie_actual,
                'sex_P21': sexo,
                'confidence_score': confianza_final,
                'annotator_metadata': metadata_str
            }

            for reg_en, val in anotaciones.items():
                qid = val.split("[")[-1].replace("]", "")
                datos_guardar[reg_en] = qid

            df_nuevo = pd.DataFrame([datos_guardar])
            file_exists = os.path.isfile(ARCHIVO_SALIDA)
            df_nuevo.to_csv(ARCHIVO_SALIDA, mode='a', header=not file_exists, index=False)

            st.success(f"¡Guardado! (Score: {confianza_final}/5)")

# ==========================================
# =               END                      =
# ==========================================