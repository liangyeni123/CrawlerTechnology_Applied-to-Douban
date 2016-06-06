# -*- encoding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import re
class user():
    def __init__(self,name,FriendNames=[],FriendLinks=[],Friends={}):
        self.name=name
        self.FriendNames=FriendNames
        self.FriendLinks=FriendLinks
        self.Friends=Friends
    def addFriend(self,friendname,friendlink):
        self.FriendNames.append(friendname)
        self.FriendLinks.append(friendlink)
        self.Friends[friendname]=friendlink
    def showFriendNames(self):
        print self.name+"has following friends:"
        for n in self.FriendNames:
            print n
    def showFriendLinks(self):
        print self.name+"has following friend links:"
        for n in self.FriendLinks:
            print n

loginUrl = 'http://accounts.douban.com/login'
formData={
    "redir":"http://www.douban.com/contacts/list",
    #'form_email':'shen_jiabin@outlook.com',
    #'form_password':'63573112h'
    
}
formData['form_email']=raw_input('please, type your username:')
formData['form_password']=raw_input('Please, type your password:')
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
#cookiejar=cookielib.CookieJar()
#opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
#urllib2.install_opener(opener)
#result=urllib2.Request(loginUrl,data,headers)

r = requests.post(loginUrl,data=formData,headers=headers)
page = r.text
soup = BeautifulSoup(page,"html.parser")

if r.url!='http://www.douban.com/contacts/list':
    captchaAddr = soup.find('img',id='captcha_image')['src'] 
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captchaID = re.findall(reCaptchaID,page)
    urllib.urlretrieve(captchaAddr,"captcha.jpg")
    captcha = raw_input('please input the captcha:')
    formData['captcha-solution'] = captcha
    formData['captcha-id'] = captchaID
    r = requests.post(loginUrl,data=formData,headers=headers)
    page = r.text
    soup=BeautifulSoup(page,'html.parser')

Friend=soup.findAll('li',attrs={'class':'clearfix'})
Myself=user(formData['form_email'])
for friend in Friend:
    name=friend.find('h3').find('a').get_text()
    link=friend.find('a').get('href')
    Myself.addFriend(name,link)
Myself.showFriendNames()
Myself.showFriendLinks()
print Myself.Friends
for name in Myself.FriendNames:
    raw_url=Myself.Friends[name]
    url=raw_url+'contacts'
    print url
    formData['redir']=url
    r = requests.post(loginUrl,data=formData,headers=headers)
    page = r.text
    soup = BeautifulSoup(page,"html.parser")
    
    if r.url!=url:
        captchaAddr = soup.find('img',id='captcha_image')['src'] 
        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captchaID = re.findall(reCaptchaID,page)
        urllib.urlretrieve(captchaAddr,"captcha.jpg")
        captcha = raw_input('please input the captcha:')
        formData['captcha-solution'] = captcha
        formData['captcha-id'] = captchaID
        r = requests.post(loginUrl,data=formData,headers=headers)
        page = r.text
        soup=BeautifulSoup(page,'html.parser')
        
    #html=urllib.urlopen(url).read()
    #soup=BeautifulSoup(html,'html.parser')
    Friend=soup.findAll('dl',attrs={'class':'obu'})
    xxx=user(name)
    for friend in Friend:
        xxx.addFriend(friend.find('img').get('alt'),friend.find('a').get('href'))
    xxx.showFriendNames()
    
