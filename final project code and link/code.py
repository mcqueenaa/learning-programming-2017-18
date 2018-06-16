##Твиттер-бот, который по предложению постит какое-нибудь прозаическое произведение русской литературы (рассказ или повесть).
##Если предложение слишком длинное и не влезает в твит, бот должен сократить его так, чтобы потерять как можно меньше смысла
##Бот постит твиты раз в час
import tweepy
import urllib.request  
import re
import html
import time
import os
from pymystem3 import Mystem
from keys import consumer_key
from keys import consumer_secret
from keys import access_token
from keys import access_token
m = Mystem()

regTag = re.compile('<.*?>', re.DOTALL)

def get_book():
    beg = 'http://ilibrary.ru/text/1099/p.'
    end = '/index.html'
    for i in range(1,240):
        url = beg + str(i) + end
        page = urllib.request.Request(url)
        with urllib.request.urlopen(page) as hpage:
            html = hpage.read().decode('windows-1251')
        #print(i)
        if re.search('<h3>(.*?)</h3>', html, re.DOTALL):
            if re.search('<h3>(.*?)<div ', html, re.DOTALL):
                text = re.search('<h3>(.*?)<div ', html, re.DOTALL).group(1)
        text = re.sub('<div ', '', text) 
        text = re.sub(regTag, '', text)
        text = re.sub('>', '', text)
        text = re.sub('&nbsp;\d', '', text)        
        text = re.sub('&mdash;', '—', text)
        with open ('Anna.txt', 'a', encoding = 'utf-8') as m:
            m.write(text + ' ')   

def sent():
    if os.path.exists('Anna.txt') == False:
        get_book() 
    with open ('Anna.txt', 'r', encoding = 'utf-8') as m:
        text = m.read()
    reg = r'[^(\s)].*?[\.\?\!]+|[А-ЯA-Z][\s[а-яa-z]+[\.\?\!\,]+\s&mdash;\s.*?[\.\?\!]+|&mdash;\s[А-ЯA-Z][\s[а-яa-z]+[\.\?\!\,]+\s&mdash;\s.*?[\.\?\!]+'
    arr = re.findall(reg, text)
    sent = arr[0]
    return sent

def del_s(s):
    with open ('Anna.txt', 'r', encoding = 'utf-8') as m:
        b = m.read()
    if re.search(s, b):
        b = re.sub(s, '', b)
    with open ('Anna.txt', 'w', encoding = 'utf-8') as m:
        m.write(b)
            
def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)    
    api = tweepy.API(auth)
    k = 0
    while k < 1:
        text = sent()
        print(text)
        if len(text) > 280:
            while len(text) > 280:
                ana = m.analyze(text)
                for i in range(len(ana)):
                    try:
                        if 'analysis' in ana[i]:
                            if ana[i]['analysis'][0]['gr'][0:2] == 'A=':
                                text = re.sub(ana[i]['text'], '', text)
                            elif ana[i]['analysis'][0]['gr'][0:3] == 'ADV':
                                text = re.sub(ana[i]['text'], '', text)
                                text = re.sub('\s\s', ' ', text)
                    except:
                        h = 'do nothing'
                if re.match('\s', text):
                    text = text[1:len(text)]
            if re.match('[а-яa-z]', text):
                f = text[0].upper()
                text = f + text[1:len(text)]
        del_s(text)        
        api.update_status(html.unescape(text))
        time.sleep(3600)
 
if __name__ == '__main__':
    main()    















                
