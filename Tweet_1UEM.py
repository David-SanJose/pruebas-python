# Importo librerias de hilos y time para esperar
import threading
import time
# Libreria de twitter
import tweepy #https://github.com/tweepy/tweepy
# Libreria del sistema, para tomar el tamaño del archivo
import os

from tweepy import Stream
from tweepy import OAuthHandler

# Creo un listener que hereda de Stream, para asi poder modificar la funcion
# on_data y on_disconnect, alterando como y cuando escribe en el archivo los datos
class MyListener (Stream):
    #Archivo donde se almacenaran los tweets
    path_json = "SpydyNWH.json"

    # Función que se llama cada vez que entra un nuevo dato,
    # introduciendolo en el archivo json
    def on_data(self, data):
        # Abre el archivo y escribe un "[" si está vacio y una
        # "," si ya tiene algun dato. Despues escribe el dato
        with open (self.path_json, 'a') as f:
            if os.path.getsize(self.path_json) > 0:
                f.write(",")
            else:
                f.write("[")
        try:
            with open(self.path_json, 'ab') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error en el dato: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

    # Cuando se desconecta escribe el corchete de cierre del json
    def on_disconnect(self):
        with open(self.path_json, 'a') as f:
            f.write("]")


# Espera 2 minutos y cierra la conexion
def cerrarALos2min(stream: Stream):
    print("inicio")
    time.sleep(120)
    stream.disconnect()

#Credenciales del Twitter API
consumer_key = "0n8rRu7WcloD53DdsEBJbZIsl"
consumer_secret = "WWNvWcYJkUTS6rf6MxAAds9J9OobygankFmSi4LIggmjpF2oTw"
access_token = "930839056715603968-mKMUqgdQ7E4cO7bUJslSHRaxzkcFHYo"
access_secret = "xGlonpxh7WV0NFsusAiYxFMtLAaWI1rRHnafs6X8KHSgm"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

twitter_stream = MyListener(consumer_key, consumer_secret, access_token, access_secret)
# Lanzo un hilo con la funcion que espera 2 min, para darle tiempo a que tome los tweets
tempo = threading.Thread(target=cerrarALos2min, args=(twitter_stream,))
tempo.start()
# Mientras el hilo se ejecuta, lanzo la busqueda de los tweets relacionados con la
# pelicula de Spiderman No Way Home, la cual era trending en el momento
twitter_stream.filter(track=['#SpiderManNoWayHome'])






