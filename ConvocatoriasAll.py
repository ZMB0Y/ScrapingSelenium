from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Links de convocatorias vigentes
links_vigentes = [
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4043/musicos-tradicionales-mexicanos-2026",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4042/artes-en-lenguas-indigenas-nacionales-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4041/jovenes-creadores-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4037/premios-nacionales-de-dramaturgia-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4036/creadores-escenicos ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4035/fomento-a-proyectos-y-coinversiones-culturales ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4032/pecda-michoacan ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4031/saberes-sobre-la-escena-en-michoacan-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4030/programa-fortalecimiento-agrupaciones-musicales-comunitarias-de-michoacan",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4029/invitacion-clases-en-coros-comunitarios",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4034/fotoseptiembre-festival-internacional-fotografia-mexico-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4028/programa-alas-y-raices-michoacan-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4033/seminario-de-produccion-fotografica-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4026/mexico-en-una-pieza ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4020/pacmyc-2026 ",
    "https://convocatorias.cultura.gob.mx/vigentes/detalle/4012/xvii-concurso-nacional-de-fotografia "
]

# Links de resultados
links_resultados = [
    "https://convocatorias.cultura.gob.mx/resultados/detalle/4040/resultados-de-la-invitacion-para-las-presentaciones-artisticas-2026 ",
    "https://convocatorias.cultura.gob.mx/resultados/detalle/4039/resultados-de-los-laboratorios-ludicos-de-artes-2026 ",
    "https://convocatorias.cultura.gob.mx/resultados/detalle/4038/resultados-de-la-invitacion-para-las-narraciones-orales-2026 "

]

# Links de vencidas
links_vencidas = [
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4027/aiec-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4025/septima-convocatoria-alas-de-lagartija-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4024/septima-convocatoria-las-otras-tintas-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4023/acmpm-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4022/paice-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4019/foremoba-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4018/semilleros-de-paz-plan-michoacan",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4017/profest-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4016/narraciones-orales-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4015/laboratorios-ludicos-de-artes-2026",
    "https://convocatorias.cultura.gob.mx/vencidas/detalle/4014/presentaciones-artisticas-dirigida-a-ninas-ninos-y-o-adolescentes-2026",

]

service = Service("C:/Users/HINOJOSA/PycharmProjects/ScrapingSelenium/chromedriver.exe")
driver = webdriver.Chrome(service=service)

convocatorias_vigentes = []
convocatorias_resultados = []
convocatorias_vencidas = []

# --- Scraping de convocatorias vigentes ---
for url in links_vigentes:
    driver.get(url)
    time.sleep(3)

    estado = driver.find_element(By.CSS_SELECTOR, "p.estados").text if driver.find_elements(By.CSS_SELECTOR, "p.estados") else ""
    titulo = driver.find_element(By.TAG_NAME, "h1").text
    descripcion = " ".join([
        p.text for p in driver.find_elements(By.CSS_SELECTOR, ".card-body p")
        if "estados" not in p.get_attribute("class")
    ])

    fecha_inicio, fecha_cierre, dependencia, pdf_link = "", "", "", ""
    datos = driver.find_elements(By.CSS_SELECTOR, ".datos p")
    for p in datos:
        txt = p.text
        if "Fecha de inicio" in txt:
            fecha_inicio = txt.replace("Fecha de inicio", "").strip()
        elif "Fecha de cierre" in txt:
            fecha_cierre = txt.replace("Fecha de cierre", "").strip()
        elif "Dependencia" in txt:
            dependencia = txt.replace("Dependencia", "").strip()

    pdf_tag = driver.find_elements(By.XPATH, "//a[contains(text(),'Descargar convocatoria')]")
    if pdf_tag:
        pdf_link = pdf_tag[0].get_attribute("href")

    convocatorias_vigentes.append({
        "Título": titulo,
        "Entidad": estado,
        "Descripción": descripcion,
        "Fecha de inicio": fecha_inicio,
        "Fecha de cierre": fecha_cierre,
        "Dependencia": dependencia,
        "PDF": pdf_link,
        "Link": url
    })

# --- Scraping de resultados ---
for url in links_resultados:
    driver.get(url)
    time.sleep(3)

    estado = driver.find_element(By.CSS_SELECTOR, "p.estados").text if driver.find_elements(By.CSS_SELECTOR, "p.estados") else ""
    titulo = driver.find_element(By.TAG_NAME, "h1").text
    descripcion = " ".join([
        p.text for p in driver.find_elements(By.CSS_SELECTOR, ".card-body p")
        if "estados" not in p.get_attribute("class")
    ])

    fecha_publicacion, dependencia, pdf_link, link_convocatoria = "", "", "", ""
    datos = driver.find_elements(By.CSS_SELECTOR, ".datos p")
    for p in datos:
        txt = p.text
        if "Fecha de publicación" in txt:
            fecha_publicacion = txt.replace("Fecha de publicación", "").strip()
        elif "Dependencia" in txt:
            dependencia = txt.replace("Dependencia", "").strip()

    pdf_tag = driver.find_elements(By.XPATH, "//a[contains(text(),'Descargar resultados')]")
    if pdf_tag:
        pdf_link = pdf_tag[0].get_attribute("href")

    rel_tag = driver.find_elements(By.XPATH, "//a[contains(text(),'Ver convocatoria relacionada')]")
    if rel_tag:
        link_convocatoria = rel_tag[0].get_attribute("href")

    convocatorias_resultados.append({
        "Título": titulo,
        "Entidad": estado,
        "Descripción": descripcion,
        "Fecha de publicación": fecha_publicacion,
        "Dependencia": dependencia,
        "PDF Resultados": pdf_link,
        "Convocatoria relacionada": link_convocatoria,
        "Link": url
    })

# --- Scraping de vencidas ---
for url in links_vencidas:
    driver.get(url)
    time.sleep(3)

    estado = driver.find_element(By.CSS_SELECTOR, "p.estados").text if driver.find_elements(By.CSS_SELECTOR, "p.estados") else ""
    titulo = driver.find_element(By.TAG_NAME, "h1").text
    descripcion = " ".join([
        p.text for p in driver.find_elements(By.CSS_SELECTOR, ".card-body p")
        if "estados" not in p.get_attribute("class")
    ])

    fecha_inicio, fecha_cierre, dependencia, categorias, pdf_link = "", "", "", "", ""
    datos = driver.find_elements(By.CSS_SELECTOR, ".datos p")
    for p in datos:
        txt = p.text
        if "Fecha de inicio" in txt:
            fecha_inicio = txt.replace("Fecha de inicio", "").strip()
        elif "Fecha de cierre" in txt:
            fecha_cierre = txt.replace("Fecha de cierre", "").strip()
        elif "Dependencia" in txt:
            dependencia = txt.replace("Dependencia", "").strip()
        elif "Categorías" in txt:
            # capturamos categorías de la lista <ul>
            ul = driver.find_elements(By.CSS_SELECTOR, ".datos ul li a")
            categorias = ", ".join([c.text for c in ul])

    pdf_tag = driver.find_elements(By.XPATH, "//a[contains(text(),'Descargar convocatoria')]")
    if pdf_tag:
        pdf_link = pdf_tag[0].get_attribute("href")

    convocatorias_vencidas.append({
        "Título": titulo,
        "Entidad": estado,
        "Descripción": descripcion,
        "Fecha de inicio": fecha_inicio,
        "Fecha de cierre": fecha_cierre,
        "Dependencia": dependencia,
        "Categorías": categorias,
        "PDF": pdf_link,
        "Link": url
    })

driver.quit()

# --- Exportar a Excel con tres hojas ---
with pd.ExcelWriter("ConvocatoriasCultura.xlsx", engine="openpyxl") as writer:
    pd.DataFrame(convocatorias_vigentes).to_excel(writer, sheet_name="Vigentes", index=False)
    pd.DataFrame(convocatorias_resultados).to_excel(writer, sheet_name="Resultados", index=False)
    pd.DataFrame(convocatorias_vencidas).to_excel(writer, sheet_name="Vencidas", index=False)

print("Scraping completado. Archivo generado: ConvocatoriasCultura.xlsx")
