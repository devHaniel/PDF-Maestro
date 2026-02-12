from PyPDF2 import PdfMerger
from pathlib import Path

from util.logger_configuracion import setup_logger
from util.rutas_validaciones import validar_rutas

def unir_pdfs(rutas_pdf, salida_pdf):

    # Validacion de las rutas
    log = setup_logger()
    objUnidor = PdfMerger()

    validador = validar_rutas(rutas_pdf, '.pdf')

    if not validador:
        log.warning('No se encontraorn pdfs')
        return

    for pdf in validador:
        try:

            objUnidor.append(pdf)
            log.info(f'PDF agregado correctamente {pdf}')

        except Exception as e:
            log.error(f'Error: {e}')


    salida_pdf = Path(salida_pdf)

    try:
        objUnidor.write(str(salida_pdf))
        log.info(f'PDF unidos correctmanete {salida_pdf}')
    except Exception as e:
        log.error(f'Error: {e}')
    finally:
        objUnidor.close()

if __name__ == '__main__':
    unir_pdfs(['n.pdf','s.pdf'],'s.pdf')