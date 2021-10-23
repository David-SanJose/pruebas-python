# IMPORTS DE SELENIUM
import selenium.common.exceptions as selExceptions
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
# PARA INTRODUCIR ESPERAS
import time
# BEAUTIFULSOUP Y REQUEST DE PAGINAS
from bs4 import BeautifulSoup
import requests
# ALMACENAMIENTO EN ARCHIVO CSV
import csv

"""Bot con driver apuntando a la pagina del juego cookie clicker
con diversas funciones:
-Juega solo
    +Hace click en la galleta para conseguir puntos
    +Compra mejoras y productos para seguir avanzando
    +Carga partida si existe
    +Guarda partida en un archivo al terminar
-Accede a la tienda, seleccionando los diversos filtros de productos
pulsando botones, listas desplegables, round buttons, etc. Obteniendo
tambien mediante beautiful soup info de los productos, y almacenando esta
en un archivo csv"""


class CookieBot:
    driver = None

    def __init__(self):  # Carga el driver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://orteil.dashnet.org/cookieclicker/"
        self.driver.get(url)
        time.sleep(1)  # Espera para que la pagina cargue

    def click_cookie(self):  # Hace click en la galleta
        coord = self.driver.find_element_by_id("bigCookie")
        coord.click()
        time.sleep(0.005)

    # Devuelve el valor de galletas total actual
    def get_actual_cookies(self) -> int:
        return self.parse_textcookies_to_int(
            self.driver.find_element_by_id("cookies").text)

    # Devuelve los productos disponibles para comprar con galletas
    def get_unlocked_products(self):
        products_table = self.driver.find_element_by_id("products")
        products = products_table.find_elements_by_xpath("//div[contains(@class,"
                                                         " 'product unlocked enabled')]")
        return products

    # Devuelve las mejoras de productos disponibles para comprar con galletas
    def get_unlocked_upgrades(self):
        return self.driver.find_elements_by_xpath("//div[contains(@class, "
                                                  "'crate upgrade enabled')]")

    # Trata de comprar la mejora más alta disponible
    def buy_most_expensive_upgrade(self):
        try:
            # Toma todas las mejoras, da la vuelta a la lista y hace click
            # en el primer elemento (el más caro)
            u_upgr = self.get_unlocked_upgrades()
            u_upgr.reverse()
            if len(u_upgr) > 0: u_upgr[0].click()
        except selExceptions.StaleElementReferenceException:
            print("UPGRADE BUY FAILED: Element not attached to the page")
        except selExceptions.ElementClickInterceptedException:
            print("UPGRADE BUY FAILED: element click intercepted")

    # Compra el producto más alta disponible
    def buy_most_expensive_product(self):
        try:
            a_cookies = self.get_actual_cookies()
            u_prod = self.get_unlocked_products()
            u_prod.reverse()
            for p in u_prod:
                price = self.parse_textcookies_to_int(
                    p.find_element_by_class_name("price").text.split()[0])
                if price <= a_cookies:
                    p.click()
                    break
        except selExceptions.StaleElementReferenceException:
            print("PRODUCT BUY FAILED: Element not attached to the page")
        except selExceptions.ElementClickInterceptedException:
            print("PRODUCT BUY FAILED: element click intercepted")

    # Transforma el texto extraido de las galletas a int, para
    # poder operar después
    def parse_textcookies_to_int(self, text: str):
        t = text
        t = t.replace(",", "")
        t = t.replace(".", "")
        t = t.replace("million", "000")
        t = t.replace(" ", "")
        t = t.replace("cookies", "")
        return int(t[0:t.find("p")])

    # Toma el texto que representa el estado actual de la partida
    # y lo almacena en un archivo .txt
    def save_game(self, file_name):
        self.driver.find_element_by_id("prefsButton").click()
        self.driver.find_element_by_xpath("//a[contains(@onclick, "
                                          "'Game.ExportSave()')]").click()

        save_text = self.driver.find_element_by_id("textareaPrompt").text
        with open(f"{file_name}.txt", mode="w") as file:
            file.write(save_text)
        time.sleep(0.5)
        self.driver.find_element_by_id("promptOption0").click()
        self.driver.find_element_by_id("prefsButton").click()

    # Toma el texto que representa el estado anterior de la partida
    # almacenado en un .txt y lo carga en la página
    def load_game(self, file_name):
        self.driver.find_element_by_id("prefsButton").click()
        self.driver.find_element_by_xpath("//a[contains(@onclick, "
                                          "'Game.ImportSave()')]").click()
        with open(f"{file_name}.txt", mode="r") as file:
            save_text = file.read()
            self.driver.find_element_by_id("textareaPrompt"). \
                send_keys(save_text)
        self.driver.find_element_by_id("promptOption0").click()
        self.driver.find_element_by_id("prefsButton").click()

    # Abre una nueva página y cambia el control del driver a esta
    def open_new_tab(self, url: str):
        self.driver.execute_script(f'''window.open("{url}","_blank");''')
        time.sleep(2)
        for handle in self.driver.window_handles:
            if handle != self.driver.current_window_handle:
                self.driver.switch_to.window(handle)

    # Abre la página de la tienda, haciendo click en el enlace.
    # Tras esto seleciona multiples filtros de productos
    def open_merchan_shop(self) -> str:
        shop_button = self.driver. \
            find_element_by_xpath("//a[contains(@class, "
                                  "'blueLink')]")
        shop_button.click()
        for handle in self.driver.window_handles:
            if handle != self.driver.current_window_handle:
                self.driver.switch_to.window(handle)
        time.sleep(1)

        self.driver.find_element_by_xpath("//button[contains(@title, "
                                          "'Ropa')]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[contains(@title, "
                                          "'Camisetas')]").click()

        time.sleep(0.5)
        self.driver.find_element_by_xpath("//div[contains(@aria-label, "
                                          "'Género')]").click()
        return self.driver.current_url

    # Toma el primer producto filtrado, abre el enlace y seleciona
    # la 3ra talla disponible de la lista
    def test_first_searched_product(self):
        time.sleep(1)
        busquedas = self.driver.find_element_by_id("SearchResultsGrid")
        url_busquedas = []
        for b in busquedas.find_elements_by_class_name("styles__link--3QJ5N"):
            url_busquedas.append(b.get_attribute("href"))

        time.sleep(2)
        if len(url_busquedas) > 0:
            self.driver.get(url_busquedas[0])

        time.sleep(1)
        self.driver.find_element_by_xpath("//button[contains(@data-testid, "
                                          "'ds-select')]").click()
        time.sleep(1)
        menu_tallas = self.driver.find_element_by_xpath("//ul[contains(@class, "
                                                        "'styles__list--2nCOW')]")
        tallas = menu_tallas.find_elements_by_class_name("styles__listItem--1L58f")
        tallas[3].click()

    # Almacena en una matriz todos los productos filtrados en forma de
    # lista: [url, nombre, precio]
    def get_all_products_info_by_url(self, url: str) -> list:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        tabla = soup.find(id="SearchResultsGrid")
        matriz_products = []
        for a in tabla.findAll("a"):
            lista_product = [a.get("href")]
            for span in a.findAll("span"):
                texto = span.text.strip()
                if texto != "": lista_product.append(texto)

            matriz_products.append(lista_product[0:3])

        return matriz_products

    # Cierra la pagina actual y centra el foco en la primera (La del juego
    # de las galletas)
    def close_page(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Función para almacenar una lista en un csv
def save_list_to_csv(file: str, cabecera: list,lista: list):
    with open(file, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(cabecera)
        writer.writerows(lista)
        print(f"Fihero '{file}' guardado")


# Menú por terminal para controlar mucho mejor las pruebas de la página
bot = CookieBot()
val_menu = "0"
while val_menu != "4":
    val_menu = input("""Opciones (Del 1 al 4):
    1- Jugar
    2- Tienda
    3- Info
    4- Salir
    """)
    if val_menu == "1":
        bot.load_game("cookie_game_file")
        time.sleep(2)
        for j in range(5):
            for i in range(100):
                bot.click_cookie()
            bot.buy_most_expensive_upgrade()
            bot.buy_most_expensive_product()

        bot.save_game("cookie_game_file")
        time.sleep(2)
    elif val_menu == "2":
        url_camisetas_w = bot.open_merchan_shop()
        productos = bot.get_all_products_info_by_url(url_camisetas_w)
        save_list_to_csv("productos.csv", ["Url", "Nombre", "Precio"], productos)

        bot.test_first_searched_product()
        input("Enter para salir")
        bot.close_page()
    elif val_menu == "3":
        print("""-Jugar:
        Carga la partida si existe, y hace 5 iteraciones
        de 100 clicks, comprando al final tanto mejoras como
        productos (Juega solo), guardando tras esto la partida (Click en
        diversos elementos, lectura y escritura en campo de
        texto)
        
        -Tienda:
        Abre una nueva pestaña, accede a la tienda, despliega
        el menu de Ropa -> Camisetas, selecciona ropa de mujer,
        trae la info de todas las prendas y accede a la 2da, para
        despues elegir talla""")
