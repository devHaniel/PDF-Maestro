import logging

from logging import FileHandler, Formatter

def setup_logger(nombre_logger = 'PDF-maestro', archivo_salida = '../app.log'):

    """
        Configuracion del logger global
    """

    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicados
    if not logger.handlers:

        archivo_handler = FileHandler(archivo_salida)
        archivo_handler.setLevel(logging.DEBUG)
        archivo_handler.setFormatter(
            Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        )

        # consola

        consola_handler = logging.StreamHandler()
        consola_handler.setLevel(logging.DEBUG)
        consola_handler.setFormatter(
            Formatter('%(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        )

        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

    return logger

