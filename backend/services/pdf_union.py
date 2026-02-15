from PyPDF2 import PdfMerger
from pathlib import Path
from backend.utils.logger_configuracion import setup_logger
from backend.utils.rutas_validaciones import validar_rutas

def unir_pdfs(rutas_pdf: list[str], salida_pdf: str) -> dict:
    """
    Une varios archivos PDF en uno solo.

    Args:
        rutas_pdf: Lista de rutas de los archivos pdf.
        salida_pdf: Ruta de salida con extensión .pdf

    Returns:
        dict: {
            'senal': bool -> Operación exitosa o no,
            'mensaje': str -> Mensaje descriptivo
        }
    """

    log = setup_logger()
    senal = False
    mensaje = ""
    objUnidor = PdfMerger()

    # Validar rutas
    validador = validar_rutas(rutas_pdf, '.pdf')
    if not validador:
        mensaje = "No se encontraron PDFs válidos."
        log.warning(mensaje)
        return {'senal': senal, 'mensaje': mensaje}

    # Intentar agregar cada PDF
    for pdf in validador:
        try:
            objUnidor.append(pdf)
            log.info(f"PDF agregado correctamente: {pdf}")
        except Exception as e:
            mensaje = f"Error agregando {pdf}: {e}"
            log.error(mensaje)
            objUnidor.close()
            return {'senal': senal, 'mensaje': mensaje}

    # Guardar PDF final
    try:
        salida_path = Path(salida_pdf)
        objUnidor.write(str(salida_path))
        senal = True
        mensaje = f"PDF unido correctamente en {salida_path}"
        log.info(mensaje)
    except Exception as e:
        mensaje = f"Error escribiendo PDF final: {e}"
        log.error(mensaje)
    finally:
        objUnidor.close()

    return {'senal': senal, 'mensaje': mensaje}
