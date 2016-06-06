import urllib2

url='http://www.douban.com/photos/album/128307752/?from=tag'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
req = urllib2.Request(url,headers = headers)
response = urllib2.urlopen(req)
page = response.read()
print page
