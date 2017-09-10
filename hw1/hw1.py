import urllib.request  
import re

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
req = urllib.request.Request('http://tuvpravda.ru/', headers={'User-Agent':user_agent})

with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')

retitle = re.compile('rel="bookmark">([^<]*?)</a>', flags= re.DOTALL)
titles = retitle.findall(html)
      
for t in titles:
    print(t)
