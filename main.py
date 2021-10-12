import csv

with open('subvenciones.csv', encoding='latin1') as fichero_csv: # latin1 nos permite trabajar con tildes.
    lector = csv.reader(fichero_csv)
    next(lector, None)  # Se salta la cabecera
    asociaciones = {}
    for linea in lector:
        centro = linea[0]
        subvencion = float(linea[2])
        if centro in asociaciones:
            asociaciones[centro] = asociaciones[centro] + subvencion
        else:
            asociaciones[centro] = subvencion
    print(asociaciones)
