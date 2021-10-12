## Ejecutar hasta aquí... Y luego el resto.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

lat = driver.find_element_by_id("ctl00_Contenido_txtLatitud")
lon = driver.find_element_by_id("ctl00_Contenido_txtLongitud")
latitud = "28.2723368"
longitud = "-16.6600606"
lat.send_keys(latitud)
lon.send_keys(longitud)

cart = driver.find_element_by_id("ctl00_Contenido_btnNuevaCartografia")
cart.click()
driver.get(url)

coord = driver.find_element_by_id("tabcoords")
coord.click()