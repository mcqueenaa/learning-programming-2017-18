import urllib.request 
import re
import html
import os
import json
from flask import Flask
from flask import url_for, render_template, request, redirect
from random import choice

app = Flask(__name__)

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
req = urllib.request.Request('https://yandex.ru/pogoda/skopje', headers={'User-Agent':user_agent})
news = urllib.request.Request('https://www.kommersant.ru/', headers={'User-Agent':user_agent})
regwords = re.compile('<td class="uu">([А-Яа-я]*?)</td><td></td><td class="uu">(.*?)</td>', re.DOTALL)
regfirst = re.compile('(([А-Яа-я]|\'|&#(\d{4});)*?)(,|\s|\b)', re.DOTALL)
regTag = re.compile('<.*?>', re.DOTALL)
allpages = ['http://www.dorev.ru/ru-index.html?l=c0', 'http://www.dorev.ru/ru-index.html?l=c1', 'http://www.dorev.ru/ru-index.html?l=c2', 'http://www.dorev.ru/ru-index.html?l=c3', 'http://www.dorev.ru/ru-index.html?l=c4', 'http://www.dorev.ru/ru-index.html?l=c5', 'http://www.dorev.ru/ru-index.html?l=c6', 'http://www.dorev.ru/ru-index.html?l=c7', 'http://www.dorev.ru/ru-index.html?l=c8', 'http://www.dorev.ru/ru-index.html?l=c9', 'http://www.dorev.ru/ru-index.html?l=ca', 'http://www.dorev.ru/ru-index.html?l=cb', 'http://www.dorev.ru/ru-index.html?l=cc', 'http://www.dorev.ru/ru-index.html?l=cd', 'http://www.dorev.ru/ru-index.html?l=ce', 'http://www.dorev.ru/ru-index.html?l=cf', 'http://www.dorev.ru/ru-index.html?l=d0', 'http://www.dorev.ru/ru-index.html?l=d1', 'http://www.dorev.ru/ru-index.html?l=d2', 'http://www.dorev.ru/ru-index.html?l=d3', 'http://www.dorev.ru/ru-index.html?l=d4', 'http://www.dorev.ru/ru-index.html?l=d5', 'http://www.dorev.ru/ru-index.html?l=d6', 'http://www.dorev.ru/ru-index.html?l=d7', 'http://www.dorev.ru/ru-index.html?l=d8', 'http://www.dorev.ru/ru-index.html?l=d9', 'http://www.dorev.ru/ru-index.html?l=da', 'http://www.dorev.ru/ru-index.html?l=db', 'http://www.dorev.ru/ru-index.html?l=dc', 'http://www.dorev.ru/ru-index.html?l=dd', 'http://www.dorev.ru/ru-index.html?l=de', 'http://www.dorev.ru/ru-index.html?l=df']


def getdict():
    dorevdict = {}
    for p in allpages:
        with urllib.request.urlopen(p) as hpage:
            html = hpage.read().decode('windows-1251')
        for i in re.findall(regwords, html):
            dorevdict[i[0]] = regTag.sub("", i[1])
            if re.search(regfirst, dorevdict[i[0]]):
                dorevdict[i[0]] = re.search(regfirst, dorevdict[i[0]]).group(1)
    with open('dictionary.json', "w", newline="") as file:
        file.write(json.dumps(dorevdict, ensure_ascii = False))
        
def downloadpage():
    #mystem в одной папке с программой
    with urllib.request.urlopen(news) as response:
       html = response.read().decode('windows-1251')
       cyryl = re.findall('([А-Я]*[а-я]*)?', html)
       for w in cyryl:
           if w != '':
               with open ('words.txt', 'a', encoding = 'utf-8') as m:
                   m.write(w + ' ')
       input_txt = os.path.join('words.txt ')
       output_txt = os.path.join('mystemwords.txt')
       os.system('mystem.exe ' + '-di ' + input_txt + output_txt)

def weather():
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
    regtemp = re.compile('<div class="temp fact__temp"><span class="temp__value">(.*?)</span>', flags= re.DOTALL)
    regcond = re.compile('<div class="fact__condition day-anchor i-bem" data-bem=(.*?)>(.*?)</div>')
    condition = re.search(regcond, html).group(2)
    temp = re.search(regtemp, html).group(1)
    weatheris = 'Погода в Скопье сейчас: ' + condition + ', ' + temp + '.'
    return weatheris

@app.route('/') 
def main():
    weatheris = weather()
    return render_template('main1.html', weather = weatheris)  

@app.route('/dorev/') 
def word():
    if os.path.exists('dictionary.json') == False:
        getdict()
    with open('dictionary.json', "r") as file: 
        d = file.read()
    weatheris = weather()
    word = request.args['username']
    for key in d:
        if word == key:
            word = d[key]
            break
    if re.search('\'', word):
        word = re.sub('\'', "", word)
    word = html.unescape(word)
    return render_template('main2.html', weather = weatheris, oldword = word) 

##@app.route('/2')
##def page2():
##    return render_template('news.html')

@app.route('/3')
def page3():
    return render_template('page3.html')

@app.route('/check/')
def check():
    k = 0
    wrong = ''
    answers = dict(request.args)
    for i in answers:
        if answers[i][0] == 'w':
            k+= 1
            if wrong == '':
                wrong = wrong + i
            else:
                wrong = wrong + ',' + i
    if k == 0:
        result = 'Ура! У Вас нет ошибок!'
    else:
        result = 'У Вас ' + str(k) + ' ошибок (ошибки) в тесте. Вы ошиблись в вопросах: ' + wrong + '.'
    return render_template('check.html', result = result)

if __name__ == '__main__':
    getdict()
    downloadpage()
    app.run(debug=True)
