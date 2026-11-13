from datetime import datetime
import sys

# ==========================================
# IMPORTACIÓN DE DATOS EXTERNOS
# ==========================================
try:
    from data_signos import DATOS_CALENDARIO
except ImportError:
    print("ERROR: No se encontró 'data_signos.py'.")
    print("Asegúrate de que el archivo esté en la misma carpeta.")
    sys.exit(1)

# ==========================================
# CONFIGURACIÓN Y CONSTANTES MAESTRAS
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

# Diccionarios de Pronóstico Simplificados (Fallback si data_signos falla o falta)
PRONOSTICO_SIGNOS_FALLBACK = {
    "Cipactli": {"estado": "Favorable", "desc": "Inicio, abundancia y energía vital."},
    "Ehecatl": {"estado": "Desfavorable", "desc": "Inconstancia y vientos de cambio drásticos."},
    "Calli": {"estado": "Neutro", "desc": "Reflexión e interiorización."},
    "Cuetzpalin": {"estado": "Favorable", "desc": "Salud, agilidad y autorreparación."},
    "Coatl": {"estado": "Favorable", "desc": "Sabiduría, fuerza mística y renovación."},
    "Miquiztli": {"estado": "Neutro", "desc": "Transformación y memoria ancestral."},
    "Mazatl": {"estado": "Favorable", "desc": "Intuición y timidez cautelosa."},
    "Tochtli": {"estado": "Favorable", "desc": "Abundancia, fertilidad y distracción."},
    "Atl": {"estado": "Desfavorable", "desc": "Inestabilidad emocional y conflicto."},
    "Itzcuintli": {"estado": "Favorable", "desc": "Fidelidad, guía espiritual y alianzas."},
    "Ozomahtli": {"estado": "Favorable", "desc": "Alegría, celebración y artes."},
    "Malinalli": {"estado": "Desfavorable", "desc": "Tenacidad ante la adversidad costosa."},
    "Acatl": {"estado": "Neutro", "desc": "Conexión divina y rectitud."},
    "Ocelotl": {"estado": "Desfavorable", "desc": "Poder indomable y riesgo de soberbia."},
    "Cuauhtli": {"estado": "Favorable", "desc": "Visión clara y valentía espiritual."},
    "Cozcacuauhtli": {"estado": "Favorable", "desc": "Larga vida y limpieza de situaciones."},
    "Ollin": {"estado": "Neutro", "desc": "Movimiento, cambio y adaptabilidad."},
    "Tecpatl": {"estado": "Desfavorable", "desc": "Juicio duro y cortes drásticos."},
    "Quiahuitl": {"estado": "Desfavorable", "desc": "Tormentas emocionales y crisis."},
    "Xochitl": {"estado": "Favorable", "desc": "Belleza, florecimiento y creatividad."}
}

PRONOSTICO_NUMERALES = {
    1: {"influencia": "Fuerte", "efecto": "Energía primordial pura."},
    2: {"influencia": "Débil", "efecto": "Dualidad y balance bajo."},
    3: {"influencia": "Fuerte", "efecto": "Productividad y dinamismo."},
    4: {"influencia": "Fuerte", "efecto": "Estabilidad y base sólida."},
    5: {"influencia": "Desfavorable", "efecto": "Inestabilidad y dispersión."},
    6: {"influencia": "Débil", "efecto": "Disminución de fuerzas."},
    7: {"influencia": "Favorable", "efecto": "Claridad mental y suerte."},
    8: {"influencia": "Fuerte", "efecto": "Realización firme."},
    9: {"influencia": "Desfavorable", "efecto": "Misterio nocturno y engaños."},
    10: {"influencia": "Favorable", "efecto": "Abundancia ordenada."},
    11: {"influencia": "Neutro", "efecto": "Transición imprevista."},
    12: {"influencia": "Fuerte", "efecto": "Madurez acumulativa."},
    13: {"influencia": "Favorable", "efecto": "Culminación trascendente."}
}

# Lista de Señores de Trecena (Basado en códices tradicionales y Piña Garza)
SEÑORES_TRECENA = [
    "Tonacatecuhtli",   # 1 Cipactli
    "Tepeyollotl",      # 14 Ocelotl
    "Tlaloc",           # 7 Mazatl
    "Xiuhtecuhtli",     # 20 Xochitl
    "Quetzalcoatl",     # 13 Acatl
    "Mictlantecuhtli",  # 6 Miquiztli
    "Chalchiuhtlicue",  # 19 Quiahuitl
    "Mayahuel",         # 12 Malinalli
    "Xochiquetzal",     # 5 Coatl
    "Xolotl",           # 18 Tecpatl
    "Itzpapalotl",      # 11 Ozomahtli
    "Huehuecoyotl",     # 4 Cuetzpalin
    "Mixcoatl",         # 17 Ollin
    "Xipe Totec",       # 10 Itzcuintli
    "Camaxtli",         # 3 Calli
    "Cozcaquauhtli",    # 16 Cozcacuauhtli
    "Tlazolteotl",      # 9 Atl
    "Ehecatl-Quetzalcoatl", # 2 Ehecatl
    "Cuauhtli",         # 15 Cuauhtli
    "Tochtli-Mayahuel"  # 8 Tochtli (Variantes según fuente)
]

# ==========================================
# FUNCIONES DE CÁLCULO CORE (Robustas)
# ==========================================

def pedir_fecha():
    while True:
        try:
            fecha_str = input("Ingrese fecha (DD/MM/AAAA): ")
            return datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            print("Formato inválido. Use DD/MM/AAAA")

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
    """Calcula días desde 1 Jan Año 1 (Juliano proléptico)"""
    año, mes, dia = fecha.year, fecha.month, fecha.day
    años_anteriores = año - 1
    dias = años_anteriores * 365 + (años_anteriores // 4)
    dias += dias_hasta_mes(mes, año)
    dias += dia
    return dias

def ajuste_gregoriano(fecha):
    if fecha < datetime(1582, 10, 15):
        return 0
    elif fecha < datetime(1700, 3, 1):
        return 10
    elif fecha < datetime(1800, 3, 1):
        return 11
    elif fecha < datetime(1900, 3, 1):
        return 12
    elif fecha < datetime(2100, 3, 1):
        return 13
    else:
        return 14 # Simplificado para >2100

def obtener_tonalpohualli(fecha):
    nj = numero_juliano_corregido(fecha)
    
    if fecha >= datetime(1582, 10, 15):
        nj = nj - ajuste_gregoriano(fecha)
        
    cifra = (nj + ANCLA_TONALPOHUALLI) % 260
    if cifra == 0:
        idx_ciclo = 259 
    else:
        idx_ciclo = cifra - 1
        
    numero = (idx_ciclo % 13) + 1
    indice_signo = idx_ciclo % 20
    
    signo_nah = SIGNOS_Nah[indice_signo]
    signo_esp = SIGNOS_Esp[indice_signo]
    num_nah = NUMEROS_Nah[numero - 1]
    
    return numero, signo_nah, signo_esp, num_nah, idx_ciclo

def calcular_trecena(idx_ciclo):
    """
    Calcula qué trecena (1-20) contiene este día.
    Método directo basado en bloques de 13 días dentro del ciclo de 260.
    """
    trecena_num = (idx_ciclo // 13) + 1
    return trecena_num

def calcular_xiuhpohualli(fecha):
    nj = numero_juliano_corregido(fecha)
    if fecha >= datetime(1582, 10, 15):
        nj = nj - ajuste_gregoriano(fecha)
        
    total_dias = nj + 309
    años_totales = total_dias // 365
    
    marcador_absoluto = años_totales % 52
    if marcador_absoluto == 0:
        marcador_absoluto = 52
        
    num_marcador = marcador_absoluto % 13
    if num_marcador == 0:
        num_marcador = 13
        
    beta_idx = marcador_absoluto % 4
    if beta_idx == 0:
        beta_idx = 4
        
    portador_name = PORTADORES_AÑO_NAH[beta_idx - 1]
    portador_esp = PORTADORES_AÑO_ESP[beta_idx - 1]
    
    return f"{num_marcador}-{portador_name}", f"{num_marcador}-{portador_esp}"

def tonal_opuesto(indice_signo_actual):
    """Avanza 10 posiciones en la rueda de 20 signos"""
    indice_opuesto = (indice_signo_actual + 10) % 20
    return SIGNOS_Nah[indice_opuesto], SIGNOS_Esp[indice_opuesto]

def generar_veredicto(numeral, signo_nah):
    info_s = PRONOSTICO_SIGNOS_FALLBACK.get(signo_nah, {"estado": "Neutro", "desc": "Sin datos"})
    info_n = PRONOSTICO_NUMERALES.get(numeral, {"influencia": "Neutro", "efecto": "Sin datos"})
    
    estado_s = info_s["estado"]
    inf_n = info_n["influencia"]
    
    veredicto = ""
    consejo = ""
    
    if estado_s == "Favorable":
        if inf_n in ["Favorable", "Fuerte"]:
            veredicto = "🌟 DÍA EXCELENTE (Cualli Tonalli)"
            consejo = "Las energías están perfectamente alineadas a tu favor. Actúa sin titubear."
        elif inf_n == "Desfavorable":
            veredicto = "⚠️ NEUTRO CON OBSTÁCULOS"
            consejo = "El signo es inherentemente bueno, pero el número exige prudencia ante malas vibras."
        else:
            veredicto = "🙂 DÍA BUENO"
            consejo = "Aprovecha la naturaleza constructiva y positiva del signo de hoy."
            
    elif estado_s == "Desfavorable":
        if inf_n == "Desfavorable":
            veredicto = "🛑 DÍA ADVERSO (Amo Cualli)"
            consejo = "Día de resguardo. Evita discusiones, firmas importantes o riesgos innecesarios."
        elif inf_n in ["Favorable", "Fuerte"]:
            veredicto = "⚡ DÍA DE DESAFÍO"
            consejo = "La gran fuerza del número te dará la energía necesaria para superar la hostilidad del signo."
        else:
            veredicto = "📉 DÍA CUIDADOSO"
            consejo = "Mantén un perfil bajo, sé paciente y fluye con el día sin forzar las cosas."
            
    else: # Neutro
        if inf_n in ["Favorable", "Fuerte"]:
            veredicto = "🙂 DÍA PRODUCTIVO"
            consejo = "La fuerza del número inclina la balanza del signo neutro hacia el éxito."
        elif inf_n == "Desfavorable":
            veredicto = "⚠️ DÍA COMPLICADO"
            consejo = "La falta de rumbo del signo neutro se junta con una energía numérica pesada."
        else:
            veredicto = "☯️ DÍA NEUTRO"
            consejo = "Día de equilibrio estricto. Momento ideal para la introspección y planeación."
            
    return veredicto, consejo

# ==========================================
# PRESENTADOR DE RESULTADOS (REPORTES)
# ==========================================

def imprimir_reporte_completo(fecha):
    # 1. Cálculos Base
    numero, signo_nah, signo_esp, num_nah, idx_ciclo = obtener_tonalpohualli(fecha)
    xiuh_nah, xiuh_esp = calcular_xiuhpohualli(fecha)
    trecena_num = calcular_trecena(idx_ciclo)
    
    # 2. Cálculo del NAHUALI (Opuesto)
    sign_op_nah, sign_op_esp = tonal_opuesto(idx_ciclo % 20)
    
    # 3. Obtener Datos de data_signos.py
    # Normalizamos claves para buscar en DATOS_CALENDARIO (quitando espacios si existen)
    key_busqueda = signo_nah.strip()
    datos_tonal = DATOS_CALENDARIO.get(key_busqueda, {})
    
    key_opuesto = sign_op_nah.strip()
    datos_nahualli = DATOS_CALENDARIO.get(key_opuesto, {})
    
    # Señor de la Trecena
    senor_trecena = SEÑORES_TRECENA[trecena_num - 1] if trecena_num <= len(SEÑORES_TRECENA) else "Desconocido"

    # 4. Pronóstico
    veredicto, consejo = generar_veredicto(numero, signo_nah)
    
    # 5. Formato de Salida
    print("\n" + "="*60)
    print(f"{' REPORTE CALENDÁRICO MEXICA v12 ':^60}")
    print("="*60)
    print(f" Fecha Analizada: {fecha.strftime('%d/%m/%Y')}")
    print("-"*60)
    
    # SECCIÓN 1: IDENTIDAD DEL TONAL (NACIMIENTO)
    print("\n🔮 TU TONAL (DÍA DE NACIMIENTO)")
    print(f"   • Combinación:       {numero} {signo_nah} ({signo_esp})")
    print(f"   • Nombre Náhuatl:    {num_nah} {signo_nah}")
    print(f"   • Posición Ciclo:    {idx_ciclo + 1}/260")
    print(f"   • Trecena:           #{trecena_num}")
    print(f"   • Señor de Trecena:  {senor_trecena}")
    
    if datos_tonal:
        dios_tonal = datos_tonal.get('dios', 'N/A')
        desc_dios_tonal = datos_tonal.get('dios_desc', 'Descripción de la deidad no disponible.')
        desc_signo_tonal = datos_tonal.get('signo_desc', 'Descripción general.')
        elemento = datos_tonal.get('elemento', 'N/A')
        rumbo = datos_tonal.get('rumbo', 'N/A')
        
        print(f"   • Deidad Patrona:    👹 {dios_tonal}")
        print(f"     └─ Descripción:    {desc_dios_tonal}")
        print(f"   • Significado:       {desc_signo_tonal}")
        print(f"   • Elemento/Rumbo:    {elemento} / {rumbo}")
    else:
        print("   ⚠️ Nota: Datos detallados no encontrados en data_signos.py para este signo.")

    # SECCIÓN 2: EL NAHUALI (OPUESTO/COMPLEMENTARIO)
    print("\n🐍 TU NAHUALI (SIGNO OPUESTO)")
    print(f"   • Definición:        Energía complementaria/espejo")
    print(f"   • Cálculo:           Avance de 10 posiciones en la rueda")
    print(f"   • Combinación:       {numero} {sign_op_nah} ({sign_op_esp})")
    
    if datos_nahualli:
        dios_nahualli = datos_nahualli.get('dios', 'N/A')
        desc_dios_nahualli = datos_nahualli.get('dios_desc', 'Descripción de la deidad no disponible.')
        desc_signo_nahualli = datos_nahualli.get('signo_desc', 'Energía complementaria.')
        
        print(f"   • Deidad Asociada:   🦅 {dios_nahualli}")
        print(f"     └─ Descripción:    {desc_dios_nahualli}")
        print(f"   • Interpretación:    {desc_signo_nahualli}")
    else:
        print(f"   • Interpretación:    Energía opuesta al signo de nacimiento.")

    # SECCIÓN 3: CONTEXTO SOLAR
    print("\n☀️ CONTEXTO SOLAR (XIUHPOLHALLI)")
    print(f"   • Año Tolteca:         {xiuh_esp} ({xiuh_nah})")
    
    # SECCIÓN 4: INTERPRETACIÓN DEL DESTINO
    print("\n📜 PRONÓSTICO SIMBÓLICO (DEL TONAL)")
    print(f"   Veredicto:             {veredicto}")
    print(f"   Consejo Práctico:      {consejo}")
    
    print("\n" + "="*60)
    print(" Nota: El 'Nahualli' aquí mostrado corresponde al signo opuesto")
    print(" (complementario) según la metodología definida por el usuario.")
    print(" Fuentes: Piña Garza (Aritmética), Tena (Ortografía), Guía PDF (+61).")
    print("="*60 + "\n")

# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    fecha_usuario = pedir_fecha()
    imprimir_reporte_completo(fecha_usuario)