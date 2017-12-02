from flask import Flask
from flask import url_for, render_template, request, redirect
import json
import re
lang = {}
towns = {}
gender = {}
##не все страницы на сайте открываются сразу (статистика, json) - сначала нужно хотя бы раз заполнить анкету
app = Flask(__name__)

@app.route('/')
def index_main():
    return render_template('q.html')

@app.route('/thanks')
def thanks():
    data = dict(request.args) 
    with open('results_data.json', "a", newline="") as file: 
        file.write(json.dumps(data, ensure_ascii = False))
    language = request.args['язык']
    town = request.args['город']
    g = request.args['пол']

    if g not in gender:
        gender[g] = '1'
    else:
        gender[g] = str(int(gender[g]) + 1)
    if language not in lang:
        lang[language] = '1'
    else:
        lang[language] = str(int(lang[language]) + 1)

    if town not in towns:
        towns[town] = '1'
    else:
        towns[town] = str(int(towns[town]) + 1)

    tchart = []
    lchart = []
    gchart = []
    for i in gender:
        g = [i, int(gender[i])]
        gchart.append(g)
    for i in towns:
        t = [i, int(towns[i])]
        tchart.append(t)
    for i in lang:
        l = [i, int(lang[i])]
        lchart.append(l)
    with open('languages.json', "w", newline="") as file:
        file.write(json.dumps(lchart, ensure_ascii = False))
    
    with open('towns.json', "w", newline="") as file:
        file.write(json.dumps(tchart, ensure_ascii = False))

    with open('genders.json', "w", newline="") as file:
        file.write(json.dumps(gchart, ensure_ascii = False))
    return render_template('thanks.html')

@app.route('/stats')
def stat():
    with open('languages.json', "r") as file: 
        lchstring = file.read()
    lchstring = re.sub(r'",', ':', lchstring)
    lchstring = re.sub(r'\[', '', lchstring)
    lchstring = re.sub(r']', '', lchstring)
    lchstring = re.sub(r'"', '', lchstring)
    languages = lchstring.split(',')
    
    with open('towns.json', "r") as file: 
        tchstring = file.read()
    tchstring = re.sub(r'",', ':', tchstring)
    tchstring = re.sub(r'\[', '', tchstring)
    tchstring = re.sub(r']', '', tchstring)
    tchstring = re.sub(r'"', '', tchstring)
    towns = tchstring.split(',')

    with open('genders.json', "r") as file: 
        genders = file.read()
    genders = re.sub(r'",', ':', genders)
    genders = re.sub(r'\[', '', genders)
    genders = re.sub(r']', '', genders)
    genders = re.sub(r'"', '', genders)
    gend = genders.split(',')
    return render_template('stats.html', languages = languages, towns = towns, genders = gend)


@app.route('/json')
def jsn():
    with open('results_data.json', "r") as file: 
        content = file.read() 
    return render_template('jsn.html', content = content)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results():
    resultik = []
    forms2 = []
    searched = request.args['search']
    with open('results_data.json', "r") as file: 
        content = file.read()
    forms = content.split('}')
    for i in forms:
        j = re.sub(r'(\[|]|"|{)', '', i)
        forms2.append(j)
    for j in forms2:
        if re.search(searched, j):
            resultik.append(j)
    return render_template('results.html', resultik = resultik) 

if __name__ == '__main__':
    app.run(debug=True)
