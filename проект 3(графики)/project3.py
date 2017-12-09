import matplotlib.pyplot as plt
import re
import urllib.request  

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
repalabra = re.compile('<ul><li><b>(\w*?)</b>(.*?)(<dd><i>(.*?)</i>(\w*?)</dd>)*</dl>', re.DOTALL)
regpofs = re.compile('<i>(.*?)</i>', re.DOTALL)
reword = re.compile('<span id="(.*?)">', re.DOTALL)
reblock = re.compile('<span class="mw-headline" id="(\w)">(.*?)</span></h3>(.*?)<h3>', re.DOTALL)
reblockZ = re.compile('<span class="mw-headline" id="Z">(.*?)</span></h3>(.*?)<h2>', re.DOTALL)

def download_html():
    page = urllib.request.Request('http://wiki.dothraki.org/Vocabulary', headers={'User-Agent':user_agent})
    with urllib.request.urlopen(page) as hpage:
        html = hpage.read().decode('utf-8')
    return html

def countletters():
    html = download_html()
    letters = {}
    for i in re.findall(reblock, html):
        letters[i[0]]= '0'
        for k in re.findall(reword, i[2]):
            letters[i[0]] = str(int(letters[i[0]]) + 1)
    letters['Z']= '0'
    for i in re.findall(reblockZ, html):
        for k in re.findall(reword, i[1]):
            letters['Z'] = str(int(letters['Z']) + 1)
    return letters

def partsofspeech():
    pofspeech = {'adjectives': '0', 'adverbs': '0', 'verbs': '0', 'conjunctions': '0', 'determiners': '0', 'interjections': '0', 'nouns': '0',
                 'numerals': '0', 'pronouns': '0', 'prepositions': '0', 'proper nouns': '0'}
    html = download_html()
    words = re.findall(repalabra, html)
    for i in words:
        for k in re.findall(regpofs, i[1]):
            if k == 'ni.' or k == 'na.' or k == 'n.' or k == 'np.':
                pofspeech['nouns'] = str(int(pofspeech['nouns']) + 1)
            if k == 'adj.':
                pofspeech['adjectives'] = str(int(pofspeech['adjectives']) + 1)
            if k == 'adv.':
                pofspeech['adverbs'] = str(int(pofspeech['adverbs']) + 1)
            if k == 'v. aux.' or k == 'v.' or k == 'vin.' or k == 'vtr.':
                pofspeech['verbs'] = str(int(pofspeech['verbs']) + 1)
            if k == 'conj.':
                pofspeech['conjunctions'] = str(int(pofspeech['conjunctions']) + 1)
            if k == 'det.':
                pofspeech['determiners'] = str(int(pofspeech['determiners']) + 1)
            if k == 'intj.':
                pofspeech['interjections'] = str(int(pofspeech['interjections']) + 1)
            if k == 'num.':
                pofspeech['numerals'] = str(int(pofspeech['numerals']) + 1)
            if k == 'pn.':
                pofspeech['pronouns'] = str(int(pofspeech['pronouns']) + 1)
            if k == 'prep.':
                pofspeech['prepositions'] = str(int(pofspeech['prepositions']) + 1)
            if k == 'prop. n.':
                pofspeech['proper nouns'] = str(int(pofspeech['proper nouns']) + 1)
    return pofspeech

def graphs():
    dictlet = countletters()
    pofspeech = partsofspeech()
    letters = []
    lnumber = []
    pofsp = []
    pnumber = []
    for i in dictlet:
        letters.append(i) 
        lnumber.append(int(dictlet[i]))
    for k in pofspeech:
        pofsp.append(k) 
        pnumber.append(int(pofspeech[k]))
    Xl = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    Xp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    Yl = lnumber
    Yp = pnumber

    ###графики показываются не вместе, а друг за другом. Если закрыть первый - откроется второй.
    plt.xticks(Xl, letters)
    plt.bar(Xl, Yl, color='plum')
    plt.title("Количество слов для каждой буквы дотракийского языка")
    plt.show()

    plt.xticks(Xp, pofsp)
    plt.bar(Xp, Yp, color='orange')
    plt.title("Количество слов каждой части речи")
    plt.show()

def main():
    graphs()

if __name__ == '__main__':
    main()









                
