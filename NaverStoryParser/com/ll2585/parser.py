import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen

#url="http://novel.naver.com/webnovel/detail.nhn?novelId=63068&volumeNo=1&week=THU"
#page=urlopen(url)
#soup = BeautifulSoup(page.read())

#soup = BeautifulSoup(open("naver4.html"))
soup = BeautifulSoup(u'\xa0')
#temp=soup.findAll("div",{"id":"detail_view_container"})
#print(page.read().decode("utf8"))

#a_file = open('wtf.txt', encoding="utf-8")
print(soup.encode('utf-8'))
#print (u'哈哈'.encode('gb2312'))