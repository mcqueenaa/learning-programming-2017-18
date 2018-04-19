import urllib.request  
import json
import os
import shutil
import math
import re
import matplotlib.pyplot as plt

stuff = '[\.\?!"@№;%:?*_()-+=#$^&:;\'"><,/\|\\~`]'

def createdirs():
    os.mkdir('posts&comments')
    os.mkdir('posts&comments/posts/')
    os.mkdir('posts&comments/comments/')

def number(link):
    req = urllib.request.Request(link)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8', errors = 'ignore')
    data = json.loads(result)
    number = data['response']['count']
    return number

def datas(link):
    req = urllib.request.Request(link)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8', errors = 'ignore')
    data = json.loads(result)
    return data, result

def saveposts():
    p_ids = []
    f_ids = []
    length_t = []
    p_number = number('https://api.vk.com/method/wall.get?owner_id=-33374477&count=1&offset=0&v=5.73&access_token=32ce1a8532ce1a8532ce1a856232ac36aa332ce32ce1a85680fd3cd59e166579eb694c4')
    h = math.ceil(p_number/100)
    o = 0
    s = 100
    for i in range(0, h):
        if i <= 100: # ограничиваем выкачивание до 10100 постов
            link = 'https://api.vk.com/method/wall.get?owner_id=-33374477&count=100&offset=' + str(o) + '&v=5.73&access_token=32ce1a8532ce1a8532ce1a856232ac36aa332ce32ce1a85680fd3cd59e166579eb694c4'
            data, result = datas(link)
            if p_number <= 100:
                for k in range(0, p_number): 
                    text = data['response']['items'][k]['text']
                    with open ('posts&comments/posts/post ' + str(k + i*100 + 1) + '.txt', 'w', encoding = 'utf-8') as m:
                        m.write(text)
                    if re.search(stuff, text):
                        text = re.sub(stuff, "", text)
                    if text == '\s*':
                        length_t.append(0)
                    else:
                        words = text.split()
                        length_t.append(len(words))
                    p_id = data['response']['items'][k]['id']
                    p_ids.append(p_id) #сохранили id постов
                    f_id = str(data['response']['items'][k]['from_id'])
                    f_ids.append(f_id) #сохранили id пользователей
            else:
                for k in range(0, 100): 
                    text = data['response']['items'][k]['text']
                    with open ('posts&comments/posts/post ' + str(k + i*100 + 1) + '.txt', 'w', encoding = 'utf-8') as m:
                        m.write(text)
                    if re.search(stuff, text):
                        text = re.sub(stuff, "", text)
                    if text == '\s*':
                        length_t.append(0)
                    else:
                        words = text.split()
                        length_t.append(len(words))
                    p_id = data['response']['items'][k]['id']                
                    p_ids.append(p_id) #сохранили id постов
                    f_id = str(data['response']['items'][k]['from_id'])
                    f_ids.append(f_id) #сохранили id пользователей
                p_number = p_number - s
                o = o + 100
    return p_ids, length_t, f_ids
    
def savecomm():
    fcom_ids = []
    length_c = []
    eachcom_len = []
    c_numbers = []
    p_ids, length_t, f_ids = saveposts()
    s = 100
    o = 0
    comm = ''
    for i in range(len(p_ids)):
        n = 0
        p = 0
        link = 'https://api.vk.com/method/wall.getComments?owner_id=-33374477&post_id=' + str(p_ids[i]) + '&count=100&v=5.73&access_token=32ce1a8532ce1a8532ce1a856232ac36aa332ce32ce1a85680fd3cd59e166579eb694c4'
        c_number = number(link)
        c_numbers.append(c_number) 
        if c_number != 0:
            h = math.ceil(c_number/100)
            for j in range(0, h):
                link = 'https://api.vk.com/method/wall.getComments?owner_id=-33374477&post_id=' + str(p_ids[i]) + '&offset=' + str(o) + '&count=100&v=5.73&access_token=32ce1a8532ce1a8532ce1a856232ac36aa332ce32ce1a85680fd3cd59e166579eb694c4'
                data, result = datas(link)
                if c_number <= 100:
                    for k in range(0, c_number):
                        h = 0
                        allwords = data['response']['items'][k]['text']
                        fcom_id = str(data['response']['items'][k]['from_id'])
                        fcom_ids.append(fcom_id) #сохранили id пользователей
                        if re.search(stuff, allwords):
                            allwords = re.sub(stuff, "", allwords)
                        words = allwords.split()
                        if len(words) != 0:
                            h = len(words)
                            eachcom_len.append(h)
                        else:
                            eachcom_len.append(0)
                        n = n + len(words)
                        p = p + 1
                        comm = comm + data['response']['items'][k]['text'] + '\n'
                    with open ('posts&comments/comments/comments for post ' + str(i + 1) + '.txt', 'w', encoding = 'utf-8') as m:
                        m.write(comm)
                    length_c.append(n/p)
                else:
                    for k in range(0, 100):
                        h = 0
                        allwords = data['response']['items'][k]['text']
                        fcom_id = str(data['response']['items'][k]['from_id'])
                        fcom_ids.append(fcom_id) #сохранили id пользователей
                        if re.search(stuff, allwords):
                            allwords = re.sub(stuff, "", allwords)
                        words = allwords.split()
                        if len(words) != 0:
                            h = len(words)
                            eachcom_len.append(h)
                        else:
                            eachcom_len.append(0)
                        n = n + len(words)
                        p = p + 1
                        comm = comm + data['response']['items'][k]['text'] + '\n'
                    with open ('posts&comments/comments/comments for post ' + str(i + 1) + '.txt', 'w', encoding = 'utf-8') as m:
                        m.write(comm)
                    length_c.append(n/p)
                    с_number = с_number - s
                    o = o + 100
        else:
            with open ('posts&comments/comments/comments for post ' + str(i + 1) + '.txt', 'w', encoding = 'utf-8') as m:
                m.write('')
            length_c.append(n)
        comm = ''
    return length_c, eachcom_len, fcom_ids

def users(length, f_ids):
    towns = []
    ages = []
    for i in range(len(f_ids)):
        if f_ids[i].startswith( '-' ) == False:
            link = 'https://api.vk.com/method/users.get?user_ids=' + f_ids[i] + '&fields=bdate,city,home_town&v=5.73&access_token=32ce1a8532ce1a8532ce1a856232ac36aa332ce32ce1a85680fd3cd59e166579eb694c4'
            data, result = datas(link)
            if re.search('bdate', result):
                bdate = data['response'][0]['bdate']
                if re.search('\d+\.\d+.(\d+)', bdate):
                    year = re.search('\d+\.\d+.(\d+)', bdate).group(1)
                    age = 2018-int(year)
                    ages.append(age)
                else:
                    ages.append('')
            else:
                ages.append('')
            if re.search('home_town', result):
                city = data['response'][0]['home_town']
                towns.append(city)
            else:
                if re.search('city', result):
                    city = data['response'][0]['city']['title']
                    towns.append(city)
                else:
                    towns.append('')
        else:
            ages.append('')
            towns.append('')
    return ages, towns

def post_users():
    length = []
    p_ids, length, f_ids = saveposts()
    towns = []
    ages = []
    ages, towns = users(length, f_ids)
    return ages, towns, length

def comm_users():
    length = []
    length_c, length, f_ids = savecomm()
    towns = []
    ages = []
    ages, towns = users(length, f_ids)
    return ages, towns, length
    
def for_graph(x, y):
    arr = []
    lenn = []
    for a in range(len(x)):
        if (x[a] not in arr) and (x[a] != ''):
            arr.append(x[a])
            k = 1
            n = int(y[a])
            for f in range(len(x)):
                if (x[f] in arr) and (f != a):
                    k = k + 1
                    n = n + int(y[f])
            lenn.append(n/k)
    return(arr, lenn)

def for_post_comm_graph():
    d, len_p, g = saveposts()
    len_c, s, f = savecomm()
    x, y = for_graph(len_p, len_c)
    return x,y

def for_comm_age_graph():
    ages = []
    length = []
    ages, towns, length = comm_users()
    x, y = for_graph(ages, length)
    return x,y

def for_comm_towns_graph():
    towns = []
    length = []
    ages, towns, length = comm_users()
    x, y = for_graph(towns, length)
    return x,y

def for_post_age_graph():
    ages = []
    length = []
    ages, towns, length = post_users()
    x, y = for_graph(ages, length)
    return x,y

def for_post_towns_graph():
    towns = []
    length = []
    ages, towns, length = post_users()
    x, y = for_graph(towns, length)
    return x,y

def graph(x, y, title, xname, yname):
    plt.plot(x, y, color='orange')
    plt.scatter(x, y)
    plt.title(title)
    plt.ylabel(xname)
    plt.xlabel(yname)
    plt.show()

def post_comm_graph():
    x = []
    y = []
    x, y = for_post_comm_graph()
    for i in range(len(x)):
        for j in range(len(x)-1):
            if x[j] > x[j+1]:
                a = x[j]
                b = x[j+1]
                d = y[j]
                e = y[j+1]
                x[j] = b  
                x[j+1] = a
                y[j] = e
                y[j+1] = d
        for j in range(len(x)-1, 0, -1):
            if x[j-1] > x[j]:
                a = x[j]
                b = x[j-1]
                d = y[j]
                e = y[j-1]
                x[j] = b
                x[j-1] = a
                y[j] = e
                y[j-1] = d
    title = 'Соотношение средней длины поста и средней длины его комментария'
    xname = 'Средняя длина комментариев'
    yname = 'Длина поста'
    graph(x, y, title, xname, yname)

def comm_age_graph():
    x = []
    y = []
    x, y = for_comm_age_graph()
    for i in range(len(x)):
        for j in range(len(x)-1):
            if x[j] > x[j+1]:
                a = x[j]
                b = x[j+1]
                d = y[j]
                e = y[j+1]
                x[j] = b  
                x[j+1] = a
                y[j] = e
                y[j+1] = d
        for j in range(len(x)-1, 0, -1):
            if x[j-1] > x[j]:
                a = x[j]
                b = x[j-1]
                d = y[j]
                e = y[j-1]
                x[j] = b
                x[j-1] = a
                y[j] = e
                y[j-1] = d
    title = 'Соотношение средней длины комментария и возраста'
    xname = 'Длина комментария'
    yname = 'Возраст'
    graph(x, y, title, xname, yname)

def post_age_graph():
    x = []
    y = []
    x, y = for_post_age_graph()
    for i in range(len(x)):
        for j in range(len(x)-1):
            if x[j] > x[j+1]:
                a = x[j]
                b = x[j+1]
                d = y[j]
                e = y[j+1]
                x[j] = b  
                x[j+1] = a
                y[j] = e
                y[j+1] = d
        for j in range(len(x)-1, 0, -1):
            if x[j-1] > x[j]:
                a = x[j]
                b = x[j-1]
                d = y[j]
                e = y[j-1]
                x[j] = b
                x[j-1] = a
                y[j] = e
                y[j-1] = d
    title = 'Соотношение средней длины поста и возраста'
    xname = 'Длина поста'
    yname = 'Возраст'
    graph(x, y, title, xname, yname)

def comm_towns_graph():
    x = []
    y = []
    xnumb = []
    x, y = for_comm_towns_graph()
    for i in range(len(x)):
        xnumb.append(i)
    title = 'Соотношение средней длины комментария и города'
    xname = 'Длина комментария'
    yname = 'Город'
    plt.xticks(xnumb, x)
    graph(xnumb, y, title, xname, yname)

def post_towns_graph():
    x = []
    y = []
    xnumb = []
    x, y = for_post_towns_graph()
    for i in range(len(x)):
        xnumb.append(i)
    title = 'Соотношение средней длины поста и города'
    xname = 'Длина поста'
    yname = 'Город'
    plt.xticks(xnumb, x)
    graph(xnumb, y, title, xname, yname)

def all_graphs():
    post_comm_graph()
    comm_age_graph()
    comm_towns_graph()
    post_age_graph()
    post_towns_graph()

def main():
    createdirs()
    all_graphs()
    
if __name__ == '__main__':
    main()
    
