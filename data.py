# encoding: UTF-8
import codecs
import os
import shutil

MAX_THREADS=3

def writefile(page,filename):
    if os.path.exists('\debug') == False:
#        shutil.rmtree('\debug')
        os.mkdir('\debug')
    html = codecs.open('\debug\\' + filename + '.htm', 'w', 'utf-8')
    html.write(page)
    html.close()

USERNAME="app_wizard"
PASSWORD="changeme1"
#PASSWORD="ty$is!mi#e8"

##get authtoken
AUTHTOKEN_PATTERN='<input name="authenticity_token" type="hidden" value="(.*)" /></div>'

# login metadatas
LOGIN_METADATA={
    'login_user[login]':USERNAME,
    'login_user[password]':PASSWORD,
    'commit':'Login',
    'utf8':u'\u2731;'.encode('utf_8')
    }

# page url
BASE_URL="http://publishtraining.ovi.com"
#BASE_URL="https://publish.ovi.com"
LOGIN_URL=BASE_URL+"/login"

# Admin tab
COMP_URL='/companies'
USER_URL='/users'

# search company
COMP_S=COMP_URL+'?'# GET, params: commit: Search  search: gameloft utf8
# list all res = req.open(BASE_URL + "/users?search=%s&show_all=true"%(urllib.quote(companyinfo["companyname"].encode("utf-8"))))

'''
all patterns
'''
# company page id pattern
# company page company name pattern
# user page id pattern
# company name pattern
# user name pattern
# user email pattern
# user disabled pattern
#live system
cid_pattern = '<td class="id-column  numeric" >(.*?)</td>'
ccname_pattern = '(?s)<td class="name-column  sorted" >(.*?)</td>' 
uid_pattern = '/users/row/([0-9]+)\?_method=get'
ucname_pattern = '(?s)<td class="company-column " >(.*?)</td>'
uname_pattern = '(?s)<td class="login-column " >(.*?)</td>'
uemail_pattern = '(?s)<td class="email-column " >(.*?)</td>'
disabled_pattern = '(?s)<td class="disabled-column " >(.*?)</td>'

##training system
#cid_pattern = '<td class="id-column  sorted numeric" >(.*?)</td>'
#ccname_pattern = '<td class="name-column" >(.*?)</td>'
#uid_pattern = 'data-refresh="/users/row/([0-9]+)\?_method=get'
#ucname_pattern = '<td class="company-column " >(.*?)</td>'
#uname_pattern = '<td class="login-column " >(.*?)</td>'
#uemail_pattern = '<td class="email-column " >(.*?)</td>'
#disabled_pattern = '<td class="disabled-column " >(.*?)</td>'

# content tab
