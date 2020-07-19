# tweetlistener.py
"""tweepy.StreamListener subclase que procesa los tweets que van llegando"""
import tweepy
from textblob import TextBlob

class TweetListener(tweepy.StreamListener):
    """Manejador de Tweets que llegan de la transmisión."""

    def __init__(self, api, limit=10):
        """Crea variables de instancia para seguimiento del numero de tweets."""
        self.tweet_count = 0
        self.TWEET_LIMIT = limit
        super().__init__(api)  # llama al constructor de la superclase

    def on_connect(self):
        """Llamado cuando la conexión se realizo exitosamente."""
        print('Conexión exitosa\n')

    def on_status(self, status):
        """Llamado cuando llega un nuevo Tweet."""
        # obtener el texto del tweet
        try:  
            tweet_text = status.extended_tweet.full_text
        except: 
            tweet_text = status.text

        print(f'Nombre de pantalla: {status.user.screen_name}:')
        print(f'            Idioma: {status.lang}')
        print(f'           Estatus: {tweet_text}')
        
        #Traduce el Tweet si no esta en español
        if status.lang != 'es':
            tweet_text = TextBlob(tweet_text).translate(to="es")
            print(f' Traducción: {tweet_text}')

        self.tweet_count += 1  # seguimiento del numero de tweets

        # si TWEET_LIMIT es alcanzado, regresa False para terminar.
        return self.tweet_count <= self.TWEET_LIMIT