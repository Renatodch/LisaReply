import csv

proyectos =[]

congresista_csv = './data/congresista.csv'
proyecto_csv = './data/proyecto.csv'

with open(proyecto_csv, 'r', encoding='utf-8') as proyecto:
    lector_proyecto_csv = csv.DictReader(proyecto)
    proyects_all = [proyecto for proyecto in lector_proyecto_csv]

with open(congresista_csv, 'r', encoding='utf-8') as congresista:
    lector_csv = csv.DictReader(congresista)
    texto_congresista=''
    for fila in lector_csv:
        nombre = fila['Nombres del Congresista']
        votacion = fila['Votacion Obtenida']
        anio_legislativo = fila['Año Legislativo']
        inicio_funciones = fila['Inicio de Funciones']
        termino_funciones = fila['Termino de Funciones']
        partido_politico = fila['Partido Politico']
        bancada = fila['Bancada que pertence']
        region = fila['Representa a']
        url_proyectos = fila['Url de Proyectos']
        condicion = fila['Condicion']

        texto_congresista += f"Nombre: {nombre}\n" \
                            f"Votación obtenida: {votacion}\n" \
                            f"Año legislativo: {anio_legislativo}\n" \
                            f"Inicio de funciones: {inicio_funciones}\n" \
                            f"Término de funciones: {termino_funciones}\n" \
                            f"Partido político: {partido_politico}\n" \
                            f"Bancada: {bancada}\n" \
                            f"Región: {region}\n" \
                            f"URL de proyectos: {url_proyectos}\n" \
                            f"Condición: {condicion}\n" \

        texto_congresista += '-' * 50 + '\n'

        archivo_texto = open("./data/data_congresista.txt", "w", encoding="utf-8")
        archivo_texto.write(texto_congresista)
