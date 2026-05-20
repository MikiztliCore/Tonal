import streamlit as st
from datetime import datetime
import os
from PIL import Image

# Configuración de la página web (Título y pestaña)
st.set_page_config(page_title="Tonalpohualli Diario", page_icon="🌞", layout="centered")

# --- LISTAS NATIVAS DE TU ALGORITMO ---
signos_Esp = [
    "Cocodrilo", "Viento", "Casa", "Lagartija", "Serpiente",
    "Muerte", "Venado", "Conejo", "Agua", "Perro",
    "Mono", "Fibra de maguey", "Carrizo", "Jaguar", "Águila",
    "Cóndor", "Movimiento", "Pedernal", "Lluvia", "Flor"
]

signos_Nah = [
    "Cipactli", "Ehecatl", "Calli", "Cuetzpalli", "Coatl",
    "Miquiztli", "Mazatl", "Tochtli", "Atl", "Itzcuintli",
    "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Cuauhtli",
    "Cozcaquauhtli", "Ollin", "Tecpatl", "Quiahuitl", "Xochitl"
]

numeros_Nah = [
    "ce", "ume", "eyi", "nahui", "macuil",
    "chicuace", "chicume", "chicueyi", "chicnahui", "matlac",
    "matlacce", "matlacume", "matlacueyi"
]

año_Nah = ["acatl", "tecpatl", "calli", "tochtli"]
año_Esp = ["carrizo", "pedernal", "casa", "conejo"]

# --- DICCIONARIOS DE PRONÓSTICO ---
SIGNOS_PRONOSTICO = {
    "Cipactli": {"estado": "Favorable", "desc": "Inicio, abundancia y energía vital. Excelente para nuevos proyectos."},
    "Ehecatl": {"estado": "Desfavorable", "desc": "Inconstancia y vientos de cambio drásticos. Mal día para firmar acuerdos."},
    "Calli": {"estado": "Neutro", "desc": "Reflexión e interiorización. Favorable para la familia, peligroso para el exterior."},
    "Cuetzpalli": {"estado": "Favorable", "desc": "Salud, agilidad y autorreparación. Excelente para el esfuerzo físico."},
    "Coatl": {"estado": "Favorable", "desc": "Sabiduría, fuerza mística y renovación. No acumules rencores hoy."},
    "Miquiztli": {"estado": "Neutro", "desc": "Transformación y memoria de los ancestros. Momento de soltar lo viejo."},
    "Mazatl": {"estado": "Favorable", "desc": "Intuición y timidez. Día de estar alerta pero actuar con cautela y gracia."},
    "Tochtli": {"estado": "Favorable", "desc": "Abundancia, fertilidad y distracción. Cuidado con los excesos."},
    "Atl": {"estado": "Desfavorable", "desc": "Inestabilidad emocional, conflicto y purificación a través del llanto."},
    "Itzcuintli": {"estado": "Favorable", "desc": "Fidelidad, guía espiritual y compañerismo. Gran día para alianzas."},
    "Ozomatli": {"estado": "Favorable", "desc": "Alegría, celebración y artes. Evita caer en la superficialidad o burla."},
    "Malinalli": {"estado": "Desfavorable", "desc": "Tenacidad ante la adversidad. Día de renovación costosa; el esfuerzo será doble."},
    "Acatl": {"estado": "Neutro", "desc": "Conexión con lo divino, rectitud. Atrae flechas de fortuna o de conflicto."},
    "Ocelotl": {"estado": "Desfavorable", "desc": "Poder, guerra y fuerza indomable. Peligro de actuar con soberbia o violencia."},
    "Cuauhtli": {"estado": "Favorable", "desc": "Visión clara, valentía y altura espiritual. Día para tomar decisiones importantes."},
    "Cozcaquauhtli": {"estado": "Favorable", "desc": "Larga vida, sabiduría analítica y limpieza de situaciones difíciles."},
    "Ollin": {"estado": "Neutro", "desc": "Movimiento, terremotos internos y cambio. Exige adaptabilidad inmediata."},
    "Tecpatl": {"estado": "Desfavorable", "desc": "Juicio duro, cortes drásticos y verdades dolorosas. Día de sacrificios."},
    "Quiahuitl": {"estado": "Desfavorable", "desc": "Tormentas emocionales y crisis. No es buen momento para viajar."},
    "Xochitl": {"estado": "Favorable", "desc": "Belleza, florecimiento espiritual, amor y creatividad. Máxima energía positiva."}
}

NUMERALES_PRONOSTICO = {
    1: {"influencia": "Fuerte", "efecto": "Energía primordial y pura. Potencia el signo al máximo."},
    2: {"influencia": "Débil", "efecto": "Dualidad y balance, pero baja intensidad física."},
    3: {"influencia": "Fuerte", "efecto": "Aumento de la productividad y dinamismo."},
    4: {"influencia": "Fuerte", "efecto": "Estabilidad, base sólida y equilibrio en la tierra."},
    5: {"influencia": "Desfavorable", "efecto": "Inestabilidad, desorden y peligro de distribución."},
    6: {"influencia": "Débil", "efecto": "Disminución de las fuerzas; propenso a la apatía."},
    7: {"influencia": "Favorable", "efecto": "Número místico y afortunado. Trae claridad mental."},
    8: {"influencia": "Fuerte", "efecto": "Fuerza de realización y firmeza en las decisiones."},
    9: {"influencia": "Desfavorable", "efecto": "Fuerzas nocturnas, misterio y peligro de engaños."},
    10: {"influencia": "Favorable", "efecto": "Abundancia y ordenamiento del destino."},
    11: {"influencia": "Neutro", "efecto": "Transición, cambios imprevistos en el rumbo del día."},
    12: {"influencia": "Fuerte", "efecto": "Gran acumulación de conocimiento y madurez."},
    13: {"influencia": "Favorable", "efecto": "Culminación, conexión espiritual y trascendencia extrema."}
}

# --- DICCIONARIO DE DEIDADES REGENTES ---
REGENTES_SIGNOS = {
    "Cipactli": {"dios": "Tonacatecuhtli", "desc": "Dios de la subsistencia y la creación primaria"},
    "Ehecatl": {"dios": "Quetzalcoatl", "desc": "Dios del viento, el aliento vital y la sabiduría"},
    "Calli": {"dios": "Tepeyollotl", "desc": "Corazón del monte, el jaguar protector de la tierra"},
    "Cuetzpalli": {"dios": "Huehuecoyotl", "desc": "Coyote viejo, dios de la danza, el juego y la astucia"},
    "Coatl": {"dios": "Chalchiuhtlicue", "desc": "La de la falda de jade, diosa del agua dulce y los ríos"},
    "Miquiztli": {"dios": "Tecciztecatl", "desc": "El del caracol de caracola, dios ancestro de la Luna"},
    "Mazatl": {"dios": "Tlaloc", "desc": "Dios de la lluvia, el rayo y la fertilidad de la tierra"},
    "Tochtli": {"dios": "Mayahuel", "desc": "Diosa del maguey, los ciclos de la vida y la embriaguez mística"},
    "Atl": {"dios": "Xiuhtecuhtli", "desc": "Dios del fuego primordial y el señor del tiempo cósmico"},
    "Itzcuintli": {"dios": "Mictlantecuhtli", "desc": "Dios del inframundo y soberano del reino de los muertos"},
    "Ozomatli": {"dios": "Xochipilli", "desc": "Príncipe de las flores, dios del arte, la danza y el juego"},
    "Malinalli": {"dios": "Patecatl", "desc": "Dios de la medicina, las plantas curativas y del pulque"},
    "Acatl": {"dios": "Tezcatlipoca", "desc": "Espejo humeante, señor de la noche, la memoria y el destino"},
    "Ocelotl": {"dios": "Tlazolteotl", "desc": "Diosa de la tierra, los ciclos lunares y la purificación"},
    "Cuauhtli": {"dios": "Xipe Totec", "desc": "Nuestro señor desollado, dios de la renovación y la vegetación"},
    "Cozcaquauhtli": {"dios": "Itzpapalotl", "desc": "Mariposa de obsidiana, deidad guerrera de las estrellas"},
    "Ollin": {"dios": "Xolotl", "desc": "El gemelo celeste, dios del relámpago y guía del ocaso nocturno"},
    "Tecpatl": {"dios": "Chalchiuhtotolin", "desc": "El pavo precioso, manifestación nocturna de Tezcatlipoca"},
    "Quiahuitl": {"dios": "Tonatiuh", "desc": "El Sol radiante, señor del día y del ciclo luminoso"},
    "Xochitl": {"dios": "Xochiquetzal", "desc": "Flor preciosa, diosa del amor, los tejidos y la belleza creativa"}
}

# --- LÓGICA DE TU ALGORITMO ---
def es_bisiesto_juliano(año):
    return año % 4 == 0

def dias_hasta_mes(mes, año):
    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if es_bisiesto_juliano(año):
        dias_por_mes[2] = 29
    dias_acumulados = 0
    for i in range(1, mes):
        dias_acumulados += dias_por_mes[i]
    return dias_acumulados

def numero_juliano_corregido(fecha):
    año, mes, dia = fecha.year, fecha.month, fecha.day
    años_anteriores = año - 1
    dias = años_anteriores * 365 + años_anteriores // 4
    dias += dias_hasta_mes(mes, año)
    dias += dia
    return dias

def ajuste_gregoriano(fecha):
    if fecha < datetime(1582, 10, 15): return 0
    elif fecha < datetime(1700, 3, 1): return 10
    elif fecha < datetime(1800, 3, 1): return 11
    elif fecha < datetime(1900, 3, 1): return 12
    elif fecha < datetime(2100, 3, 1): return 13
    else: return 13

def cifra_tonalpohualli(numero_base):
    cifra = (numero_base + 61) % 260
    return cifra if cifra != 0 else 260

def tonalpohualli_completo(fecha, calendario='juliano'):
    if calendario == 'juliano':
        nj = numero_juliano_corregido(fecha)
    else:
        nj = numero_juliano_corregido(fecha) - ajuste_gregoriano(fecha)
    
    cifra = cifra_tonalpohualli(nj) 
    numero = (cifra - 1) % 13 + 1
    indice_signo = (cifra - 1) % 20
    
    return numero, signos_Nah[indice_signo], f"{numero}-{signos_Esp[indice_signo]} / {numeros_Nah[numero-1]}-{signos_Nah[indice_signo]}"

def año_tolteca(numero_base):
    total = numero_base + 309
    años = total // 365
    residuo = total % 365
    año_t = años if residuo == 0 else años + 1
    marcador = año_t % 52
    marcador = 52 if marcador == 0 else marcador
    return f"{numeros_Nah[marcador % 13]}-{año_Nah[(marcador % 4)-1]} / {(marcador % 13) + 1}-{año_Esp[(marcador % 4)-1]}", año_t

# --- MOTOR DE PRONÓSTICOS ---
def generar_pronostico(numeral, signo):
    info_signo = SIGNOS_PRONOSTICO.get(signo)
    info_numeral = NUMERALES_PRONOSTICO.get(numeral)
    
    if info_signo["estado"] == "Favorable":
        if info_numeral["influencia"] in ["Favorable", "Fuerte"]:
            return "🌟 DÍA EXCELENTE (Cualli Tonalli)", "Las energías están perfectly alineadas a tu favor. Actúa sin titubear.", "success"
        elif info_numeral["influencia"] == "Desfavorable":
            return "⚠️ DÍA NEUTRO CON OBSTÁCULOS", "El signo es bueno, pero el número exige prudencia ante malas vibras.", "warning"
        else:
            return "🙂 DÍA BUENO", "Aprovecha la naturaleza constructiva y positiva del signo de hoy.", "success"
    elif info_signo["estado"] == "Desfavorable":
        if info_numeral["influencia"] == "Desfavorable":
            return "🛑 DÍA ADVERSO (Amo Cualli)", "Día de resguardo. Evita discusiones, firmas importantes o riesgos.", "error"
        elif info_numeral["influencia"] in ["Favorable", "Fuerte"]:
            return "⚡ DÍA DE DESAFÍO", "La gran fuerza del número te dará la energía para superar la hostilidad del signo.", "warning"
        else:
            return "📉 DÍA CUIDADOSO", "Mantén un perfil bajo, sé paciente y fluye con el día sin forzar las cosas.", "warning"
    else:
        if info_numeral["influencia"] in ["Favorable", "Fuerte"]:
            return "🙂 DÍA PRODUCTIVO", "La fuerza del número inclina la balanza del signo neutro hacia el éxito.", "success"
        elif info_numeral["influencia"] == "Desfavorable":
            return "⚠️ DÍA COMPLICADO", "La falta de rumbo del signo neutro se junta con una energía numérica pesada.", "warning"
        else:
            return "☯️ DÍA NEUTRO", "Día de equilibrio estricto. Momento ideal para la introspección.", "info"

# --- INTERFAZ GRÁFICA (STREAMLIT) ---

st.title("🌞 Cronología Mexica & Tonalpohualli")
st.write("Selecciona cualquier fecha para calcular su signo y conocer su destino cósmico.")

# 1. Forzar la zona horaria local para evitar el desfase con el servidor UTC
from zoneinfo import ZoneInfo
zona_local = ZoneInfo("America/Mexico_City") # Ajusta a tu zona si es diferente
fecha_hoy_local = datetime.now(zona_local).date()

# Selector de fecha interactivo con rango extendido (Año 1000 al 2300)
fecha_seleccionada = st.date_input(
    label="Selecciona una fecha para consultar:",
    value=fecha_hoy_local,  # Ahora sí, usará siempre TU fecha de hoy
    min_value=datetime(1000, 1, 1).date(),  
    max_value=datetime(2300, 12, 31).date() 
)
fecha = datetime.combine(fecha_seleccionada, datetime.min.time())

if fecha < datetime(1582, 10, 15):
    st.info(f"📅 Analizando fecha bajo el **Calendario Juliano**")
    num_tonal, signo_tonal, tonal_str = tonalpohualli_completo(fecha, 'juliano')   
    xiuh_str, tolteca_num = año_tolteca(numero_juliano_corregido(fecha))   
else:
    st.info(f"📅 Analizando fecha bajo el **Calendario Gregoriano**")
    num_tonal, signo_tonal, tonal_str = tonalpohualli_completo(fecha, 'gregoriano')
    xiuh_str, tolteca_num = año_tolteca(numero_juliano_corregido(fecha) - ajuste_gregoriano(fecha))

st.markdown("---")

# 2. Despliegue Visual de los Glifos (Convertidos a minúsculas para coincidir con tus archivos)
st.subheader("Signo del Día")

# Se añade .lower() para buscar 'cipactli.png' en vez de 'Cipactli.png'
ruta_numero = f"assets/numbers/{num_tonal}.png"
ruta_signo = f"assets/days/{signo_tonal.lower()}.png"

col_num, col_sig = st.columns(2)

with col_num:
    st.markdown(f"<h3 style='text-align: center;'>Numeral: {num_tonal} ({numeros_Nah[num_tonal-1]})</h3>", unsafe_allow_html=True)
    if os.path.exists(ruta_numero):
        img_num = Image.open(ruta_numero)
        st.image(img_num, use_container_width=True)
    else:
        st.warning(f"No se encontró el archivo: {ruta_numero}")

with col_sig:
    st.markdown(f"<h3 style='text-align: center;'>Signo: {signo_tonal} ({tonal_str.split(' - ')[0].split('-')[1]})</h3>", unsafe_allow_html=True)
    if os.path.exists(ruta_signo):
        img_sig = Image.open(ruta_signo)
        st.image(img_sig, use_container_width=True)
    else:
        st.warning(f"No se encontró el archivo (intentado en minúsculas): {ruta_signo}")

st.markdown("---")

# 3. Métricas del Año (Xiuhpohualli)
st.metric(label="Xiuhpohualli (Año Tolteca)", value=f"Año {tolteca_num}", delta=xiuh_str)

st.markdown("---")

# 4. Bloque de Pronóstico
veredicto, consejo, tipo_alerta = generar_pronostico(num_tonal, signo_tonal)

st.subheader("🔮 Pronóstico del Destino")

if tipo_alerta == "success":
    st.success(f"**{veredicto}**")
elif tipo_alerta == "warning":
    st.warning(f"**{veredicto}**")
elif tipo_alerta == "error":
    st.error(f"**{veredicto}**")
else:
    st.info(f"**{veredicto}**")

st.write(f"• **Signo ({signo_tonal}):** {SIGNOS_PRONOSTICO[signo_tonal]['desc']}")
st.write(f"• **Numeral ({num_tonal}):** {NUMERALES_PRONOSTICO[num_tonal]['efecto']}")
st.info(f"👉 **Consejo del día:** {consejo}")

st.markdown("---")

# --- 5. SECCIÓN: DEIDAD REGENTE DEL SIGNO (También protegida en minúsculas) ---
st.subheader("🏛️ Deidad Patrona del Signo")

datos_regente = REGENTES_SIGNOS.get(signo_tonal, {"dios": "Desconocido", "desc": "Sin descripción"})
nombre_dios = datos_regente["dios"]
desc_dios = datos_regente["desc"]

# Se añade .lower() por si guardas los dioses en minúsculas (ej: 'quetzalcoatl.png')
ruta_dios = f"assets/gods/{nombre_dios.lower()}.png"

col_img_dios, col_txt_dios = st.columns([1, 2])

with col_img_dios:
    if os.path.exists(ruta_dios):
        img_dios = Image.open(ruta_dios)
        st.image(img_dios, use_container_width=True)
    else:
        st.caption(f"📷 *(Esperando imagen en: {ruta_dios})*")

with col_txt_dios:
    st.markdown(f"El signo **{signo_tonal}** se encuentra bajo la tutela cósmica de:")
    st.info(f"🏛️ **{nombre_dios}**\n\n*{desc_dios}*")

# --- 6. SECCIÓN: CONTEXTO LUNAR ---
st.markdown("---")
st.subheader("🌙 Contexto Astronómico: La Cuenta Lunar (Metztlapohualli)")
st.markdown("""
El día que has consultado forma parte de un engranaje cósmico mucho mayor estructurado por el *Tonalpohualli* (260 días), el *Metztlapohualli* (Ciclo Lunar) y el *Xiuhpohualli* (365 días). Cuando estos ciclos se sincronizaban por completo cada 52 años, se realizaba la trascendental ceremonia del *Xiuhmolpilli* o el **Fuego Nuevo**.
""")

st.link_button(
    label="Leer más sobre el Calendario Lunar en Pueblos Originarios",
    url="https://pueblosoriginarios.com/meso/valle/azteca/calendarios/calendario_lunar.html"
)