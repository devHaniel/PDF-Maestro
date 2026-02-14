from PyPDF2 import PdfMerger
from pathlib import Path

from util.logger_configuracion import setup_logger
from util.rutas_validaciones import validar_rutas

def unir_pdfs(rutas_pdf, salida_pdf):

    """

    Args:
        rutas_pdf: Lista de rutas de los archivos pdf.
        salida_pdf: cadena de texto con la salida junto la extesion .pdf

    Returns:
        senal = boolean -> Operacion exitosa o no.\n
        mensaje = indica que paso.
    """

    senal = False
    mensaje = ""

    # Validacion de las rutas
    log = setup_logger()
    objUnidor = PdfMerger()

    validador = validar_rutas(rutas_pdf, '.pdf')

    if not validador:
        log.warning('No se encontraorn pdfs')
        mensaje = "No se encontraen pdfs"
        return {'senal': senal, 'mensaje': mensaje}

    for pdf in validador:
        try:
            objUnidor.append(pdf)
            log.info(f'PDF agregado correctamente {pdf}')
        except Exception as e:
            log.error(f'Error: {e}')

            mensaje = f'Error: {e}'
            return {'senal': senal, 'mensaje': mensaje}

    salida_pdf = Path(salida_pdf)

    try:
        objUnidor.write(str(salida_pdf))
        log.info(f'PDF unidos correctmanete {salida_pdf}')
        senal = True
        mensaje = "PDF unido correctamente"
        return {'senal': senal, 'mensaje': mensaje}


    except Exception as e:
        log.error(f'Error: {e}')
        mensaje = f"Error: {e}"
        return {'senal': senal, 'mensaje': mensaje}
    finally:
        objUnidor.close()
