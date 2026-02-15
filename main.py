import eel
from backend.services.pdf_union import unir_pdfs
from pathlib import Path
import base64

eel.init('frontend')

@eel.expose
def subir_pdf(data_b64, nombre_archivo):
    ruta = Path("data/temp") / nombre_archivo
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "wb") as f:
        f.write(base64.b64decode(data_b64))
    return str(ruta.resolve())

@eel.expose
def unir(lista_rutas, ruta_salida):
    if not lista_rutas or len(lista_rutas) < 2:
        return {"senal": False, "mensaje": "Se necesitan al menos 2 PDFs"}
    return unir_pdfs(lista_rutas, ruta_salida)

eel.start("conversor.html", size=(1000, 600))
