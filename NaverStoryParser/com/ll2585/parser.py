import sys
from bs4 import BeautifulSoup
import html2text
from urllib.request import urlopen
import types


#url="http://novel.naver.com/webnovel/detail.nhn?novelId=1&volumeNo=55&week=MON"
#page=urlopen(url)
#soup = BeautifulSoup(page.read())
def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, types.StringTypes):
            text += elem.strip()
        elif elem.name == 'p':
            text += '\n'
    return text

soup = BeautifulSoup(open('naver4.html', encoding="utf-8"))
#soup = BeautifulSoup(u'\xa0')
#temp=soup.findAll("div",{"id":"detail_view_container"})
#print(page.read().decode("utf8"))

#a_file = open('wtf.txt', encoding="utf-8")
for e in soup.find_all('div', attrs={'class':'detail_view_content ft15'}):
    spans = soup.find_all('span')
    for span in spans:
        span.decompose()
    print(e.get_text())

