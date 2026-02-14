from docx2pdf import convert
import os

from util.logger_configuracion import setup_logger
from util.rutas_validaciones import validar_rutas

def convertir_word_pdf(*ruta_archivos_word):

    # Validacion de las rutas
    log = setup_logger()
    validador = validar_rutas(ruta_archivos_word , '.docx')

    if not validador:
        log.error('No se encontraron archivos word')
        return

    for archivo_word in validador:
        try:
           convert(archivo_word)

        except Exception as e:
            log.error(f'Error en ruta: {e}')
            return
        else:
            log.info(f'La conversión fue exitosa\n '
                     f'ruta final: {archivo_word}')

if __name__ == '__main__':

    convertir_word_pdf("D:\CEUTEC\Trabajos Ceutec Periodo 5\Comercio Electronico\\tarea 7\portadaa - copia.docx"
,"D:\CEUTEC\Trabajos Ceutec Periodo 5\Comercio Electronico\\tarea 7\portadaa.docx")