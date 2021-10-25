import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Libreria llamada glom
with open('SpydyNWH.json', 'r') as f:
    tweets_str = f.read()
    tweets_json = json.loads(tweets_str)

    df_full = pd.json_normalize(tweets_json)
    df = pd.DataFrame(df_full.get(["id", "text",
                                   "lang", "user.screen_name",
                                   "user.description", "user.followers_count",
                                   "user.friends_count", "user.favourites_count",
                                   "user.statuses_count", "user.created_at",
                                   "retweet_count", "favorite_count", "reply_count",
                                   "quote_count"]))
    df = df.drop_duplicates()
    df = df.dropna(thresh=len(df.columns) - 2)
    df = df.sample(frac=1)
    # Comentarios según idioma, ordenados por frecuencia
    num_by_lang = df.groupby(by="lang")["id"].count().sort_values(ascending=False)

    print(type(num_by_lang))
    lang = list(num_by_lang.index)
    count = num_by_lang.values
    plt2 = sns.barplot(x=lang, y=count)
    plt2.set(xlabel="Idioma", ylabel="Total")
    plt.show()
    # Relación de variables
    df_num = df.get(["user.followers_count",
                     "user.friends_count", "user.favourites_count",
                     "user.statuses_count", "retweet_count",
                     "favorite_count", "reply_count",
                     "quote_count"])
    print(df_num.values)
    sns.set(rc={'figure.figsize': (15, 8)})
    sns.heatmap(data=df_num.corr(), annot=True, linewidths=.5)
    plt.show()
