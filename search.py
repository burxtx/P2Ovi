# encoding: UTF-8

from postHandler import *
from data import *
from db import *
from create import *

from threading import Thread, Lock, stack_size
from Queue import Queue
from time import sleep

global gAuthToken
stack_size(32768*16)

def search_list(url, name):
    '''Navigate to Admin->Companies/users->search, search company/user name. Return the page'''
    # input company name and search. GET method
    
    
    # get encoded metadata, return params for GET or POST method
    def encode_metadata(name):
        metadata={'search':name,
                  'commit':'Search'}
#                  'utf8':'✓'}
        params = urllib.urlencode(metadata)
        return params
    
    
    params = encode_metadata(name)
    # http://publishtraining.ovi.com/companies?utf8=%E2%9C%93&search=nokia&commit=Searchs
    page = getPage(url+params)
    # list all
    try:
        if '/companies?' in url:
            page = getPage(BASE_URL + "/companies?search=%s&show_all=true"%(urllib.quote(name)))
        elif '/users?' in url:
            page = getPage(BASE_URL + "/users?search=%s&show_all=true"%(urllib.quote(name)))
    except:
        pass
    return page
    
def fetch_elems(page, elem_pattern):
    '''After search_list is executed, use regex to find the id, compname, username or useremail and return a list'''
    elems = re.findall(elem_pattern, page, re.DOTALL)
    elems = [i.strip() for i in elems]
    # 结果里面的数字包含逗号
    if elem_pattern == cid_pattern:
        elems=[i.replace(',', '') for i in elems]
    return elems

def match(column_list, csvdata):
    for ind, elem in enumerate(column_list):
        if elem == csvdata:
            return ind
        else:
            return -1

def further_match(disabled, company_list, company_name, uid_list):
    '''
    This function check 'disabled' and 'company name' in the search results of user page
    '''
    companyid = search_company(company_name)
    if disabled == 'true':
        print '[disabled] account is disabled within company "s".' % company_name
        raise
    else:
        ind = match(company_list, company_name)
        if ind > -1:
#            print 'company match & username match...'
            return uid_list[ind], companyid
        
def search_company(company_name):
    url = BASE_URL + '/companies?'
    page = search_list(url,company_name)
    writefile(page, 'search company in company page')
    elem_list = fetch_elems(page, ccname_pattern)
    cid_list = fetch_elems(page, cid_pattern)
    ind = match(elem_list, company_name)
    if ind > -1:
#        print 'match', company_name, cid_list[ind]
        return int(cid_list[ind])
    else:
#        print '[not found]', company_name
        return 0
    
def search_in_user_tab(elem):
    '''
    calling sequence
    1. elem = company name
    2. elem = user name
    3. elem = user email
    '''
    url = BASE_URL + '/users?'
    page = search_list(url, elem)
    writefile(page, 'search result %s' % elem)
    company_list = fetch_elems(page, ucname_pattern)
    user_list = fetch_elems(page, uname_pattern)
    uid_list = fetch_elems(page, uid_pattern)
    email_list = fetch_elems(page, uemail_pattern)
    disabled_list = fetch_elems(page, disabled_pattern)
    if len(company_list) == len(user_list) == len(uid_list) == len(email_list) == len(disabled_list):
        if len(company_list) == len(user_list) == len(uid_list) == len(email_list) == len(disabled_list) == 0:
            print '[info] no available account ...'
        return company_list, user_list, uid_list, email_list, disabled_list
    else:
        print '[error] search failed ...'
        
def verify_operation(username, companyname, email):
    userid, companyid = search_control(username, companyname, email)
    if userid == 0:
        if companyid == 0:
            # user[x] company[x] 
            print "[info] user and company do not exist; will create"
        else:
            # user[x] company[o]
            print '[warning] user name does not exist in registered company; Please get CP manager approval first before creating user'
    else:
        if companyid == 0:
            # user[o] company[x]
            print "[error] User name may already exists but does not match company. Skipping content"
        else:
            # user[o] company[o]
            print '[PSS Check] Double check that the above username and company are correct'
    return companyid, userid

def register_company_and_user(csvdata, username, companyname, email):
#    try:
#        gAuthToken = login(LOGIN_URL, LOGIN_METADATA, AUTHTOKEN_PATTERN)
#    except:
#        raise
    companyid = 0
    userid = 0
    
    try:
        userid, companyid = verify_operation(username, companyname, email)
    except:
        print '[info] bad search result found ...'
        return 
#    if userid == 0:
#        if companyid == 0:
#            companyid = register_company(gAuthToken, csvdata, isUpdate = False, companyid = None)
#            if companyid == 0:
#                print "[error] cannot register company name: " + csvdata["Company_Name"]
#            params = urllib.urlencode({ 
#                      'authenticity_token'                        : gAuthToken,
#                      "company_channel[channel_id]"               : 5,  # Ovi Store
#                      "commit"                                    : "Add"
#                      })
#            urllib2.urlopen(BASE_URL + "/companies/add_channel/%d" % companyid, params)
#            #and you mes set the legal checked to true
#            params = urllib.urlencode({ 
#                      'authenticity_token'                        : gAuthToken
#                      })
#            #http://publishtraining.ovi.com/companies/set_legal_checked/4145?legal_checked=true
#            urllib2.urlopen(BASE_URL + "/companies/set_legal_checked/%d?legal_checked=true" % companyid, params)
#
##            userid = register_user(gHTTPReq, gAuthToken, userinfo, companyid)
#            if userid == 0:
#                print "[error] cannot register user name: " + csvdata["username"]
#        else:
#            print '[WARNING] Company exists but user requires CP manager approval -- user selected yes so now creating user... '
##            userid = register_user(gHTTPReq, gAuthToken, userinfo, companyid)
#            if userid == 0:
#                print "[error] cannot create user name: ", username
#    else:
#        if companyid == 0:
#            # user[o] company[x]
#            print "creating company ", companyname
#            print "[error] user name: ", username, " already exists but does not match company. Skipping Content"
#            # <TODO> create a new company and move the user???
#            raise
#        
#        else:
#            # user[o] company[o]
#            print "user and company already exist"
#            foo = ""
#            while foo != 'n' and foo != 'u':
#                foo = raw_input('\n need company update?    Enter "u" or "n": ')
#                if foo == 'u':
#                    print "[info] start updating company & user... "
#                    #update companyinfo                                                      
#                    user_role_check = register_user(gAuthToken, csvdata, companyid, True, userid)
#                    if user_role_check != -1:
#                        print "[info] updating company..."
#                        register_company(gAuthToken, csvdata, True, companyid)
#                    else:
#                        print "#### skip company update###"
#                elif foo =='n':
#                    pass
#            pass
                    
def search_control(username, companyname, email):
    
    '''------------search company------------'''
    print '\tsearching company "%s" in user page ...' % companyname
    company_list, user_list, uid_list, email_list, disabled_list = search_in_user_tab(companyname)
    # match username
    ind = match(user_list, username)
    if ind > -1:
        disabled = disabled_list[ind]
        userid, companyid = further_match(disabled, company_list, companyname, uid_list)
        print '[OK] user "%s %s" available.' % (uid_list[ind], username)
        return userid, companyid

    # match email
    ind = match(email_list, email)
    if ind > -1:
        disabled = disabled_list[ind]
        userid, companyid = further_match(disabled, company_list, companyname, uid_list)
        print '[OK] email "%s %s" available.' % (uid_list[ind], email)
        return userid, companyid
#    print '[sorry] no available account when searching company name "%s" in user page...' % companyname
    
    # neither username nor email matches, may be need manual select.
#    if len(user_list) != 0 and len(uid_list) != 0 and len(company_list) != 0:
#        print '[warning] Need manual select...'
#        for ind,i in enumerate(company_list):
#            print '[info] Maybe found valid user, user name and user email and company name may be different to csv file \n################ - Results %s - ####################\n\tUser: %s \n\twith user id: %s\n\twith company: %s \n\twith email: %s \n[WARNING] UserName from csv is: %s \n[WARNING] CompanyName from csv is: %s \n[WARNING] Email from csv is: %s\n################ - Results %s - ####################\n' \
#            % (str(ind), user_list.encode("utf-8"), uid_list[ind], company_list[ind].encode("utf-8"), email_list[ind].encode('utf-8'), username.encode("utf-8"), companyname.encode("utf-8"), email.encode("utf-8"), str(ind))
#        optionlist=['u','c','e']
#        foo=''
#        while foo not in optionlist:
#            foo = raw_input('\nHow to process the appwiz? ("u" will do company update, "c" will create new company, "e" will escalate company)\nEnter "u" or "c" or "e": ')
#        if foo=="u":
#            RecordNum = raw_input('Please select a record to update: ')
#            while int(RecordNum)>=len(uid_list):
#                RecordNum = raw_input('Invalid Record Number, Please re enter: ')
#            print "[info] Will update company: %s -> %s" % (company_list[int(RecordNum)].encode("utf-8"), companyname.encode("utf-8"))
#            #update company
#            companyid = search_company(companyname)
#            userid = int(uid_list[int(RecordNum)])                                            
#            return userid, companyid
#        elif foo=="c":
#            print "[info] Will create new company: %s" % companyname.encode("utf-8")
#            return 0,0
#        elif foo=="e":
#            print "[info] Will escalate company: %s" % companyname.encode("utf-8")
#            return int(uid_list[0]),companyid

    '''------------search username------------'''
    print '\tsearching user "%s" in user page ...' % username
    company_list, user_list, uid_list, email_list, disabled_list = search_in_user_tab(username)
    # match username
    ind = match(user_list, username)
    if ind > -1:
        disabled = disabled_list[ind]
        userid, companyid = further_match(disabled, company_list, companyname, uid_list)
        print '[OK] user "%s %s" available.' % (uid_list[ind], username)
        return userid, companyid

    # match email
    ind = match(email_list, email)
    if ind > -1:
        disabled = disabled_list[ind]
        userid, companyid = further_match(disabled, company_list, companyname, uid_list)
        print '[OK] email "%s %s" available.' % (uid_list[ind], email)
        return userid, companyid
#    print '[sorry] no available account when searching user name "%s" in user page...' % username
    
    '''------------search email---------------'''
    print '\tsearching email "%s" in user page ...' % email  
    company_list, user_list, uid_list, email_list, disabled_list = search_in_user_tab(email)
    # match username
    ind = match(user_list, username)
    if ind > -1:
        disabled = disabled_list[ind]
        userid, companyid = further_match(disabled, company_list, companyname, uid_list)
        print '[OK] user "%s %s" available.' % (uid_list[ind], username)
        return userid, companyid
    
    # match email
    ind = match(email_list, email)
    if ind > -1:
        disabled = disabled_list[ind]
        userid, companyid = further_match(disabled, company_list, companyname, uid_list)
        print '[OK] email "%s %s" available.' % (uid_list[ind], email)
        return userid, companyid
#    print '[sorry] no available account when searching email "%s" in user page...' % email
    
    '''----------- maybe none exists ----------------'''
    print '[] will seprate "%s, s, s"' % (companyname, username, email)
    companyid = search_company(companyname)
    if companyid == 0:
        return 0, companyid
    else:
        raise
    
def search_appwizard(app, app_type, gAuthToken):
    params = urllib.urlencode({ 'authenticity_token':gAuthToken,
                                'filter[search]':  app.encode("utf-8"),#.split(u' (')[-2],
                                'filter[folder]':   '',
                                'filter[company_id]':   '',
                                'filter[content_type_id]' : '',
                                'filter[channel_id]' :  '',
                                'filter[qa_status]'  : '', 
                                'filter[ovi_state]' : '',
                                'filter[account_manager_id]'    : '',
                                'commit' :  'Submit' })
    page = getPage(BASE_URL + "/content_items/list", params)
    appidresult = re.findall('\(app wizard ([0-9]+)', page)
    appname = re.findall("Display: <strong>(.*)</strong>",page)
    contentid = re.findall('<a href="/content_items/show/([0-9]+)">', page)
    
    Found=False
    type=re.findall('a (.*)\n        in Ovi Store',page)
#    print type
    for i in type:
        if i=="Java application":
            i="Java"
        elif i=="WRT Widget":
            i="WRT"
        if i==app_type:
            Found=True
            break
        elif i!=app_type:
            Found=False

    print "[info] ##### search result #####"
    if appidresult==[]:
        print "app id Not Found!"
        
    else:
        print "app id: "
        appidresult=[i.encode("utf-8") for i in appidresult]
        print appidresult

    if appname==[]:
        print "app name Not Found!"
    else:
        print "app name:"
        appname=[i.encode("utf-8") for i in appname]
        for i in appname:
            print i.encode("utf-8")
            
    if contentid==[]:
        print "content id Not Found!"
    else:
        print "content id: "
        contentid=[i.encode("utf-8") for i in contentid]
        print contentid
    return (appidresult, appname, contentid, Found)

def search_contentid(contentname, gAuthToken):
    params = urllib.urlencode({ 'authenticity_token':gAuthToken,
                                'filter[search]':  contentname.encode("utf-8")[:50],#.split(u' (')[-2],
                                'filter[folder]':   '',
                                'filter[company_id]':   '',
                                'filter[content_type_id]' : '',
                                'filter[channel_id]' :  '',
                                'filter[qa_status]'  : '', 
                                'filter[ovi_state]' : '',
                                'filter[account_manager_id]'    : '',
                                'commit' :  'Submit' })
    page = getPage(BASE_URL + "/content_items/list", params)
    contentid = re.findall('/content_items/show/([0-9]+)', page)
    if len(contentid) > 0 :
        return int(contentid[0])
    return 0

def console():
    while not q.empty():
        r = q.get()
        # search company name in company page
        companyname = r['Company_Name']
        username = r['User_first_name']+'.'+r['User_last_name']
        email = r['User_email']
#        g_mutex.acquire()
        try:
            gAuthToken = login(LOGIN_URL, LOGIN_METADATA, AUTHTOKEN_PATTERN)
        except:
            sleep(10)
            continue
#        g_mutex.release()
        register_company_and_user(r, username, companyname, email)
#        try:
#            register_company_and_user(r, username, companyname, email)
#        except:
#            print '#######'
#            continue
        q.task_done()
    print '[info] ... task completes'
    return 
#        process_contents(r)
    
conn = sqlite3.connect('appwizard_db')
conn.text_factory = str
q = select_from_db('appwizard_table', conn)#('appwizard_db', 'appwizard_table')

if __name__ == "__main__":
#    conn = sqlite3.connect('appwizard_db')
#    conn.row_factory = sqlite3.Row
#    conn.text_factory = str
#    c = conn.cursor()
#    global g_mutex
#    g_mutex = Lock()
    for i in range(MAX_THREADS):
        t = Thread(target = console)
        t.setDaemon(True)
        t.start()
        sleep(10)
    q.join()
#    search_control()