# encoding: UTF-8
from postHandler import *
from search import *
import urllib2
import random
import string
def register_company(gAuthToken, args, isUpdate = False, companyid = None):

    def getOptionList():
        page = getPage(BASE_URL + "/companies/new?_method=get&adapter=_list_inline_adapter")
        return re.findall('<option value="([0-9]+)">(.*)</option>', page)
        
    def lookup_id(list, key):
        for i in list:
            if i[1] == key:
                return i[0] # i[0] is id
        print "[Error] cannot find '%s' in the register company lookup table" % key
        # if not found raise error
        raise 

    def lookupCountry_id(list, key):
        countryAbbKeyList = ['AB',          'AF',           'AL',       'DZ',       'AS',               'AD',       'AO',       'AI',           'AG',                   'AR',           'AM',       'AW',       'AU',           'AT',       'AZ',           'BS',       'BH',       'BD',           'BB',           'BY',       'BE',       'BZ',       'BJ',       'BM',       'BT',       'BO',       'BA',                       'BW',           'BR',       'VG',                       'BN',                   'BG',           'BF',               'BI',       'KH',           'CM',           'CA',       'CV',           'KY',               'CF',                           'TD',       'CL',       'CN',       'CO',           'KM',       'CK',               'CR',           'CI',               'HR',       'CU',       'CY',       'CZ',               'CD',                                   'DK',       'DJ',           'DM',           'DO',                   'TL',           'EC',       'EG',       'SV',           'GQ',                   'ER',       'EE',       'ET',           'FK',                   'FO',               'FJ',       'FI',       'FR',       'GF',               'PF',                   'GA',       'GM',       'GE',       'DE',       'GH',       'GI',           'GR',       'GL',           'GD',       'GP',                           'GU',       'GT',           'GN',       'GW',               'GY',       'HT',       'HN',           'HK',           'HU',       'IS',       'IN',       'ID',           'IR',       'IQ',       'IE',       'IL',       'IT',       'JM',       'JP',       'JO',       'KZ',           'KE',       'KI',           'KW',       'KG',           'LA',                           'LV',       'LB',       'LS',       'LR',       'LY',                       'LI',               'LT',           'LU',           'MO',       'MK',           'MG',           'MW',       'MY',           'MV',           'ML',       'MT',       'MH',                   'MR',           'MU',           'MX',       'FM',           'MD',       'MC',       'MN',           'ME',           'MS',           'MA',       'MZ',           'MM',               'NA',       'NR',       'NP',       'NL',           'AN',                       'NC',               'NZ',           'NI',           'NE',       'NG',       'MP',                           'KR',           'NO',       'OM',       'PK',           'PW',       'PS',           'PA',       'PG',                   'PY',           'PE',       'PH',           'PL',       'PT',           'PR',           'QA',       'CG',                       'RE',       'RO',       'RU',                   'RW',       'KN',                       'LC',           'PM',                           'VC',                                   'WS',       'SM',           'ST',                       'SA',               'SN',       'RS',       'SC',           'SL',               'SG',           'SK',           'SI',           'SB',               'SO',       'ZA',               'KP',               'ES',       'SP',       'LK',           'SD',       'SR',           'SZ',           'SE',       'CH',           'SY',                       'TW',       'TJ',           'TZ',           'TH',           'TG',       'TO',       'TT',                   'TN',       'TR',       'TM',               'TC',                           'UG',       'UA',       'AE',                       'GB',               'US',                           'VI',                               'UY',       'UZ',           'VU',       'VA',                   'VE',           'VN',       'WF',                   'YE',       'ZM',       'ZW']
        countryList =       [u'Abkhazia',   u'Afghanistan', u'Albania', u'Algeria', u'American Samoa',  u'Andorra', u'Angola',  u'Anguilla',    u'Antigua and Barbuda', u'Argentina',   u'Armenia', u'Aruba',   u'Australia',   u'Austria', u'Azerbaijan',  u'Bahamas', u'Bahrain', u'Bangladesh',  u'Barbados',    u'Belarus', u'Belgium', u'Belize',  u'Benin',   u'Bermuda', u'Bhutan',  u'Bolivia', u'Bosnia and Herzegovina',  u'Botswana',    u'Brazil',  u'British Virgin Islands',  u'Brunei Darussalam',   u'Bulgaria',    u'Burkina Faso',    u'Burundi', u'Cambodia',    u'Cameroon',    u'Canada',  u'Cape Verde',  u'Cayman Islands',  u'Central African Republic',    u'Chad',    u'Chile',   u'China',   u'Colombia',    u'Comoros', u'Cook Islands',    u'Costa Rica',  u'Côte dIvoire',    u'Croatia', u'Cuba',    u'Cyprus',  u'Czech Republic',  u'Democratic Republic of the Congo',    u'Denmark', u'Dijbouti',    u'Dominica',    u'Dominican Republic',  u'East Timor',  u'Ecuador', u'Egypt',   u'El Salvador', u'Equatorial Guinea',   u'Eritrea', u'Estonia', u'Ethiopia',    u'Falkland Islands',    u'Faroe Islands',   u'Fiji',    u'Finland', u'France',  u'French Guiana',   u'French Polynesia',    u'Gabon',   u'Gambia',  u'Georgia', u'Germany', u'Ghana',   u'Gibraltar',   u'Greece',  u'Greenland',   u'Grenada', u'Guadeloupe and Martinique',   u'Guam',    u'Guatemala',   u'Guinea',  u'Guinea-Bissau',   u'Guyana',  u'Haiti',   u'Honduras',    u'Hong Kong',   u'Hungary', u'Iceland', u'India',   u'Indonesia',   u'Iran',    u'Iraq',    u'Ireland', u'Israel',  u'Italy',   u'Jamaica', u'Japan',   u'Jordan',  u'Kazakhstan',  u'Kenya',   u'Kiribati',    u'Kuwait',  u'Kyrgyzstan',  u'Lao Peoples Democratic Rep.', u'Latvia',  u'Lebanon', u'Lesotho', u'Liberia', u'Libyan Arab Jamahiriya',  u'Liechtenstein',   u'Lithuania',   u'Luxembourg',  u'Macau',   u'Macedonia',   u'Madagascar',  u'Malawi',  u'Malaysia',    u'Maldives',    u'Mali',    u'Malta',   u'Marshall Islands',    u'Mauritania',  u'Mauritius',   u'Mexico',  u'Micronesia',  u'Moldova', u'Monaco',  u'Mongolia',    u'Montenegro',  u'Montserrat',  u'Morocco', u'Mozambique',  u'Myanmar (Burma)', u'Namibia', u'Nauru',   u'Nepal',   u'Netherlands', u'Netherlands Antilles',    u'New Caledonia',   u'New Zealand', u'Nicaragua',   u'Niger',   u'Nigeria', u'Northern Mariana Islands',    u'North Korea', u'Norway',  u'Oman',    u'Pakistan',    u'Palau',   u'Palestine',   u'Panama',  u'Papua New Guinea',    u'Paraguay',    u'Peru',    u'Philippines', u'Poland',  u'Portugal',    u'Puerto Rico', u'Qatar',   u'Republic of the Congo',   u'Réunion', u'Romania', u'Russian Federation',  u'Rwanda',  u'Saint Kitts and Nevis',   u'Saint Lucia', u'Saint Pierre and Miquelon',   u'Saint Vincent and the Grenadines',    u'Samoa',   u'San Marino',  u'Sao Tome and Principe',   u'Saudi Arabia',    u'Senegal', u'Serbia',  u'Seychelles',  u'Sierra Leone',    u'Singapore',   u'Slovakia',    u'Slovenia',    u'Solomon Islands', u'Somalia', u'South Africa',    u'South Korea',     u'Spain',   u'Spain',   u'Sri Lanka',   u'Sudan',   u'Suriname',    u'Swaziland',   u'Sweden',  u'Switzerland', u'Syrian Arab Republic',    u'Taiwan',  u'Tajikistan',  u'Tanzania',    u'Thailand',    u'Togo',    u'Tonga',   u'Trinidad and Tobago', u'Tunisia', u'Turkey',  u'Turkmenistan',    u'Turks and Caicos Islands',    u'Uganda',  u'Ukraine', u'United Arab Emirates',    u'United Kingdom',  u'United States of America',    u'United States Virgin Islands',    u'Uruguay', u'Uzbekistan',  u'Vanuatu', u'Vatican City State',  u'Venezuela',   u'Vietnam', u'Wallis and Futuna',   u'Yemen',   u'Zambia',  u'Zimbabwe']
        
        # make a dictionary from the two listsprint "Combining the two lists into a dictionary:"
        if len(countryAbbKeyList) > len(countryList):
            raise
        dictCountry = dict(zip(countryAbbKeyList, countryList))
        #key = re.sub("\"","", key)
        key  = dictCountry[key]
        #for x in range(len(countryAbbKeyList)):
        #    if countryAbbKeyList[x] == key: 
        #        key = countryList[x]

        for i in list:
            if i[1] == key:
                return i[0] # i[0] is id
        print "[Error] cannot find '%s' in the country code lookup table" % key
        # if not found raise error
        raise 
    
    def lookupCountry_VAT(key):
                                #10                                    #11                                        #12                    #13                #14                     #15
        countryAbbKeyList = ['DK','FI','HU','IE','LU','MT','SI',    'BB','CY','DE','EE','ES','SP','GR','PT',    'BE','CZ','PL','SK',    'FR','IT','LV',     'AU','GB','LT','NL',    'MX']
        countryList =       ['10','10','10','10','10','10','10',    '11','11','11','11','11','11','11','11',    '12','12','12','12',    '13','13','13',     '14','14','14','14',    '15']       
        
        # make a dictionary from the two listsprint "Combining the two lists into a dictionary:"
        if len(countryAbbKeyList) > len(countryList):
            raise
        dictCountry = dict(zip(countryAbbKeyList, countryList))
        vatSum = ''
        #key = re.sub("\"","", key)
        try:
            vatSum  = dictCountry[key]
        except:
            vatSum = '3'
        #for x in range(len(countryAbbKeyList)):
        #    if countryAbbKeyList[x] == key: 
        #        key = countryList[x]

        vatNum = ''
#        for i in list:
#            if i[1] == key:
#                print i[0]
#                
        total = int(vatSum)
        for numZeroes in range(0, total):
            vatNum = vatNum + '0'
        print 'Company VAT: ' + vatNum
        return vatNum
        
        #print "[Error] cannot find '%s' in the VAT lookup table" % key
        # if not found raise error
        #raise
    
    def lookupCountryPostalCode(key):
        
        # lenth of characters in postal code, it does not check ANA NAN or NNN or AAA
        countryList =       ['03','03','03','04','04','04','04','04','04','04','04','04','04','04','04','04','04','04','05','05','05','05','05','05','05','05','05','05','05','05','05','05','05','05','05','05','06','06','06','06','06','06','06','06','05','07','07','07','08','08','07','09','05','05']
        countryAbbKeyList = ['FO','IS','LS','BB','BE','CY','AT','AU','CH','CR','DK','HU','LU','NA','NO','PH','TN','ZA','IL','TD','DZ','ES','SP','FI','FR','GR','IR','IT','KW','MC','MY','SA','TH','TR','VN','YU','CN','IN','NP','RO','RU','SG','SE','PL','DE','KP','CA','NL','JP','PT','GB','BR','US','MX']
        # make a dictionary from the two listsprint "Combining the two lists into a dictionary:"
        if len(countryAbbKeyList) > len(countryList):
            raise
        dictCountry = dict(zip(countryAbbKeyList, countryList))

        postalCodeLength = ''
        try:
            postalCodeLength  = dictCountry[key]
        except:
            postalCodeLength  = '0'
        
        totalChars = int(postalCodeLength)
        print '[info] Postal Code should be %s characters: ' % str(totalChars)
        return totalChars
        
        #print "[Error] cannot find '%s' in the VAT lookup table" % key
        # if not found raise error
        #raise
    
    optionlist = getOptionList()

    postalCodeLength = lookupCountryPostalCode(args["Country"])
    ##Neusoft: 
    if len(args['Zip_Postal_Code']) < postalCodeLength and postalCodeLength != 0:
# 邮编长度若超出范围
#        if leng(args['zip']) > postalCodeLength:
#            print "[error] Postal code length exceeds: %s" % len(args['zip'])
# Postal code不满足长度时，用0补足
        zipNum=''
        num = postalCodeLength - len(args['zip'])
        for numZeroes in range(0, num):
            zipNum += '0'
        args['Zip_Postal_Code'] += zipNum
        print '[info] Postal code is: %s' % args['zip']

    params = { 
            'authenticity_token'                  : gAuthToken,
            'record[name]'                        : args["Company_name"].encode("utf-8"),    # required
            'record[entity_type]'                 : "personal",
            'record[account_manager_id]'          : lookup_id(optionlist, "Ovi Support"),
            'record[report_url]'                  : "", 
            'record[report_username]'             : "",
            'record[report_password]'             : "",
            'record[report_description]'          : "",
            'record[trust_level]'                 : "1",
            'record[default_content_ranking]'     : "",
            'record[nda_bypass]'                  : "true",
            'record[details][vat_number]'         : lookupCountry_VAT(args["Country"]).encode("utf-8"),        # required
            'record[details][street_address]'     : args["Street_Address"].encode("utf-8"),         # required
            'record[details][street_address2]'    : "",
            'record[details][postal_code]'        : args["Zip_Postal_Code"],            # required
            'record[details][city]'               : args["City"].encode("utf-8"),           # required
            'record[details][state]'              : "",
            'record[details][province]'           : args["Province_State_District"].encode("utf-8"),
            'record[details][corporate_phone]'    : "",
            'record[details][business_email]'     : args["User_email"],  #args["email"],
            'record[details][business_phone]'     : args["User_phone"],          # required
            'record[details][technical_email]'    : "",
            'record[details][technical_phone]'    : "",
            'record[country_id]'                  : lookupCountry_id(optionlist, args["country"]),
            'record[details][www_url]'            : args["Company_Website"].encode("utf-8"),            # required
            ##Neusoft: Contact person和description暂不需要
            ##'record[details][contact_person]'     : (argsUser["firstname"].encode("utf-8") +' '+argsUser["lastname"]).encode("utf-8"),
            ##'record[details][description]'        : args["description"].encode("utf-8"),
            'record[details][where_you_find_us]'  : "Forum Nokia",
            'record[details][public_name]'        : unicode(args["Company_name"][:16].encode("utf-8")),
            'record[public_icon_file]'            : open(args["Application_icon_filename"],"rb"),
            #'record[details][messaging_allowed]'  : "true",
            'record[details][public_description]' : args["Company_description"].encode("utf-8")}
#    params = construct_metadata(BASE_URL + "/companies/new?_method=get&adapter=_list_inline_adapter",params,AUTHTOKEN_PATTERN)
    if isUpdate == False:
        params['commit'] = "Create"
    else:
        params['commit'] = "Update"

    if len(args["description"]) == 0:
        print '[error] company description is empty, cannot create company.'
        raise

    if isUpdate == False:
        page = getPage(BASE_URL + "/companies/create?iframe=true", params)
        companyid = re.findall("/companies/show/([0-9]+)\?_method=get", page)
        if len(companyid) != 1:
            print re.findall("Problems in fields: (.*)", page)
            raise
        return int(companyid[0])
    else:
        page = getPage(BASE_URL + "/companies/update/%s?iframe=true" % companyid, params)
        print "[info] complete"
        
def register_user(gAuthToken, args, companyid, isUpdate = False, userid = None):
    
    def getOptionList(page):
        return re.findall('<option value="([0-9]+)">(.*)</option>', page)

    def getRoleID(page):
        return re.findall('record_role__user_roles_([0-9]+)', page)[0]

    def parseinfo():
        # load the add a new user page to get the option list
        #print BASE_URL + "/users/new?_method=get&adapter=_list_inline_adapter"
        res = urllib2.urlopen(BASE_URL + "/users/new?_method=get&adapter=_list_inline_adapter")
        page = unicode(res.read(), "utf-8") 
        return getOptionList(page),getRoleID(page) 

    def lookup_id(list, key):
        for i in list:
            if i[1] == key:
                return i[0] # i[0] is id
        print "[Error] cannot find '%s' in the lookup table" % key
        # if not found raise error
        raise 

    optionlist,roleid = parseinfo()

    params = { 
                "authenticity_token"                        : gAuthToken,
                "record[email]"                             : args["useremail"].encode("utf-8"),
                "record[firstname]"                         : args["firstname"].encode("utf-8"),
                "record[lastname]"                          : args["lastname"].encode("utf-8"),
                "record[telephone]"                         : args["userphone"].encode("utf-8"),
                "record[company]"                           : companyid,
                "record[disabled]"                          : "false"}
                
    if isUpdate == False:
        global theRandString
        length=8
        seedlower=string.lowercase
        seeddigit=string.digits
        seedupper=string.uppercase
        theRandString=pwdd=pwdl=pwdu=''
    
        countl=random.randrange(1,length-1)
        countu=random.randrange(1,length-countl)
        countd=(length-countl-countu)
    
        #生成随机的字符
        for l in random.sample(seedlower,countl):
            pwdl+=l
        for u in random.sample(seedupper,countu):
            pwdu+=u
        for d in random.sample(seeddigit,countd):
            pwdd+=d
    
        #在随机位置出现随机的字符
        seed=pwdl+pwdu+pwdd
        shuffler=random.sample(seed,len(seed))
        theRandString="".join(shuffler)
        ##print theRandString
    ###########################################
        #random.choice(data)
        #suffix += unicode(str(random.randrange(1, 256)),'utf-8')
        params['commit'] = "Create"
        params['record[login]'] = args["username"].encode("utf-8")
        params["record[user_roles][%s][role][id]" % roleid] = lookup_id(optionlist, "app_wizard_role")
        
        params['record[password]'] = theRandString
        params['record[password_confirmation]'] = theRandString
        
        print 'User Random Password is:\t' + theRandString
        
        #print BASE_URL + "/users/create?iframe=true"
        res = urllib2.urlopen(BASE_URL + "/users/create?iframe=true", params)
        page = res.read()
        userid = re.findall("/users/show/([0-9]+)\?_method=get", page)
    
        if len(userid) != 1:
            print re.findall("There were problems with the following fields:(.*)", page)
            raise
    
        return int(userid[0])
    else:
        print "[info] checking user role..."
        params_userrole = urllib.urlencode({
                                            'authenticity_token':gAuthToken,
                                            '_method' : "get",
                                            'adapter' : "_list_inline_adapter",
                                            'associations' : "user_roles"})
        res = urllib2.urlopen(BASE_URL + "/users/nested/%s?" % userid, params_userrole)
        page = unicode(res.read(), "utf-8")
        userrole = page.find("app_wizard_role")
        if userrole != -1:
            print "[info] updating user..."
            params['commit'] = "Update"
            res = urllib2.urlopen(BASE_URL + "/users/update/%s?" % userid, params)
            print "[info] complete"
            return userrole
        else:
            print "####user role is not app wizard role, skip user update####"
            return userrole

def process_contents(csvdata):
    # 1. search 
    appidlist, appnamelist, = search_appwizard(appid)
    if appidlist == []:
        appidlist, appnamelist, search_appwizard(appname)
    search_contentid()
    # 2. upload
    
    # 3. update
    
    