import matplotlib.pyplot as plt
import csv
import requests
url = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
resp = requests.get(url)

# with open("horario.csv", "wb") as output:
#     output.write(resp.content)
with open("horario.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if (row[0] + row[1] + row[2]) == '28079008' and row[3] == '10':
            plt.title("Óxido de nitrógeno: " + row[8] + "/" + row[7] + "/" + row[6])
            hora = 0
            desp = 9
            vs = []
            horas = []

            while hora <= 23:
                ## Esto quiere decir que si el valor de lectura en la hora corresponde con un valor válido.
                if row[desp + 2 * hora + 1] == 'V':
                    vs.append(int(row[desp + 2 * hora]))
                    horas.append(hora)
                hora += 1
            plt.plot(horas, vs)
            plt.show()
