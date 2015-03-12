#encoding:UTF-8

import re
import urllib
import urllib2
import cookielib
import MultipartPostHandler
from data import *
from time import sleep

#def getAuthToken(URL,pattern):
#    authtoken=findString(URL,pattern)[0] 
#    return authtoken

def construct_metadata(URL,metadata,pattern):
    """construct the metadata, return a complete metadata dictionary(or tuple, not implemented yet)"""
    metadata['authenticity_token']=findString(URL,pattern)[0]
    return metadata, metadata['authenticity_token']

def getParams(metadata):
    params=urllib.urlencode(metadata)
    return params

def getReq(URL):
    cjar = cookielib.CookieJar()
    if URL[0:5]=="https":
        req=urllib2.build_opener(
                                 urllib2.HTTPCookieProcessor(cjar),
#                                 urllib2.ProxyHandler({"https":"https://10.57.49.104:"}), 
                                 urllib2.HTTPSHandler(),
                                 MultipartPostHandler.MultipartPostHandler
                                 )
    elif URL[0:5]=="http:":
        req=urllib2.build_opener(
                                 urllib2.HTTPCookieProcessor(cjar),
#                                 urllib2.ProxyHandler({"http":"http://10.57.49.104:"}),
                                 urllib2.HTTPBasicAuthHandler(),
                                 MultipartPostHandler.MultipartPostHandler
                                 )
#    req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15 ( .NET CLR 3.0.4506.2152)')]
    urllib2.install_opener(req)
    
#
#    headers = {
#               'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
#               }


def getPage(URL, metadata=None):
#    if metadata is None:
#        try:
#            res=urllib2.urlopen(URL)
#        except:
#            print "[warning] post/get page failed"
#    else:
#        try:
#            res=urllib2.urlopen(URL, getParams(metadata))
#        except:
#            res=urllib2.urlopen(BASE_URL+"/companies")
#    req=getReq(URL)

    try:
        if metadata is None:
            res=urllib2.urlopen(URL)
        else:
            res=urllib2.urlopen(URL, getParams(metadata))
        if res.code == 500:
            getPage(URL, metadata=None)
    except urllib2.HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        raise urllib2.HTTPError
    except urllib2.URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        raise urllib2.HTTPError
    page=res.read()
    writefile(page,'debug login')
    return page

def findString(URL,pattern):
    """find matched 'pattern' in the 'url' web page, return a list object"""
    
    s=re.findall(pattern, getPage(URL))
    print s
    return s
    
def login(URL,metadata,pattern):
    getReq(URL)
    metadata, authtoken=construct_metadata(URL,metadata,pattern)
    getPage(URL,metadata)
    print "[OK] Already login"
    return authtoken

def main():
    # login p2ovi
    try:
        authtoken = login(LOGIN_URL, LOGIN_METADATA, AUTHTOKEN_PATTERN)
        print "[info] Already login"
        
    except:
        print "[warning] Login failed"
    
if __name__=='__main__': 
    main()
