# -*- encoding:utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import re
import time

        
def login(user):
    '''
    This function is used to login the douban and redireted to the contact list page.
    return the page in beautifulsoup formed.
    '''
    loginUrl = 'http://accounts.douban.com/login'
    formData={}
    formData['redir']='https://www.douban.com/people/'+str(user)+'/contacts'
    formData['form_email']=raw_input('please, type your username:')
    formData['form_password']=raw_input('Please, type your password:')
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
        'Referer':'http://accounts.douban.com'}
    s=requests.Session()
    r = s.post(loginUrl,data=formData,headers=headers)
    page = r.content
    soup = BeautifulSoup(page,"html.parser")
    # check if a captcha is needed.
    if r.url!='https://www.douban.com/people/'+str(user)+'/contacts':
        captchaAddr = soup.find('img',id='captcha_image')['src'] 
        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captchaID = re.findall(reCaptchaID,page)
        urllib.urlretrieve(captchaAddr,"captcha.jpg")
        captcha = raw_input('please input the captcha:')
        formData['captcha-solution'] = captcha
        formData['captcha-id'] = captchaID
       # r = s.post(loginUrl,data=formData,headers=headers)
    return loginUrl,formData,headers
        
def WordCheck(name):
    '''
    This function check the words that cannnot be used as a file or folder name and replace it.
    '''
    name=name.replace(' ','')
    name=name.replace('\n','')
    name=name.replace('/','')
    name=name.replace(':','')
    name=name.replace('?','')
    name=name.replace('\\','')
    name=name.replace('|','')
    name=name.replace('>','')
    name=name.replace('<','')
    name=name.replace('"','')
    name=name.replace('*','')
    return name
def convert(loginUrl,formData,headers,user):
    s=requests.Session()
    r = s.post(loginUrl,data=formData,headers=headers)
    page = r.content
    soup=BeautifulSoup(page,'html.parser')
    if r.url!=('https://www.douban.com/people/'+str(user)+'/contacts' and 'https://www.douban.com/contacts/list'):
        captchaAddr = soup.find('img',id='captcha_image')['src'] 
        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captchaID = re.findall(reCaptchaID,page)
        urllib.urlretrieve(captchaAddr,"captcha.jpg")
        captcha = raw_input('please input the captcha:')
        formData['captcha-solution'] = captcha
        formData['captcha-id'] = captchaID
        r = s.post(loginUrl,data=formData,headers=headers)
    return r

def FindFriends(r,user):
    '''
    This function serach the friends of the given user.
    And build a folder to store the images of friends.
    And a text to store friends
    '''
    page = r.content
    soup=BeautifulSoup(page,'html.parser')
    print r.url
    if r.url=='https://www.douban.com/contacts/list':
        myself=1
    else:
        myself=0
    if myself==1:
        Friends_list=soup.findAll('li',{'class':'clearfix'})
    else:
        Friends_list=soup.findAll('dl',{'class':'obu'})
    name=user
    print name
    print Friends_list
    name=WordCheck(name)
    try:
        os.makedirs('./'+name)
    except OSError:
        if os.path.exists('./'+name):
            pass
        else:
            raise
    os.chdir('./'+name)
    fo_name=open(name.encode('utf8')+'.txt','w')
    fo_name.write('Friends List:\n')
    fo_address=open(name.encode('utf8')+'address.txt','w')
    FriendsLinks={} #store the links of friends
    FriendsNames=[]
    for friend in Friends_list:
        try:
            address=friend.find('span',{'class':'loc'}).get_text()
        except:
            address=''
        print address
        address=address.replace("live in:".decode('utf8'),'')
        friend_name=friend.find('img').get('alt')
        friend_name=WordCheck(friend_name)
        fo_name.write(friend_name.encode('utf8')+';')
        fo_address.write(friend_name.encode('utf8')+'from'+address.encode('utf8')+';')
        urllib.urlretrieve(friend.find('img').get('src'),'./%s.jpg' %friend_name)
        FriendsLinks[friend_name]=friend.find('a').get('href')
        FriendsNames.append(friend_name)
    fo_name.close()
    fo_address.close()
    '''
    This part download the Movies and Books of friends.
    Store the images of the Moives and Bools in two folder.
    '''
    for friend_name in FriendsNames:
        url=FriendsLinks[friend_name]
        print url
        html=urllib.urlopen(url).read()
        soup=BeautifulSoup(html,'lxml')
        try:
            os.makedirs('./'+friend_name)
        except OSError:
            if os.path.exists('./'+friend_name):
                pass
            else:
                raise
        os.chdir('./'+friend_name)
        #books
        acquire=1
        try:
            all_book=soup.find('div',{'id':'book'}).find('h2').findAll('a')
        except:
            acquire=0
        try:
            os.makedirs('./books')
        except OSError:
            if os.path.exists('./books'):
                pass
            else:
                raise
        os.chdir('./books')
        fo_bookname=open('books.txt','w')
        if acquire==1:
            for book in all_book:
                html=urllib.urlopen(book.get('href')).read()
                book_soup=BeautifulSoup(html,'lxml')
                book_imgs=book_soup.findAll('li',{'class':'subject-item'})
                for book_im in book_imgs:
                    name=book_im.find('h2').find('a').get_text()
                    name=WordCheck(name)
                    print name
                    fo_bookname.write(name.encode('utf8')+';')
                    if name!='None':
                        urllib.urlretrieve(book_im.find('img').get('src'),'./%s.jpg' %name)
                    else:
                        name=book_im.find('h2').find('a').get('title')
                        urllib.urlretrieve(book_im.find('img').get('src'),'./%s.jpg' %name)
        fo_bookname.close()
        os.chdir('../')   
        #movie
        acquire=1
        try:
            all_movie=soup.find('div',{'id':'movie'}).find('h2').findAll('a')
        except:
            acquire=0
        try:
            os.makedirs('./movies')
        except OSError:
            if os.path.exists('./movies'):
                pass
            else:
                raise
        os.chdir('./movies')
        fo_moviename=open('movies.txt','w')
        if acquire==1:
            for movie in all_movie:
                html=urllib.urlopen(movie.get('href')).read()
                movie_soup=BeautifulSoup(html,'lxml')  
                movie_imgs=movie_soup.findAll('div',{'class':'item'})
                for movie_im in movie_imgs:
                    name=movie_im.find('li',{'class':'title'}).find('a').get_text()
                    name=WordCheck(name)
                    print name
                    fo_moviename.write(name.encode('utf8')+';')
                    if name!='None':
                        urllib.urlretrieve(movie_im.find('img').get('src'),'./%s.jpg' %name)
                    else:
                        name=movie_im.find('li',{'class':'title'}).find('a').get('title')
                        urllib.urlretrieve(movie_im.find('img').get('src'),'./%s.jpg' %name)
        fo_moviename.close()
        os.chdir('../')
        os.chdir('../')
    os.chdir('../')
    return FriendsNames, FriendsLinks
    
def TestCrawl():
    user='liangyeni'
    loginUrl,formData,headers=login(user)
    FriendsNames, FriendsLinks=FindFriends(convert(loginUrl,formData,headers,user),user)
    for friend_name in FriendsNames:
        a=FriendsLinks[friend_name]
        u=a[30:a.find("/",30)]
        formData['redir']='https://www.douban.com/people/'+str(u)+'/contacts'
        print formData
        m,n=FindFriends(convert(loginUrl,formData,headers,u),u)
        
if __name__ == '__main__':
    TestCrawl()
