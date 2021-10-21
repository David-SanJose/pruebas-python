import selenium.common.exceptions as selExceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

from bs4 import BeautifulSoup
import requests
import re


class CookieBot:
    driver = None

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://orteil.dashnet.org/cookieclicker/"
        self.driver.get(url)
        time.sleep(1)

    def click_cookie(self):
        coord = self.driver.find_element_by_id("bigCookie")
        coord.click()
        time.sleep(0.005)

    def get_actual_cookies(self) -> str:
        return self.parse_textcookies_to_int(
            self.driver.find_element_by_id("cookies").text)

    def get_unlocked_products(self):
        products_table = self.driver.find_element_by_id("products")
        products = products_table.find_elements_by_xpath("//div[contains(@class,"
                                                         " 'product unlocked enabled')]")
        print(type(products))
        return products
        # for p in products:
        #     print(p.find_element_by_class_name("price").text)

    def get_unlocked_upgrades(self):
        return self.driver.find_elements_by_xpath("//div[contains(@class, "
                                                  "'crate upgrade enabled')]")

    def buy_most_expensive_upgrade(self):
        try:
            u_upgr = self.get_unlocked_upgrades()
            u_upgr.reverse()
            if len(u_upgr) > 0: u_upgr[0].click()
        except selExceptions.StaleElementReferenceException:
            print("UPGRADE BUY FAILED: Element not attached to the page")
        except selExceptions.ElementClickInterceptedException:
            print("UPGRADE BUY FAILED: element click intercepted")

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

    def parse_textcookies_to_int(self, text: str):
        t = text
        t = t.replace(",", "")
        t = t.replace(".", "")
        t = t.replace("million", "000")
        t = t.replace(" ", "")
        t = t.replace("cookies", "")
        print(t[0:t.find("p")])
        return int(t[0:t.find("p")])

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

    def open_new_tab(self, url: str):
        self.driver.execute_script(f'''window.open("{url}","_blank");''')
        time.sleep(2)
        for handle in self.driver.window_handles:
            if handle != self.driver.current_window_handle:
                self.driver.switch_to.window(handle)

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
        
    def test_first_searched_product(self):
        time.sleep(1)
        busquedas = self.driver.find_element_by_id("SearchResultsGrid")
        url_busquedas = []
        for b in busquedas.find_elements_by_class_name("styles__link--3QJ5N"):
            url_busquedas.append(b.get_attribute("href"))
    
        #print("URLs: ",url_busquedas)
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
        
    def get_all_products_info_by_url(self, url:str):
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html5lib")
        tabla = soup.find(id = "SearchResultsGrid")
        matriz_products = []
        for a in tabla.findAll("a"):
            lista_product = []
            lista_product.append(a.get("href"))
            for span in a.findAll("span"):
                texto = span.text.strip()
                if texto != "": lista_product.append(texto)
                    
            matriz_products.append(lista_product[0:3])
        
        print(matriz_products)
bot = CookieBot()
url_camisetas_w = bot.open_merchan_shop()
bot.get_all_products_info_by_url(url_camisetas_w)
bot.test_first_searched_product()
# bot.load_game("cookie_game_file")
# time.sleep(2)
# for j in range(5):
#     for i in range(100):
#         bot.click_cookie()
#     bot.buy_most_expensive_upgrade()
#     bot.buy_most_expensive_product()
#
# bot.save_game("cookie_game_file")
# time.sleep(2)


## Ejecutar hasta aquí... Y luego el resto.

# lat = driver.find_element_by_id("ctl00_Contenido_txtLatitud")
# lon = driver.find_element_by_id("ctl00_Contenido_txtLongitud")
# latitud = "28.2723368"
# longitud = "-16.6600606"
# lat.send_keys(latitud)
# lon.send_keys(longitud)
#
# cart = driver.find_element_by_id("ctl00_Contenido_btnNuevaCartografia")
# cart.click()


#
# html = driver.find_element_by_xpath("/html")
# print(html.text)
#
# head = driver.find_element_by_xpath("/html/head")
# body = driver.find_element_by_xpath("/html/body")
# html2 = body.find_element_by_xpath("/html")
#
# hijos = driver.find_elements_by_xpath("/html/body/*")
# for element in hijos:
#     print(element.tag_name)