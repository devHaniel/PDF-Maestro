from pathlib import Path
from logger_configuracion import setup_logger

logger = setup_logger()

def valdiad_Rutas(rutas, extension):

    """
    Devuelve una lista de las rutas validas\n
    sino encuentra alguna, se devolvera una cadena vacia.
    
    Args:
        rutas     : lista de rutas.
        extension : extension que debe tener cada ruta. 
    """

    salida = []

    for ruta in rutas:

        ruta = Path(ruta)

        if not ruta.exists() or ruta.suffix.lower() != extension:
            logger.warning(f'{ruta} no existe o no es un PDF')
            continue

        salida.append(ruta)

    logger.info(f'salida: {salida}')
    return salida

if __name__ == '__main__' : 
    valdiad_Rutas(['hola.pdf','pruea.pdf'],'.pdf')
