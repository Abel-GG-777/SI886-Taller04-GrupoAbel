# 02_identidad/MV01_diagnostico_declaraciones.py
"""Diagnóstico técnico de la misión y la visión publicadas por una empresa.

Aplica los instrumentos de la teoría de la Semana 04 — los cinco componentes,
los siete defectos, las tres pruebas de calidad y los cinco atributos de la
visión— y emite el veredicto. El programa detecta lo que se puede leer en el
texto; el juicio que exige evidencia lo pone el equipo, y lo sustenta.
"""
import re
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# LO QUE EL EQUIPO EDITA. Datos reales de Bitel (Viettel Perú S.A.C.)
# ---------------------------------------------------------------------------
EMPRESA = "Viettel Perú S.A.C. (Bitel)"
COMPETIDORES = ["América Móvil Perú S.A.C. (Claro)",
                "Telefónica del Perú S.A.A. (Movistar)",
                "Entel Perú S.A."]

# Misión oficial traducida (Paso A)
MISION = ("Bitel siempre intenta ser creativo y transformarse a sí mismo para "
          "contribuir a mejorar la calidad de vida de los peruanos y de la sociedad. "
          "Asimismo, Bitel continúa innovando junto con los clientes para crear "
          "productos y servicios que hagan la vida y el trabajo fáciles.")

# Visión oficial traducida (Paso A)
VISION = ("Bitel es pionero en el despliegue de tecnología 4.0 y en la creación de "
          "plataformas digitales para cada persona; la organización en su conjunto "
          "contribuye y crea nuevos valores para el desarrollo del país y de los peruanos.")

FUENTE = {
    "Dirección de la página": "https://bitel.com.pe",
    "Fecha de consulta": "10 de septiembre de 2026",
    "¿Publica visión?": "Sí, en la sección institucional de historia",
    "Prueba de la decisión": "Insuficiente para la toma de decisiones. El texto es genérico.",
}

# Los cinco componentes mapeados directamente del texto literal de Bitel
COMPONENTES = {
    "Qué hacemos":        "crear productos y servicios",
    "Para quién":         "de los peruanos y de la sociedad junto con los clientes",
    "Cómo nos distingue": "intenta ser creativo y transformarse a sí mismo continúa innovando",
    "Para qué":           "contribuir a mejorar la calidad de vida que hagan la vida y el trabajo fáciles",
    "Con qué compromiso": None, # Ausente en la declaración de Bitel
}

# Los tres defectos analizados basados en las pruebas empíricas del taller
JUICIO_MISION = {
    "Intercambiable":
        (True, "Sobrevive plenamente a la sustitución por Claro, Movistar o Entel sin perder coherencia"),
    "Contradice la práctica":
        (False, "Las acciones de despliegue de infraestructura comercial concuerdan con dar cobertura"),
    "Escrita por una sola persona":
        (False, "Forma parte del lineamiento corporativo global de Viettel Group"),
}

# Evaluación técnica de los atributos cualitativos de la visión
JUICIO_VISION = {
    "Ambiciosa pero alcanzable":
        (True, "Es alcanzable debido a su alta participación de mercado y red de fibra óptica"),
    "Específica del negocio":
        (True, "Establece el rubro mediante los conceptos de tecnología 4.0 y plataformas digitales"),
    "Movilizadora":
        (False, "No instruye un cambio en la conducta del personal ante la ausencia de un vector de meta claro"),
}

# ---------------------------------------------------------------------------
# LO QUE EL PROGRAMA DETECTA EN EL TEXTO
# ---------------------------------------------------------------------------
ASPIRACIONAL = re.compile(r"\b(ser|seremos|convertirnos|liderar|líder\w*|"
                          r"número uno|primera opción|la mejor|pionero\w*)\b", re.I)
VALORES = re.compile(r"\b(honestidad|respeto|integridad|excelencia|compromis\w+|"
                     r"innovación|calidad total|trabajo en equipo|mejora continua|"
                     r"transparencia|responsabilidad|creativo\w*)\b", re.I)
HORIZONTE = re.compile(r"(al\s+(año\s+)?20\d{2}|en\s+20\d{2}|"
                       r"al cierre del horizonte|a\s+\w+\s+años)", re.I)
METRICA = re.compile(r"\d+([.,]\d+)?\s*(%|por ciento|puntos|horas|días|millones|mil|4\.0)", re.I)

pal_mision = len(MISION.split())
pal_vision = len(VISION.split())
presentes = {k: v for k, v in COMPONENTES.items() if v}

print("=" * 74)
print(f"DIAGNÓSTICO DE LAS DECLARACIONES PUBLICADAS · {EMPRESA}")
print("=" * 74)
for k, v in FUENTE.items():
    print(f"  {k:32s} {v}")

# --- Los cinco componentes de la misión ---
print(f"\n=== MISIÓN · {pal_mision} palabras ===")
print(f"«{MISION}»\n")
print("Los cinco componentes")
for comp, cita in COMPONENTES.items():
    marca = "SÍ" if cita else "NO"
    print(f"  [{marca}] {comp:20s} {cita or '— ausente'}")
print(f"  → {len(presentes)} de 5 componentes")

# --- Los siete defectos ---
detectados = {
    "Intercambiable": JUICIO_MISION["Intercambiable"],
    "Confunde misión con visión": (
        bool(ASPIRACIONAL.search(MISION)),
        "Lenguaje de aspiración en el texto — " + ", ".join(sorted(
            {m.group(0).lower() for m in ASPIRACIONAL.finditer(MISION)}))),
    "Enumera valores": (
        len({m.group(0).lower() for m in VALORES.finditer(MISION)}) >= 3,
        "Tres o más términos de valor en el texto"),
    "Omite al destinatario": (
        COMPONENTES["Para quién"] is None,
        "El componente «Para quién» no está en la declaración"),
    "Extensión desmedida": (
        pal_mision > 50, f"{pal_mision} palabras, el límite práctico es 50"),
    "Contradice la práctica": JUICIO_MISION["Contradice la práctica"],
    "Escrita por una sola persona": JUICIO_MISION["Escrita por una sola persona"],
}
print("\nLos siete defectos")
for defecto, (hay, razon) in detectados.items():
    print(f"  [{'X' if hay else ' '}] {defecto:30s} {razon if hay else ''}")
n_defectos = sum(1 for hay, _ in detectados.values() if hay)
print(f"  → {n_defectos} de 7 defectos")

# --- Las tres pruebas de calidad ---
print("\nPrueba de sustitución — se lee cada línea en voz alta")
for comp in COMPETIDORES:
    print(f"  · {comp} — «{MISION[:64]}…»")
sobrevive = JUICIO_MISION["Intercambiable"][0]
print(f"  → {'FALLA' if sobrevive else 'PASA'} la prueba de sustitución")
print(f"Prueba de la decisión  → {FUENTE['Prueba de la decisión']}")
print("Prueba del reconocimiento → se responde si el equipo tiene acceso; si no, se declara no comprobable")

# --- Los cinco atributos de la visión ---
print(f"\n=== VISIÓN · {pal_vision} palabras ===")
print(f"«{VISION}»\n")
hay_horizonte, hay_metrica = bool(HORIZONTE.search(VISION)), bool(METRICA.search(VISION))
atributos = {
    "Temporalmente acotada": (
        hay_horizonte, "Declara el horizonte" if hay_horizonte
        else "Sin horizonte temporal explícito. No se puede medir avance temporal."),
    "Verificable": (
        hay_metrica, "Trae una cifra comprobable (métrica 4.0)" if hay_metrica
        else "Sin cifra cuantitativa de control de mercado."),
    "Ambiciosa pero alcanzable": JUICIO_VISION["Ambiciosa pero alcanzable"],
    "Específica del negocio": JUICIO_VISION["Específica del negocio"],
    "Movilizadora": JUICIO_VISION["Movilizadora"],
}
print("Los cinco atributos")
for atr, (cumple, razon) in atributos.items():
    print(f"  [{'SÍ' if cumple else 'NO'}] {atr:26s} {razon}")
n_atributos = sum(1 for c, _ in atributos.values() if c)
print(f"  → {n_atributos} de 5 atributos")
metricas = [m.group(0) for m in METRICA.finditer(VISION)]
print(f"Métricas implícitas en la visión → {metricas or 'ninguna'}")


# --- Veredicto final ---
def veredicto_mision():
    if sobrevive:
        return ("SE REFORMULA",
                "Falla la prueba de sustitución. Una misión que sirve para un "
                "competidor no define la estrategia de la organización.")
    if len(presentes) <= 3:
        return "SE REFORMULA", f"Solo porta {len(presentes)} de los cinco componentes"
    if len(presentes) == 4 or n_defectos:
        return "SE AJUSTA", "Le falta el componente de Compromiso y arrastra un defecto de generalidad."
    return "SE CONSERVA", "Cinco componentes y las tres pruebas superadas"


def veredicto_vision():
    if n_atributos <= 2:
        return "SE REFORMULA", f"Solo cumple {n_atributos} de los cinco atributos por falta de horizonte medible."
    if n_atributos <= 4:
        return "SE AJUSTA", "Le faltan atributos indispensables (Falta: Horizonte Temporal Acotado)."
    return "SE CONSERVA", "Cumple los cinco atributos"


print("\n" + "=" * 74)
for etiqueta, (v, razon) in [("MISIÓN", veredicto_mision()),
                             ("VISIÓN", veredicto_vision())]:
    print(f"  VEREDICTO DE LA {etiqueta} · {v}")
    print(f"     {razon}")
print("=" * 74)
print("  El equipo evalúa y propone. Cambiar la declaración es decisión de la")
print("  alta dirección de la empresa.")

# --- Generación del gráfico de diagnóstico técnico exigido en los anexos ---
fig, ejes = plt.subplots(1, 2, figsize=(11, 4))
for eje, datos, titulo in [
        (ejes[0], {k: bool(v) for k, v in COMPONENTES.items()},
         "Misión · los cinco componentes"),
        (ejes[1], {k: c for k, (c, _) in atributos.items()},
         "Visión · los cinco atributos")]:
    etiquetas = list(datos)[::-1]
    valores = [1 if datos[e] else 0 for e in etiquetas]
    eje.barh(etiquetas, valores,
             color=["#0F766E" if v else "#B45309" for v in valores])
    eje.set_xlim(0, 1)
    eje.set_xticks([0, 1])
    eje.set_xticklabels(["Ausente", "Presente"])
    eje.set_title(titulo, fontsize=10)
    eje.tick_params(labelsize=8)
fig.suptitle(f"Diagnóstico de las declaraciones vigentes · {EMPRESA}", fontsize=11)
plt.tight_layout()
plt.savefig("docs/evidencias/S04/salidas/MV_diagnostico_declaraciones.png", dpi=140)
print("\n[INFO] Gráfico guardado exitosamente en: docs/evidencias/S04/salidas/MV_diagnostico_declaraciones.png")
