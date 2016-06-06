import urllib
from bs4 import BeautifulSoup

global n
n=0
def gethtml(url):
    html=urllib.urlopen(url).read()
    soup=BeautifulSoup(html)
    return soup

def downloadImg(soup):
    global n
    imgs=soup.find_all('div',{'class':"photo_wrap"})
    for img in imgs:
        ImgTag=img.find('img')
        urllib.urlretrieve(ImgTag.get('src'),'./images/%s.jpg' %n)
        n+=1
        
print "Please, put in the album No."

albumnu=raw_input()
albumurl="http://www.douban.com/photos/album/"+str(albumnu)+"/?from=tag"

page=1
print "getting page"+str(page)
downloadImg(gethtml(albumurl))
page+=1

while True:
    try:
        print "getting page"+str(page)
        albumurl="http://www.douban.com/photos/album/"+str(albumnu)+"/?start="+str((page-1)*18)
        soup=gethtml(albumurl)
        if soup==[]:
            print "No more!"
            exit()
        else:
            downloadImg(soup)
            page+=1
    except:
        print "problem!"
        break

    
