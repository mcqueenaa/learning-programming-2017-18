from pymystem3 import Mystem
import pymorphy2
import urllib.request  
import re
import random
from pymorphy2 import MorphAnalyzer
import telebot
import conf
import flask

morph = MorphAnalyzer()
m = Mystem()

def words():
    regTag = re.compile('<.*?>', re.DOTALL)
    n = []
    v = []
    adjf = []
    adjs = []
    comp = []
    prtf = []
    prts = []
    grnd = []
    numr = []
    npro = []
    pred = []
    advb = []
    prep = []
    prcl = []
    conj = []
    intj = []
    page = urllib.request.Request('http://smartfiction.ru/prose/telegram/')
    with urllib.request.urlopen(page) as hpage:
        html = hpage.read().decode('utf-8')
    if re.search('<p>.*<hr />', html, re.DOTALL):
        text = re.search('<p>.*<hr />', html, re.DOTALL).group(0)
        text = re.sub(regTag, '', text)    
    for i in text.split():
        ana = morph.parse(i)
        first = ana[0]
        tag = first.normalized.tag
        form = first.normalized.normal_form
        if 'NOUN' in tag:
            n.append([form, tag])
        elif 'VERB' in tag or 'INFN' in tag:
            v.append([form, tag])
        elif 'ADJF' in tag:
            adjf.append([form, tag])
        elif 'ADJS' in tag:
            adjs.append([form, tag])
        elif 'COMP' in tag:
            comp.append([form, tag])
        elif 'PRTF' in tag:
            prtf.append([form, tag])
        elif 'PRTS' in tag:
            prts.append([form, tag])
        elif 'GRND' in tag:
            grnd.append([form, tag])
        elif 'NUMR' in tag:
            numr.append([form, tag])
        elif 'ADVB' in tag:
            advb.append([form, tag])
        elif 'INTJ' in tag:
            intj.append([form, tag])
        elif 'PREP' in tag:
            prep.append([form, tag])
        elif 'PRCL' in tag:
            prcl.append([form, tag])
        elif 'CONJ' in tag:
            conj.append([form, tag])
        elif 'NPRO' in tag:
            npro.append([form, tag])
    return n, v, adjf, adjs, comp, prtf, prts, grnd, numr, advb, npro, prep, conj, prcl, intj

def check(h, ltag, tag, pos, string):
    while h == 0:
        j = random.randrange(0, int(len(pos)))
        if ltag == pos[j][1]:
            try:
                gram = str(tag)
                new = morph.parse(pos[j][0])[0]
                for k in gram.split(','):
                    for r in k.split():
                        new = new.inflect({r})
                h = 1
                string = string + new.word + ' '
            except:
                h = 0
    return string

def smth(gtext):
    stuff = '[\.\?!"@№;%:?*_()-+=#$^&:;\'"><,/\|\\~`]'
    gtext = re.sub(stuff, '', gtext)
    n, v, adjf, adjs, comp, prtf, prts, grnd, numr, advb, npro, prep, conj, prcl, intj = words()
    string = ''
    for i in gtext.split():
        h = 0
        ana = morph.parse(i)
        first = ana[0]
        tag = first.tag
        ltag = first.normalized.tag
        print(ltag)
        if 'NOUN' in ltag:
            string = check(h, ltag, tag, n, string)
        if 'VERB' in ltag or 'INFN' in ltag:
            string = check(h, ltag, tag, v, string)
        if 'ADJF' in ltag:
            string = check(h, ltag, tag, adjf, string)
        if 'ADJS' in ltag:
            string = check(h, ltag, tag, adjs, string)
        if 'COMP' in ltag:
            string = check(h, ltag, tag, comp, string)
        if 'PRTF' in ltag:
            string = check(h, ltag, tag, prtf, string)
        if 'PRTS' in ltag:
            string = check(h, ltag, tag, prts, string)
        if 'NUMR' in ltag:
            string = check(h, ltag, tag, numr, string)
        if 'ADVB' in ltag:
            string = check(h, ltag, tag, advb, string)
        if 'INTJ' in ltag:
            string = check(h, ltag, tag, intj, string)
        if 'PREP' in ltag:
            string = check(h, ltag, tag, prep, string)
        if 'PRCL' in ltag:
            string = check(h, ltag, tag, prcl, string)
        if 'CONJ' in ltag:
            string = check(h, ltag, tag, conj, string)
        if 'NPRO' in ltag:
            string = check(h, ltag, tag, npro, string)
    return string

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.chat.id
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, с которым можно разговаривать.")

@bot.message_handler(content_types=['text'])
def send_len(message):
    user = message.chat.id
    
    gtext = message.text
    string = smth()
    bot.send_message(message.chat.id, string)

@bot.message_handler(content_types=['sticker'])
def send_welcome(message):
    user = message.chat.id
    bot.send_message(message.chat.id, "Красивый стикер!!!")

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

bot.polling(none_stop=True)
