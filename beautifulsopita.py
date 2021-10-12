from bs4 import BeautifulSoup
import requests
import re

url="misegundapagina.html"
url2="https://www.kassoon.com/dnd/5e/premade-characters/"

r = requests.get(url2)
print(r)
tabla = re.search('<table class="sortable">[\S\s]*</table>', r.content.decode())
print(tabla)
th_lista = re.findall("((?<=<th>)[^<]*)", tabla.string)
print(th_lista)
pers_lista = re.findall('(?<=<tr class="light">).*?(?=</tr>)', tabla.string)
print(pers_lista)
lista_personajes = []
for pj in pers_lista:
    i = re.findall('(?<=<td>).*?(?=</td>)', pj)
    if len(i) != 0: lista_personajes.append(i)
print(lista_personajes)


# '(?<=<tr class="light">).*?(?=</tr>)'
# soup = BeautifulSoup(r.content,"html5lib")
#
#
# thead = soup.table.thead
# cabeceras = []
# for ths in thead.findAll("th"):
#     cabeceras.append(ths.string)
# print(cabeceras)
# personajes = soup.table.tbody.findAll("tr")
# for pj in personajes:
#     lista = []
#     for tds in pj.findAll("td"):
#         lista.append(tds.text)
#     print(lista)