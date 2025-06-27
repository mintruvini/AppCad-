import ezdxf

def analizar_dwg(ruta_archivo):
    '''
    Abre un archivo DWG y extrae información básica para validación.
    Retorna un diccionario con datos y una lista de advertencias si faltan cosas.
    '''
    resultado = {
        "superficie_total": None,
        "altura_maxima": None,
        "retiros": None,
        "capas_detectadas": [],
        "errores": []
    }

    try:
        doc = ezdxf.readfile(ruta_archivo)
        msp = doc.modelspace()

        # Recolectar capas
        resultado["capas_detectadas"] = list(doc.layers.names())

        # Buscar textos que indiquen altura, superficie, etc.
        for entidad in msp:
            if entidad.dxftype() == 'TEXT':
                texto = entidad.dxf.text.lower()

                if "superficie" in texto and resultado["superficie_total"] is None:
                    resultado["superficie_total"] = texto

                if "altura" in texto and resultado["altura_maxima"] is None:
                    resultado["altura_maxima"] = texto

                if "retiro" in texto and resultado["retiros"] is None:
                    resultado["retiros"] = texto

    except Exception as e:
        resultado["errores"].append(str(e))

    return resultado
