#Раз в 10 минут бот постит по предложению из "Война и мир".
import tweepy
import urllib.request  
import re
import html
import time
import os
import flask
from pymystem3 import Mystem
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
m = Mystem()
app = flask.Flask(__name__)

regTag = re.compile('<.*?>', re.DOTALL)

def get_warnpeace():
    beg = 'http://ilibrary.ru/text/11/p.'
    end = '/index.html'
    for i in range(1,362):
        url = beg + str(i) + end
        page = urllib.request.Request(url)
        with urllib.request.urlopen(page) as hpage:
            html = hpage.read().decode('windows-1251')
        print(i)
        if re.search('<h3>(.*?)</h3>', html, re.DOTALL):
            chapt = re.search('<h3>(.*?)</h3>', html, re.DOTALL).group(1)
            if chapt == 'I':
                if re.search('<h3>(.*?)<div ', html, re.DOTALL):
                    text = re.search('>(Том|Эпилог).*?Часть.*?<.*?>.*?<div ', html, re.DOTALL).group(0)
            else:
                if re.search('<h3>(.*?)<div ', html, re.DOTALL):
                    text = re.search('<h3>(.*?)<div ', html, re.DOTALL).group(1)
        text = re.sub('<div ', '', text) 
        text = re.sub(regTag, '', text)
        text = re.sub('>', '', text)
        text = re.sub('&nbsp;\d', '', text)
        with open ('War and Peace.txt', 'a', encoding = 'utf-8') as m:
            m.write(text + ' ')   

def sent():
    if os.path.exists('War and Peace.txt') == False:
       get_warnpeace() 
    with open ('War and Peace.txt', 'r', encoding = 'utf-8') as m:
        text = m.read()
    reg = r'[^(\s)].*?[\.\?\!]+|[А-ЯA-Z][\s[а-яa-z]+[\.\?\!\,]+\s&mdash;\s.*?[\.\?\!]+|&mdash;\s[А-ЯA-Z][\s[а-яa-z]+[\.\?\!\,]+\s&mdash;\s.*?[\.\?\!]+'
    arr = re.findall(reg, text)
    return arr
    
def main():
    sentences = sent()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    for text in sentences:
        text = re.sub('&mdash;', '—', text)
        if len(text) > 280:
            while len(text) > 280:
                ana = m.analyze(text)
                for i in range(len(ana)):
                    if 'analysis' in ana[i]:
                        if ana[i]['analysis'][0]['gr'][0:2] == 'A=':
                            text = re.sub(ana[i]['text'], '', text)
                        elif ana[i]['analysis'][0]['gr'][0:3] == 'ADV':
                            text = re.sub(ana[i]['text'], '', text)
                text = re.sub('\s\s', ' ', text)
                if re.match('\s', text):
                    text = text[1:len(text)]
            if re.match('[а-яa-z]', text):
                f = text[0].upper()
                text = f + text[1:len(text)]
        api.update_status(html.unescape(text))
        time.sleep(600)

if __name__ == '__main__':
    main()    
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
















                
