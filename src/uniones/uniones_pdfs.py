from PyPDF2 import PdfMerger
from pathlib import Path

def unir_pdfs(rutas_pdf, salida_pdf):

    # Validacion de las rutas
    objUnidor = PdfMerger()

    for ruta in rutas_pdf:
        ruta = Path(ruta)

        if not ruta.exists() or ruta.suffix.lower() != '.pdf':
            print(f'Advertencia: {ruta} no existe o no es un PDF')
            continue

        objUnidor.append(ruta)

    if len(objUnidor.pages == 0):
        print('No se agregaron PDFS validos')
        return
    
    salida_pdf = Path(salida_pdf)

    objUnidor.write(str(salida_pdf))

    objUnidor.close()

    print(f'PDF unidos correctamente en {salida_pdf}')


