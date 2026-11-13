import streamlit as st
from datetime import datetime
import os

# ==========================================
# IMPORTACIÓN DE DATOS EXTERNOS
# ==========================================
try:
    from data_signos import DATOS_CALENDARIO
except ImportError:
    st.error("❌ ERROR: No se encontró 'data_signos.py'. Asegúrate de que esté en la misma carpeta.")
    st.stop()

st.set_page_config(page_title="Tonalpohualli Mexica v12.4", layout="wide", page_icon="🗿")

# ==========================================
# CONSTANTES Y LISTAS MAESTRAS
# Fuente: Ortografía estándar INAH/Rafael Tena / Piña Garza
# Correlación: Basada en PDF guía (Ancla +61)
# ==========================================

SIGNOS_Esp = [
    "Cocodrilo", "Viento", "Casa", "Lagartija", "Serpiente",
    "Muerte", "Venado", "Conejo", "Agua", "Perro",
    "Mono", "Hierba Torcida", "Caña", "Jaguar", "Águila",
    "Buitre", "Movimiento", "Pedernal", "Lluvia", "Flor"
]

SIGNOS_Nah = [
    "Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl",
    "Miquiztli", "Mazatl", "Tochtli", "Atl", "Itzcuintli",
    "Ozomahtli", "Malinalli", "Acatl", "Ocelotl", "Cuauhtli",
    "Cozcacuauhtli", "Ollin", "Tecpatl", "Quiahuitl", "Xochitl"
]

NUMEROS_Nah = [
    "Ce", "Umey", "Eyi", "Nahui", "Macuilli",
    "Chicuace", "Chicome", "Chicuey", "Chicnahui", "Matlactli",
    "Matlactliomelli", "Matlactlimeyi", "Matlactlichicuey"
]

PORTADORES_AÑO_NAH = ["Tochtli", "Acatl", "Tecpatl", "Calli"]
PORTADORES_AÑO_ESP = ["Conejo", "Caña", "Pedernal", "Casa"]

ANCLA_TONALPOHUALLI = 61 

# ==========================================
# SEÑORES DE LAS TREVENAS (Dioses Patronos por Bloque de 13 días)
# Índice 0 = Trecena 1, Índice 19 = Trecena 20
# ==========================================
SEÑORES_TRECENA = {
    1: {"dios": "Tonacatecuhtli", "desc": "Señor de la creación y el sustento."},
    2: {"dios": "Tepeyollotl", "desc": "Corazón de la montaña, señor de los sismos."},
    3: {"dios": "Tlaloc", "desc": "Dios de la lluvia y la fertilidad agrícola."},
    4: {"dios": "Xiuhtecuhtli", "desc": "Señor del fuego antiguo y el tiempo."},
    5: {"dios": "Quetzalcoatl", "desc": "La Serpiente Emplumada, viento y sabiduría."},
    6: {"dios": "Mictlantecuhtli", "desc": "Señor del inframundo y la muerte."},
    7: {"dios": "Chalchiuhtlicue", "desc": "Diosa del agua dulce y los ríos."},
    8: {"dios": "Mayahuel", "desc": "Diosa del maguey y la embriaguez sagrada."},
    9: {"dios": "Xochiquetzal", "desc": "Diosa de las flores, el amor y la artesanía."},
    10: {"dios": "Xolotl", "desc": "Gemelo de Quetzalcoatl, guía de los muertos."},
    11: {"dios": "Itzpapalotl", "desc": "Mariposa de obsidiana, deidad guerrera nocturna."},
    12: {"dios": "Huehuecoyotl", "desc": "Coyote viejo, dios de la música y la danza."},
    13: {"dios": "Mixcoatl", "desc": "Dios de la caza y las estrellas matutinas."},
    14: {"dios": "Xipe Totec", "desc": "El desollado, renovación y agricultura."},
    15: {"dios": "Camaxtli", "desc": "Dios rojo de la caza y el cielo seco."},
    16: {"dios": "Cozcaquauhtli", "desc": "Señor del buitre, limpieza y vejez."},
    17: {"dios": "Tlazolteotl", "desc": "Diosa de la purificación y los secretos sexuales."},
    18: {"dios": "Ehecatl", "desc": "Manifestación de Quetzalcoatl como Viento."},
    19: {"dios": "Cuauhtli", "desc": "El Águila, sol de mediodía y guerra."},
    20: {"dios": "Tochtli", "desc": "El Conejo, luna y abundancia."}
}

# ==========================================
# MOTOR DE PRONÓSTICOS RECUPERADO (Versión Completa v9/v12)
# ==========================================

SIGNOS_ESTADO = {
    "Cipactli": "Favorable", "Ehecatl": "Desfavorable", "Calli": "Neutro",
    "Cuetzpalin": "Favorable", "Coatl": "Favorable", "Miquiztli": "Neutro",
    "Mazatl": "Favorable", "Tochtli": "Favorable", "Atl": "Desfavorable",
    "Itzcuintli": "Favorable", "Ozomahtli": "Favorable", "Malinalli": "Desfavorable",
    "Acatl": "Neutro", "Ocelotl": "Desfavorable", "Cuauhtli": "Favorable",
    "Cozcacuauhtli": "Favorable", "Ollin": "Neutro", "Tecpatl": "Desfavorable",
    "Quiahuitl": "Desfavorable", "Xochitl": "Favorable"
}

NUMERALES_INFLUENCIA = {
    1: "Fuerte", 2: "Débil", 3: "Fuerte", 4: "Fuerte", 5: "Desfavorable",
    6: "Débil", 7: "Favorable", 8: "Fuerte", 9: "Desfavorable", 10: "Favorable",
    11: "Neutro", 12: "Fuerte", 13: "Favorable"
}

def generar_pronostico(numeral, signo):
    estado_s = SIGNOS_ESTADO.get(signo, "Neutro")
    inf_n = NUMERALES_INFLUENCIA.get(numeral, "Neutro")
    
    if estado_s == "Favorable":
        if inf_n in ["Favorable", "Fuerte"]:
            return "🌟 DÍA EXCELENTE (Cualli Tonalli)", "Las energías están perfectamente alineadas a tu favor. Actúa sin titubear.", "success"
        elif inf_n == "Desfavorable":
            return "⚠️ DÍA NEUTRO CON OBSTÁCULOS", "El signo es bueno, pero el número exige prudencia ante malas vibras.", "warning"
        else:
            return "🙂 DÍA BUENO", "Aprovecha la naturaleza constructiva y positiva del signo de hoy.", "success"
            
    elif estado_s == "Desfavorable":
        if inf_n == "Desfavorable":
            return "🛑 DÍA ADVERSO (Amo Cualli)", "Día de resguardo. Evita discusiones, firmas importantes o riesgos innecesarios.", "error"
        elif inf_n in ["Favorable", "Fuerte"]:
            return "⚡ DÍA DE DESAFÍO", "La gran fuerza del número te dará la energía necesaria para superar la hostilidad del signo.", "warning"
        else:
            return "📉 DÍA CUIDADOSO", "Mantén un perfil bajo, sé paciente y fluye con el día sin forzar las cosas.", "warning"
            
    else: # Neutro
        if inf_n in ["Favorable", "Fuerte"]:
            return "🙂 DÍA PRODUCTIVO", "La fuerza del número inclina la balanza del signo neutro hacia el éxito.", "success"
        elif inf_n == "Desfavorable":
            return "⚠️ DÍA COMPLICADO", "La falta de rumbo del signo neutro se junta con una energía numérica pesada.", "warning"
        else:
            return "☯️ DÍA NEUTRO", "Día de equilibrio estricto. Momento ideal para la introspección y planeación.", "info"

# ==========================================
# FUNCIONES DE CÁLCULO CORE
# ==========================================

def es_bisiesto_juliano(año): return año % 4 == 0

def dias_hasta_mes(mes, año):
    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if es_bisiesto_juliano(año): dias_por_mes[2] = 29
    return sum(dias_por_mes[:mes])

def numero_juliano_corregido(fecha):
    años_anteriores = fecha.year - 1
    dias = años_anteriores * 365 + (años_anteriores // 4)
    dias += dias_hasta_mes(fecha.month, fecha.year)
    dias += fecha.day
    return dias

def ajuste_gregoriano(fecha):
    if fecha < datetime(1582, 10, 15): return 0
    elif fecha < datetime(1700, 3, 1): return 10
    elif fecha < datetime(1800, 3, 1): return 11
    elif fecha < datetime(1900, 3, 1): return 12
    elif fecha < datetime(2100, 3, 1): return 13
    else: return 14

def obtener_tonalpohualli(fecha):
    nj = numero_juliano_corregido(fecha)
    if fecha >= datetime(1582, 10, 15): nj -= ajuste_gregoriano(fecha)
    
    cifra = (nj + ANCLA_TONALPOHUALLI) % 260
    idx_ciclo = 259 if cifra == 0 else cifra - 1
    
    numero = (idx_ciclo % 13) + 1
    indice_signo = idx_ciclo % 20
    
    return numero, SIGNOS_Nah[indice_signo], SIGNOS_Esp[indice_signo], NUMEROS_Nah[numero - 1], idx_ciclo

def calcular_xiuhpohualli(fecha):
    nj = numero_juliano_corregido(fecha)
    if fecha >= datetime(1582, 10, 15): nj -= ajuste_gregoriano(fecha)
    total_dias = nj + 309
    años_totales = total_dias // 365
    marcador_absoluto = años_totales % 52 or 52
    num_marcador = marcador_absoluto % 13 or 13
    beta_idx = marcador_absoluto % 4 or 4
    portador_name = PORTADORES_AÑO_NAH[beta_idx - 1]
    portador_esp = PORTADORES_AÑO_ESP[beta_idx - 1]
    return f"{num_marcador}-{portador_name}", f"{num_marcador}-{portador_esp}"

def tonal_opuesto(indice_signo_actual):
    indice_opuesto = (indice_signo_actual + 10) % 20
    return SIGNOS_Nah[indice_opuesto], SIGNOS_Esp[indice_opuesto]

def get_clean_data(signo_key):
    """Busca en DATOS_CALENDARIO ignorando espacios en blanco."""
    # Intento directo
    data = DATOS_CALENDARIO.get(signo_key)
    if data:
        return data
    
    # Intento limpio (por si acaso hay espacios residuales en el dict externo)
    clean_key = signo_key.strip()
    for k, v in DATOS_CALENDARIO.items():
        if k.strip() == clean_key:
            return v
            
    return {}

# Helper para cargar imágenes con fallbacks robustos
def load_image_safe(base_path_prefix, name, extensions=['.png', '.jpg']):
    """
    Intenta encontrar una imagen usando varias convenciones de nombre.
    base_path_prefix: ej "assets/gods/"
    name: ej "Xipe Totec"
    """
    # Generamos variantes del nombre para buscar
    variants = []
    # 1. Original lower
    variants.append(name.lower())
    # 2. Replace spaces with underscore
    variants.append(name.replace(" ", "_").lower())
    # 3. Remove accents/spaces entirely (simple cleanup)
    clean_name = "".join(c for c in name if c.isalnum()).lower()
    variants.append(clean_name)
    
    # Eliminamos duplicados manteniendo orden
    seen = set()
    unique_variants = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            unique_variants.append(v)

    for ext in extensions:
        for var in unique_variants:
            full_path = f"{base_path_prefix}{var}{ext}"
            if os.path.exists(full_path):
                return full_path
                
    return None

# ==========================================
# INTERFAZ STREAMLIT
# ==========================================

with st.sidebar:
    st.title("⚙️ Configuración")
    fecha_input = st.date_input(
        "Ingresa tu fecha:", 
        value=datetime.today(),
        min_value=datetime(1500, 1, 1),
        max_value=datetime(2100, 12, 31)
    )
    st.divider()
    st.info("Usando correlación histórica Ancla +61.\nRango: 1500-2100 d.C.")

fecha_dt = datetime.combine(fecha_input, datetime.min.time())

# --- CÁLCULOS ---
numero, signo_nah, signo_esp, num_nah, idx_ciclo = obtener_tonalpohualli(fecha_dt)
xiuh_nah, xiuh_esp = calcular_xiuhpohualli(fecha_dt)
sign_op_nah, sign_op_esp = tonal_opuesto(idx_ciclo % 20)

# Generar Pronóstico
veredicto_texto, consejo_texto, veredicto_tipo = generar_pronostico(numero, signo_nah)

# Datos Simbólicos
datos_tonal = get_clean_data(signo_nah)
datos_nahualli = get_clean_data(sign_op_nah)

# Cálculo de Trecena y Señor
trecena_num = (idx_ciclo // 13) + 1
senor_trecena_info = SEÑORES_TRECENA.get(trecena_num, {"dios": "Desconocido", "desc": "Sin datos"})

# --- VISUALIZACIÓN ---
st.markdown("<h1 style='text-align: center;'>🌞 Cronología Ritual Mexica</h1>", unsafe_allow_html=True)
st.caption("Interpretación simbólica basada en la aritmética del Tonalpohualli y Xiuhpohualli.")

col_img_num, col_img_signo, col_info_central = st.columns([1, 1, 2])

with col_img_num:
    img_path_num = load_image_safe("assets/numbers/", str(numero))
    if img_path_num:
        st.image(img_path_num, caption=f"Número {numero} ({num_nah})", use_container_width=True)
    else:
        st.markdown(f"<div style='font-size: 50px; text-align:center;'>{numero}</div>", unsafe_allow_html=True)
        st.caption(f"Náhuatl: {num_nah}")

with col_img_signo:
    img_path_signo = load_image_safe("assets/days/", signo_nah)
    if img_path_signo:
        st.image(img_path_signo, caption=signo_esp, use_container_width=True)
    else:
        st.markdown(f"<div style='font-size: 50px; text-align:center;'>❓</div>")
        st.caption("Imagen no encontrada")

with col_info_central:
    st.header(f"{numero} {signo_nah}")
    st.subheader(f"({signo_esp})")
    
    badge_map = {"success": "#28a745", "warning": "#ffc107", "error": "#dc3545", "info": "#17a2b8"}
    color_hex = badge_map.get(veredicto_tipo, "#6c757d")
    
    # MOSTRAR VEREDICTO Y CONSEJO CLARAMENTE
    st.markdown(
        f'<div style="background-color:{color_hex}; color:white; padding:15px; border-radius:8px; margin-bottom:10px;">'
        f'<strong>{veredicto_texto}</strong><br>'
        f'<span style="font-size:0.9em;">{consejo_texto}</span>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.metric(label="Posición Ciclo (260)", value=f"{idx_ciclo + 1}/260")

st.divider()

tab_tonal, tab_nahualli, tab_trecena = st.tabs(["🔮 Tu Tonal (Destino)", "🐍 Tu Nahualli (Opuesto)", "🏛️ Señor de la Trecena"])

with tab_tonal:
    c_desc, c_deity = st.columns([2, 1])
    
    with c_desc:
        st.subheader("Significado Simbólico")
        desc_signo = datos_tonal.get('signo_desc', 'Descripción general del signo.')
        st.write(desc_signo)
        
        st.subheader("Influencia Numeral")
        efecto_num = f"El número {numero} aporta energía {'fuerte' if numero in [1,3,4,8,12] else ('caótica' if numero in [5,9] else 'equilibrada')}."
        st.write(efecto_num)
        
        st.info(f"**Elemento:** {datos_tonal.get('elemento', 'N/A')} | **Rumbo:** {datos_tonal.get('rumbo', 'N/A')}")

    with c_deity:
        st.subheader("Deidad Patrona del Día")
        dios_name = datos_tonal.get('dios', 'Desconocido')
        
        img_path_dios = load_image_safe("assets/gods/", dios_name)
        if img_path_dios:
            st.image(img_path_dios, caption=dios_name, use_container_width=True)
        else:
            st.markdown(f"**{dios_name}**")
            
        st.write(datos_tonal.get('dios_desc', ''))

with tab_nahualli:
    st.markdown("""
    > **Definición Metodológica:** El *Nahualli* aquí mostrado es el **signo opuesto** (avance de 10 posiciones). Representa la energía complementaria o espejo.
    """)
    
    c_img_op, c_desc_op, c_deity_op = st.columns([1, 2, 1])
    
    with c_img_op:
        st.subheader("Glifo del Nahualli")
        img_path_signo_op = load_image_safe("assets/days/", sign_op_nah)
        if img_path_signo_op:
            st.image(img_path_signo_op, caption=sign_op_esp, use_container_width=True)
        else:
            st.markdown(f"<div style='font-size: 50px; text-align:center;'>❓</div>")
            st.caption("Imagen no encontrada")

    with c_desc_op:
        st.subheader(f"Energía Complementaria: {numero} {sign_op_nah}")
        desc_op = datos_nahualli.get('signo_desc', 'Energía opuesta al signo de nacimiento.')
        st.write(desc_op)
        st.success(f"Tu Tonal ({signo_nah}) vs tu Nahualli ({sign_op_nah}).")
        
        st.info(f"**Elemento Opuesto:** {datos_nahualli.get('elemento', 'N/A')} | **Rumbo Opuesto:** {datos_nahualli.get('rumbo', 'N/A')}")

    with c_deity_op:
        st.subheader("Deidad Asociada al Nahualli")
        dios_op_name = datos_nahualli.get('dios', 'Desconocido')
        
        # Aquí está la clave: usamos load_image_safe para buscar la imagen del DIOS del Nahualli
        img_path_dios_op = load_image_safe("assets/gods/", dios_op_name)
        
        if img_path_dios_op:
            st.image(img_path_dios_op, caption=dios_op_name, use_container_width=True)
        else:
            st.markdown(f"**{dios_op_name}**")
            st.caption("(Imagen de deidad no encontrada)")
            
        st.write(datos_nahualli.get('dios_desc', ''))

with tab_trecena:
    st.subheader(f"Trecena #{trecena_num}")
    st.write(f"Este día pertenece al bloque de 13 días gobernado por:")
    
    c_trec_img, c_trec_txt = st.columns([1, 2])
    
    with c_trec_img:
        dios_trec_name = senor_trecena_info['dios']
        img_path_trec = load_image_safe("assets/gods/", dios_trec_name)
        
        if img_path_trec:
            st.image(img_path_trec, caption=dios_trec_name, use_container_width=True)
        else:
            st.markdown(f"**{dios_trec_name}**")
            st.caption("(Imagen no disponible)")

    with c_trec_txt:
        st.markdown(f"### 👹 {dios_trec_name}")
        st.write(senor_trecena_info['desc'])
        st.divider()
        st.caption("Los señores de las trecenas son las deidades principales que rigen el destino colectivo durante esos 13 días.")

st.divider()
col_año, col_footer = st.columns(2)

with col_año:
    st.metric(label="Año Tolteca (Xiuhpohualli)", value=xiuh_esp)
    st.caption(f"Marcador Náhuatl: **{xiuh_nah}**")

with col_footer:
    st.caption("Basado en la aritmética de Piña Garza (2003) y ortografía normalizada de Rafael Tena (INAH). Correlación Ancla +61.")