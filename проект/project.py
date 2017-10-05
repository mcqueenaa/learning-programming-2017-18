import urllib.request  
import re
import os
import shutil
#mystem в одной папке с программой

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
sections = ['obshchestvo', 'politika', 'kultura', 'proishestviya', 'ekonomika', 'sport', 'zhkkh', 'ot-redaktsii', '9maya'] 
regSpace = re.compile('\s{2,}', re.DOTALL)
regTag = re.compile('<.*?>', re.DOTALL)
regText = re.compile('<div class="itemIntroText">.*?<div class="itemFullText">.*?<div class="itemContentFooter">', re.DOTALL)
regAuth = re.compile(r'<meta name="author" content="(.*?)" />', re.DOTALL)
regTitle = re.compile('<meta property="og:title" content="(.*?)\| ЗОРИ ПЛЮС', re.DOTALL)
regDate = re.compile('<time data-time="(.*?) .*?">', re.DOTALL)
regTopic = re.compile('<!-- Item category name -->.*?news.*?>(.*?)</a>', re.DOTALL)
numbers = []
for i in range(6319, 9042):
    numbers.append(i)
commonUrl = 'http://dobryanka.net/news/'

def metadata(pageUrl):
    html = download_html(pageUrl)
    Author = get_author(pageUrl)
    Title = re.search(regTitle, html).group(1)
    Date = get_сdate(pageUrl)
    Topic = get_topic(pageUrl)
    year = get_year(pageUrl)
    month = get_month(pageUrl)
    Path = 'newspaper/' + year + '/' + month + '/' + Topic
    with open ('newspaper/metadata.csv', 'a', encoding = 'utf-8') as m:
        m.write(Path + '; ' + Author + '; ; ; ' + Title + ';  ' + Date + '; публицистика; ; ; ' + Topic + '; ; нейтральный; н-возраст ; н-уровень; городская; ' + pageUrl + '; ЗОРИ ПЛЮС; ; ' + year + '; газета; Россия; Добрянка; ru \n')

def get_topic(pageUrl):
    html = download_html(pageUrl)
    if html != 0:
        if re.search(regTopic, html):
            Topic = re.search(regTopic, html).group(1)
        else:
            Topic = 'not found'
    return Topic

def get_author(pageUrl):
    html = download_html(pageUrl)
    if html != 0:
        if re.search(regAuth, html):
            author = re.search(regAuth, html).group(1)
        else:
            author = 'Noname'
    return author

def get_сdate(pageUrl):
    html = download_html(pageUrl)
    if html != 0:
        if re.search(regDate, html).group(1):
            date = re.search(regDate, html).group(1)
            date = re.sub('-', '.', date)
        else:
            date = 'not found'
    return date

def get_year(pageUrl):
    Date = get_сdate(pageUrl)
    year = re.search(r'(\d{4})\.\d{2}\.\d{2}', Date).group(1)
    return(year)

def get_month(pageUrl):
    Date = get_сdate(pageUrl)
    month = re.search(r'\d{4}\.(\d{2})\.\d{2}', Date).group(1)
    return(month)

def get_header(pageUrl):
    html = download_html(pageUrl)
    if html != 0:
        header = re.search(regTitle, html).group(1)
        header = re.sub(r'\\|/|\||\*|\?|:|"|<|>', '', header)
        return(header)

def download_html(pageUrl):
    try:
        page = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
        with urllib.request.urlopen(page) as hpage:
            html = hpage.read().decode('utf-8')
        return html
    except:
        print('there\'s no such page', pageUrl)
        html = 0
        return html

def download_text(pageUrl):
        html = download_html(pageUrl)
        if html != 0:
            if re.search(regText, html):
                text = re.search(regText, html).group(0)
                text = regSpace.sub(" ", text)
                text = regTag.sub("", text)
            else:
                text = 0
            return text

def mystemer(yeardir, monthdir, filename):
    input_txt = os.path.join('newspaper', 'plain', yeardir, monthdir, filename + '.txt ')
    output_txt = os.path.join('newspaper', 'mystem-plain', yeardir, monthdir, filename + '.txt')
    output_xml = os.path.join('newspaper', 'mystem-xml', yeardir, monthdir, filename + '.xml')
    os.system('mystem.exe ' + '-di ' + input_txt + output_txt)
    os.system('mystem.exe ' + '-di ' + input_txt + output_xml)
    
def smth():
    os.mkdir('newspaper')
    os.mkdir('newspaper/plain/')
    os.mkdir('newspaper/mystem-plain/')
    os.mkdir('newspaper/mystem-xml/')
    with open ('newspaper/metadata.csv', 'w', encoding = 'utf-8') as m:
        m.write('path; author; sex; birthday; header; created; sphere; genre_fi; type; topic; chronotop; style; audience_age; audience_level; audience_size; publication; publisher; publ_year; medium; country; region; language; source \n')
    #csv открывает с нормальной кодировкой только в notepad
    for section in sections:
        for i in numbers:
            pageUrl = commonUrl + section + '/item/' + str(i)
            html = download_html(pageUrl)
            if html != 0:                
                text = download_text(pageUrl)
                if text != 0: 
                    print('I am on the page', i)
                    yeardir = get_year(pageUrl)
                    monthdir = get_month(pageUrl)
                    header = get_header(pageUrl)
                    date = get_сdate(pageUrl)
                    author = get_author(pageUrl)
                    topic = get_topic(pageUrl)
                    metadata(pageUrl)
                    if os.path.exists('newspaper/plain/' + yeardir) == False:
                        os.mkdir('newspaper/plain/' + yeardir)
                        os.mkdir('newspaper/mystem-plain/' + yeardir)
                        os.mkdir('newspaper/mystem-xml/' + yeardir)
                        if os.path.exists('newspaper/plain/' + yeardir + '/' + monthdir) == False:
                            os.mkdir('newspaper/plain/' + yeardir + '/' + monthdir)
                            os.mkdir('newspaper/mystem-plain/' + yeardir + '/' + monthdir)
                            os.mkdir('newspaper/mystem-xml/' + yeardir + '/' + monthdir)
                    else:
                        if os.path.exists('newspaper/plain/' + yeardir + '/' + monthdir) == False:
                            os.mkdir('newspaper/plain/' + yeardir + '/' + monthdir)
                            os.mkdir('newspaper/mystem-plain/' + yeardir + '/' + monthdir)
                            os.mkdir('newspaper/mystem-xml/' + yeardir + '/' + monthdir)
                    filename = 'article' + str(i)
                    with open ('newspaper/plain/' + yeardir + '/' + monthdir + '/' + filename + '.txt', 'w', encoding = 'utf-8') as t:
                        t.write('@ ' + author + '\n@ ' + header + '\n@ ' + date + '\n@ ' + topic + '\n@ ' + pageUrl + '\n')
                    with open ('newspaper/plain/' + yeardir + '/' + monthdir + '/' + filename + '.txt', 'a', encoding = 'utf-8') as t:
                        t.write(text)
                    mystemer(yeardir, monthdir, filename)

smth()

