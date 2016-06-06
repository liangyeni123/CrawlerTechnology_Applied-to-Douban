# -*- encoding:utf-8 -*-
import urllib2,urllib
import re, os
from bs4 import BeautifulSoup

def crawl(url): 
   page = urllib2.urlopen(url) 
   contents = page.read() 
   soup = BeautifulSoup(contents,"lxml")
   try:
        os.makedirs('./MoviePictures')
   except OSError:
        if os.path.exists('./MoviePictures'):
            pass
        else:
            raise
   os.chdir('./MoviePictures')
    
   for tag in soup.find_all('div', {'class':"item"}):       
       m_order = int(tag.find('div', {'class':"pic"}).find('em').get_text())         
       m_name = tag.find('div',{'class':'info'}).span.get_text()         
       m_rating_score = float(tag.find('span',{'class':'rating_num'}).get_text())         
       urllib.urlretrieve(tag.find('img').get('src'),'./%s.jpg' %m_name)
       print("%s %s %s" % (m_order, m_name, m_rating_score))
       fo.write( str(m_order)+" "+m_name.encode('utf8')+" "+str(m_rating_score))
       fo.write('\n')
   os.chdir('../')  
    
if __name__ == '__main__':
    FirstPage='http://movie.douban.com/top250?format=text'
    fo=open('top250.txt','w')
    crawl(FirstPage)
    for i in range(1,10):
        Page='http://movie.douban.com/top250?start='+str(25*i)+'&filter='
        crawl(Page)
    fo.close()
