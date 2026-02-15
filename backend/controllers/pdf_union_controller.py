from PyPDF2 import PdfMerger
from pathlib import Path
from backend.utils.logger_configuracion import setup_logger
from backend.utils.rutas_validaciones import validar_rutas

def unir_pdfs(rutas_pdf, salida_pdf):
    log = setup_logger()
    objUnidor = PdfMerger()
    senal = False
    mensaje = ""

    validador = validar_rutas(rutas_pdf, '.pdf')

    if not validador:
        log.warning("No se encontraron PDFs")
        return {'senal': senal, 'mensaje': "No se encontraron PDFs"}

    for pdf in validador:
        try:
            objUnidor.append(pdf)
            log.info(f'PDF agregado correctamente: {pdf}')
        except Exception as e:
            log.error(f'Error: {e}')
            return {'senal': senal, 'mensaje': f'Error: {e}'}

    salida_pdf = Path(salida_pdf)
    salida_pdf.parent.mkdir(parents=True, exist_ok=True)

    try:
        objUnidor.write(str(salida_pdf))
        objUnidor.close()
        log.info(f'PDF unidos correctamente: {salida_pdf}')
        senal = True
        mensaje = f"PDF unido correctamente: {salida_pdf}"
        return {'senal': senal, 'mensaje': mensaje}
    except Exception as e:
        log.error(f'Error: {e}')
        return {'senal': senal, 'mensaje': f"Error: {e}"}
