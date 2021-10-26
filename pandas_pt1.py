import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

column_names = [
    "id", "text",
    "lang", "user.screen_name",
    "user.description", "user.followers_count",
    "user.friends_count", "user.favourites_count",
    "user.statuses_count", "user.created_at",
    "retweet_count", "favorite_count", "reply_count",
    "quote_count"]
column_names_retw = ["retweeted_status." + s for s in column_names]


def get_full_dataframe(file: str) -> pd.DataFrame:
    # Leemos el json
    with open(file, 'r') as f:
        tweets_str = f.read()
        tweets_json = json.loads(tweets_str)
        # Transformamos el json a dataframe normalizandolo,
        # de forma que los campos anidados sean de facil acceso
        # y lo devolvemos
        #
        # Ejemplo:
        # "user": {"name" = "Paco"  --> "user.name" = "Paco"
        return pd.json_normalize(tweets_json)


# Función que une los tweets y los retweets linkeados a los mismos
# de forma que todos formen parte del mismo dataframe.
#
# Se basa en acceder al objeto "retweeted_status" del tweet
# inicial, el cual es otro tweet, tomar ambos y almacenarlos
# en 2 dataframes diferentes, hacer que los nombres de las
# columnas coincidan, y unir ambos df en uno solo
def append_tweets_and_retweets(df_full: pd.DataFrame) -> pd.DataFrame:
    # Dataframes de tweets y tweets retweeteados
    df = pd.DataFrame(df_full.get(column_names))
    df_retw = pd.DataFrame(df_full.get(column_names_retw))
    # Obtenemos un diccionario de equivalencias entre nombres de columnas
    dict_column_equivalences = dict(zip(column_names_retw, column_names))
    # Renombramos todas las columnas para igualarlas a las de df
    df_retw.rename(columns=dict_column_equivalences, inplace=True)
    # Une ambos df y devuelve el resultante
    return df.append(df_retw)


# Limpia de duplicados, valores no interesantes y baraja el df
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df = df.dropna(thresh=len(df.columns) - 2)
    df = df.sample(frac=1)

    return df


# Muestra un grafico de barras con el numero de tweets sobre
# \#SpiderManNoWayHome según el idioma
def plot_num_of_comments_by_leng(df: pd.DataFrame):
    # Comentarios según idioma, ordenados por frecuencia
    num_by_lang = df.groupby(by="lang")["id"].count().sort_values(ascending=False)
    # Creamos las listas que representaran las "X" y las "Y"
    lang = list(num_by_lang.index)
    count = num_by_lang.values
    # Mostramos el gráfico
    plt2 = sns.barplot(x=lang, y=count)
    plt2.set(xlabel="Idioma", ylabel="Total")
    plt.show()


# Muestra un mapa de calor de distintas variables relacionadas
# con el usuario y sus interacciones
def users_variables_correlation(df: pd.DataFrame):
    # Relación de variables
    df_num = df.get(["user.followers_count",
                     "user.friends_count", "user.favourites_count",
                     "user.statuses_count", "retweet_count",
                     "favorite_count", "reply_count",
                     "quote_count"])
    sns.set(rc={'figure.figsize': (15, 8)})
    sns.heatmap(data=df_num.corr(), annot=True, linewidths=.5)
    plt.show()


# MENU DE GRÁFICAS
df1 = clean_dataframe(append_tweets_and_retweets(get_full_dataframe('SpydyNWH.json')))
str_menu = """Elige una opción:
1-Numero de tweets sobre #SpiderManNoWayHome por idioma
2-Relación de variables de usuario
3-Salir
"""
a = ""
while a != "3":
    a = input(str_menu).strip()
    if a == "1":
        plot_num_of_comments_by_leng(df1)
    elif a == "2":
        users_variables_correlation(df1)
