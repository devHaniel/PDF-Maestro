from docx2pdf import convert
import os

from util.logger_configuracion import setup_logger
from util.rutas_validaciones import validar_rutas

def convertir_word_pdf(*ruta_archivos_word):

    """

    Args:
        *ruta_archivos_word: cadenas de texto con rutas de .docx

    Returns:
        senal = boolean -> Operacion exitosa o no.\n
        mensaje = indica que paso.
    """

    senal = False
    mensaje = ""
    # Validacion de las rutas
    log = setup_logger()
    validador = validar_rutas(ruta_archivos_word , '.docx')

    if not validador:
        log.error('No se encontraron archivos word')
        mensaje = "No se encontraron archivos word"
        return {'senal' : senal, 'mensaje' : mensaje}

    for archivo_word in validador:
        try:
           convert(archivo_word)
        except Exception as e:
            log.error(f'Error en ruta: {e}')
            mensaje = f"Error: {e}"
            return {'senal' : senal, 'mensaje' : mensaje}
        else:
            log.info(f'La conversión fue exitosa\n '
                     f'ruta final: {archivo_word}')

            senal = True
            mensaje = f"Operación exitosa."

    return { 'senal' : senal, 'mensaje' : mensaje}