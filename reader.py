import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from datetime import datetime
import glob
from PIL import Image

# ===========================
# imports
# ===========================


# ============================
# setpage inicializa la pagina
# ============================
st.set_page_config(page_title="Curador Visual TKG", layout="wide")
# ============================
# Registro del curador
# ============================
with st.sidebar:
    st.header("👤 Sesión de Curaduría")
    # Ponemos tu nombre por defecto para agilizar
    #Se inicializa un input cpn un nombre predeterminado (Jair/Karen)
    curador = st.text_input("Nombre del Curador", value="Jair")

    session_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.write(f"**Inicio:** {session_time}")

    # El archivo de salida guarda tus datos curados
    # Cambia esta linea por data/TKG_Curation_Progress_0_193.csv
    ARCHIVO_SALIDA = 'data/TKG_Curation_Progress_193_383.csv'
    st.caption(f"Guardando en: {ARCHIVO_SALIDA}")

# ==========================================
# 1. CARGA Y PROCESAMIENTO DE DATOS
# ==========================================
@st.cache_data
def cargar_datos():
    # 1. Cargar todas las observaciones
    df_obs_full = pd.read_csv('data/tkg_hummingbirds_research_grade.csv')

    # 2. Cargar el Diccionario HBW respetando sus encabezados
    df_colors = pd.read_csv('data/color_dictionary_hbw_wikidata.csv')

    # Renombramos 'hbw_name' a 'color_name' para que el resto del código visual funcione sin cambios
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
            # Columna / Fila
            'color_name': 'Data Deficient',
            'wikidata_qid': 'Q106512361',
            'hex': '#000000',  # Negro/Vacío visualmente
            'type': 'NA'
        }])
        df_colors = pd.concat([dd_row, df_colors], ignore_index=True)
    df_colors['display'] = df_colors['color_name'] + " [" + df_colors['wikidata_qid'].astype(str) + "]"

    # 4. Filtro Inteligente del Lote
    especies_unicas = list(df_obs_full['scientific_name'].unique())
    #Cambia el archivo al rango corrrespondiente
    especie_historial = pd.read_csv('data/TKG_Curation_Progress_193_383.csv')
    nombre_inicio_lote = especie_historial['scientific_name'].iat[0]
    #nombre_inicio_lote = 'Heliodoxa branickii'

    if nombre_inicio_lote in especies_unicas:
        idx_inicio = especies_unicas.index(nombre_inicio_lote)
        lote_especies = especies_unicas[idx_inicio:]

    else:
        lote_especies = especies_unicas

    df_lote = df_obs_full[df_obs_full['scientific_name'].isin(lote_especies)]

    return df_lote, lote_especies, df_colors


df_obs, lista_especies, df_colors = cargar_datos()
total_especies = len(lista_especies)  # Esto se mantendrá firme en 174




# ==========================================
# 2. GESTIÓN DE ESTADO (MEMORIA Y AUTOGUARDADO)
# ==========================================
if 'indice_especie' not in st.session_state:
    try:
        # Leemos el historial
        especie_historial = pd.read_csv(ARCHIVO_SALIDA)
        ultima_especie = especie_historial['scientific_name'].iat[-1]

        # Buscamos dónde está esa especie en la lista COMPLETAstrea
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
# 3. INTERFAZ DE USUARIO
# ==========================================
col_paleta, col_visor, col_preguntas = st.columns([1, 2, 1.2])

especie_actual = lista_especies[st.session_state.indice_especie]

datos_especie = df_obs[df_obs['scientific_name'] == especie_actual]


# --- COLUMNA CENTRAL: VISOR MÚLTIPLE ---
with col_visor:
    st.markdown(f"### 📷 {especie_actual}")
    st.write(datos_especie.head(3))
    st.markdown(f"**Progreso del Lote:** Especie {st.session_state.indice_especie + 1} de {total_especies}")

    # Limitar a un máximo de 3 fotos para mantener la limpieza visual
    URLs_fotos = datos_especie['image_url'].tolist()[:3]

    if URLs_fotos:
        cols_fotos = st.columns(len(URLs_fotos))
        for idx, url in enumerate(URLs_fotos):
            with cols_fotos[idx]:
                st.image(url, width='stretch', caption=f"Evidencia {idx + 1}")
    else:
        st.warning("No hay fotos en grado de investigación para esta especie.")

    # Controles de navegación
    st.write("---")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.button("⬅️ Especie Anterior", on_click=especie_anterior, width='stretch')
    with c3:
        st.button("Siguiente Especie ➡️", on_click=especie_siguiente, width='stretch')

    img = Image.open('/home/t0r120/bioScripts/hummingBirdUI/colibri.png')

    # Mostrarla en la app
    html_img = st.image(img, caption="Descripción de la imagen", width=500)

# --- COLUMNA IZQUIERDA: PALETA VISUAL (BUSCADOR DINÁMICO) ---
with col_paleta:
    st.subheader("🎨 Buscador de Tonos")

    # 1. Barra de búsqueda
    busqueda = st.text_input("🔍 Buscar color en inglés (ej. 'green')...", "").lower().strip()

    st.markdown("---")

    # 2. Lógica de filtrado Simple (Solo busca en la columna original de HBW)
    if busqueda:
        df_filtrado = df_colors[df_colors['color_name'].str.lower().str.contains(busqueda, na=False)]

        if df_filtrado.empty:
            st.warning("No se encontraron colores con ese término.")
    else:
        st.info("Escribe arriba para buscar, o mira esta muestra:")
        df_filtrado = df_colors.head(15)

    # 3. Renderizado HTML
    html_colores = "<div style='font-family: sans-serif; padding: 5px;'>"
    for _, fila in df_filtrado.iterrows():
        color_hex = fila['hex']
        nombre = fila['color_name']
        qid = fila['wikidata_qid']

        html_colores += f"""
        <div style='display: flex; align-items: center; margin-bottom: 10px;'>
            <div style='width: 30px; height: 30px; background-color: {color_hex}; border: 1px solid #aaa; border-radius: 4px; margin-right: 12px; box-shadow: 1px 1px 3px rgba(0,0,0,0.2);'></div>
            <div>
                <span style='font-size: 14px; color: white; font-weight: bold;'>{nombre}</span><br>
                <span style='font-size: 11px; color: #666;'>{qid} | {color_hex}</span>
            </div>
        </div>
        """
    html_colores += "</div>"

    components.html(html_colores, height=500, scrolling=True)


# --- COLUMNA DERECHA: REGISTRO ANATÓMICO ---
with col_preguntas:
    st.subheader("📝 Matriz Fenotípica")

    with st.form("form_curaduria", clear_on_submit=False):

        # 1. Identificación de Sexo
        sexo = st.selectbox("Sexo (P21)", ["Unknown", "Male", "Female", "Juvenile"])
        st.write("---")

        # 2. Regiones Anatómicas (Mapeo a Español)
        mapa_regiones = {
            "Crown": "Corona", "Crest": "Cresta", "Nape": "Nuca", "Chin": "Barbilla",
            "Bill": "Pico", "Gorget": "Gorguera", "Breast": "Pecho", "Belly": "Vientre",
            "Flanks": "Flancos", "Back": "Dorso", "Rump": "Rabadilla",
            "Tail_coverts": "Coberteras caudales", "Rectrices": "Rectrices", "Remiges": "Rémiges"
        }

        anotaciones = {}
        form_c1, form_c2 = st.columns(2)

        for i, (reg_en, reg_es) in enumerate(mapa_regiones.items()):
            target_col = form_c1 if i < 7 else form_c2
            anotaciones[reg_en] = target_col.selectbox(f"{reg_es} / {reg_en}", options=df_colors['display'].tolist())

        # 3. Evaluación de Calidad Automática (Las 3 preguntas)
        st.write("---")
        st.markdown("**Evaluación de Evidencia**")
        q1 = st.selectbox("Nitidez / Distancia", ["Alta: Acercamiento y nítido", "Media: Distante o algo borroso",
                                                  "Baja: Muy borroso o pixelado"])
        q2 = st.selectbox("Iluminación", ["Óptima: Luz natural directa", "Promedio: Algunas sombras o contraluz",
                                          "Pobre: Sombra pesada / Sobreexpuesto"])
        q3 = st.selectbox("Visibilidad", ["Total: Todas las regiones claras", "Parcial: Mayoría de regiones claras",
                                          "Mínima: Oclusión significativa"])

        submit = st.form_submit_button("💾 Guardar Especie", width='stretch')

        if submit:
            # Lógica de conversión a puntos (como en R)
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

            confianza_final = max(1, puntos)  # Asegura que el mínimo sea 1

            # Preparar datos base
            id_referencia = datos_especie.iloc[0]['id'] if not datos_especie.empty else "N/A"
            metadata_str = f"User: {curador} | Session: {session_time}"

            datos_guardar = {
                'observation_id_ref': id_referencia,
                'scientific_name': especie_actual,
                'sex_P21': sexo,
                'confidence_score': confianza_final,
                'annotator_metadata': metadata_str
            }

            # Guardar regiones y extraer QIDs
            for reg_en, val in anotaciones.items():
                qid = val.split("[")[-1].replace("]", "")
                datos_guardar[reg_en] = qid

            # Escribir en CSV
            df_nuevo = pd.DataFrame([datos_guardar])
            file_exists = os.path.isfile(ARCHIVO_SALIDA)
            df_nuevo.to_csv(ARCHIVO_SALIDA, mode='a', header=not file_exists, index=False)

            st.success(f"¡Guardado! (Score de calidad: {confianza_final}/5)")