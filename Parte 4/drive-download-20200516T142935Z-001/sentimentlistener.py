# sentimentlistener.py
"""Script que encuentra tweets que correspondan con cierta búsqueda
y determine el número de tweets positivos, negativos y neutrales"""

import keys
import preprocessor as p 
import sys
from textblob import TextBlob
import tweepy

class SentimentListener(tweepy.StreamListener):
    """Manejador de la transmisión de tweets"""

    def __init__(self, api, sentiment_dict, topic, limit=10):
        """Configuración de SentimentListener"""
        self.sentiment_dict = sentiment_dict
        self.tweet_count = 1
        self.topic = topic
        self.TWEET_LIMIT = limit
        # tweet-preprocessor elimina URLs/palabra reservadas
        p.set_options(p.OPT.URL, p.OPT.RESERVED) 
        super().__init__(api)  # llamada al constructor de la superclase

    def on_error(self, status_code):
        print(status_code)
    
    def on_connect(self):
        print('Conexión satisfactoria')

    def on_status(self, status):
        """Llamado cuando Twitter envia un nuevo tweet"""
        # obtiene el texto del tweet
        try:  
            tweet_text = status.extended_tweet.full_text
        except: 
            tweet_text = status.text

        # se ignoran los retweets
        if tweet_text.startswith('RT'):
            return

        tweet_text = p.clean(tweet_text)  # limpiando el tweet
        
        # ignora el tweet si el tópico no esta en el texto
        if self.topic.lower() not in tweet_text.lower():
            return

        # traduce el tweet si no esta en inglés
        try:
            if status.lang != 'en':
                tweet_text = str(TextBlob(tweet_text).translate())
        except:
            return
      
        # actualiza el diccionario de acuerdo a la polaridad
        blob = TextBlob(tweet_text)
        if blob.sentiment.polarity > 0:
            sentiment = '+'
            self.sentiment_dict['positivo'] += 1 
        elif blob.sentiment.polarity == 0:
            sentiment = ' '
            self.sentiment_dict['neutral'] += 1 
        else:
            sentiment = '-'
            self.sentiment_dict['negativo'] += 1 
            
        # muestra el tweet
        print(f'{sentiment} {status.user.screen_name}: {tweet_text}\n')
        
        self.tweet_count += 1  # seguimiento a los tweets procesados

        # Si TWEET_LIMIT es alcanzado, regresa Falso para terminar
        return self.tweet_count <= self.TWEET_LIMIT