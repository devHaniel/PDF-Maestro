from pathlib import Path
import logging

def validar_rutas(lista_rutas, extension):
    log = logging.getLogger("PDF-maestro")
    salida = []

    for ruta in lista_rutas:
        p = Path(ruta).resolve()
        if not p.exists() or not p.is_file() or p.suffix.lower() != extension:
            log.warning(f"{p} no existe o no es un PDF")
            continue
        salida.append(str(p))

    return salida
