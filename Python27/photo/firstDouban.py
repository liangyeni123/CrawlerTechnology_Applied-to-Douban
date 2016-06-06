import urllib
from bs4 import BeautifulSoup

n=1
link_list=[]
raw_url='http://www.douban.com/tag/%E6%97%A5%E6%9C%AC%E6%96%99%E7%90%86/?source=search'
html=urllib.urlopen(raw_url).read()
soup=BeautifulSoup(html,'lxml')
x=soup.find_all('div',{'class':'album-item'})
for links in x:
    link_list.append(links.a['href'])
    print links.a['href']
for imgs in x:
    img_list=imgs.find_all('img')
    for img in img_list:
        urllib.urlretrieve(img.get('src'),'./images/%s.jpg' %n)
        n+=1
for url in link_list:
    html=urllib.urlopen(url).read()
    soup=BeautifulSoup(html,'lxml')
    x=soup.find('div',{'class':"photolst clearfix"})
    imgs=x.find_all('img')
    for img in imgs:
        urllib.urlretrieve(img.get('src'),'./images/%s.jpg' %n)
        n+=1
