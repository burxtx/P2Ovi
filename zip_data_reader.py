#encoding:UTF-8

from zipfile import ZipFile
import os
import sys
import platform
import re
import sqlite3
from db import *
import codecs

global script_dir
script_dir = os.path.dirname(sys.argv[0])

zip_data_folder = 'test'
global PATHDELIM
if platform.system() == 'Windows':
    PATHDELIM = '\\'
else:
    PATHDELIM = '/'

global csv_key_std
# 44 columns will be imported to database
csv_key_std=['Supplied_Publish_to_Ovi_Username',
                'Supplied_Publish_to_Ovi_Email',
                'Company_Name',
                'Street_Address',
                'City',
                'Province_State_District',
                'Zip_Postal_Code', 
                'Country',
                'Company_Description',
                'Company_Website',
                'File_Type',
                'Java_Certificate_Expiry_Date',
                'Does_your_content_contain_encryption',
                'Do_you_have_the_legal_right_to_distribute_this_content',
                'Does_your_content_adhere_to_Content_Guidelines',
                'Content_Item_Name',
                'Display_Name',
                'Description',
                'Category',
                'Categorization_Tags',
                'Price_Point',
                'Keywords',
                'Support_Email_Address',
                'Support_Website',
                'Version',
                'Country_Distribution',
                'Language_Distribution',
                'Company_logo_filename',
                'Application_icon_filename',
                'Java_screenshot_1_filename',
                'Java_screenshot_2_filename',
                'Java_screenshot_3_filename',
                'WRT_screenshot_1_filename',
                'WRT_screenshot_2_filename',
                'WRT_screenshot_3_filename',
                'Java_binary_jar_filename',
                'Java_binary_jad_filename',
                'Widget_binary_filename',
                'User_first_name',
                'User_last_name',
                'User_email',
                'User_phone',
                'Device_Distribution_for_WRT',
                'Device_Distribution_for_Java']  
csv_key_std.sort()
def check_zip_folder():
    """create a folder which stores the .zip files, return the dir of .zip packages"""
    zip_data_dir = script_dir + PATHDELIM + zip_data_folder
    if os.path.exists(zip_data_dir) == False:
        try:
            os.mkdir(zip_data_dir)
        except:
            print '[warning] creating work folder failed'
            return False
    print '[info] work folder: '+ zip_data_dir
    return zip_data_dir

def isZip(filename):
    """check if the file is a .zip file, return a bool variant"""
    extList = ["zip"]
    if "." not in filename: return False
    #1 in rsplit makes sure the it only get the right most dot
    elif filename.rsplit(".",-1)[-1].lower() in extList: return True
    else: return False
    
def check_zipped_csv_file(zip_data_dir):
    """return a csv file list, its element is the csv file path"""
    csvlist = []
    dirlist=os.listdir(zip_data_dir)
    if dirlist == []:
        print '[warning] Pls put a .zip folder in ' + zip_data_dir
        return csvlist
    for ind, file in enumerate(dirlist):
        file = zip_data_dir + PATHDELIM + file
        if os.path.isfile(file) == False:
            print '[warning] Skipping: %s' % file
            continue
        elif isZip(file):
            print '[info] Found zip file: %s' % file
        else: 
            print '[warning] file found but not zip file' 
            continue
        # extract zip package to their tmp folder
        csvfile = extract_csv_file(file)
        if csvfile:
            csvlist.append(csvfile)
    return csvlist

def get_app_id(fname):
    """return appwizard id"""
    fstr = fname.split('appwizard')[-1]
    fstr2 = re.findall('_([0-9]+)_', fstr)
    if len(fstr2) == 0:
        fstr2 = re.findall('([0-9]+)_', fstr)
    return fstr2[0]

def extract_csv_file(fname):
    """extract the .zip package to a folder with id and return csv file path"""
    app_id = get_app_id(fname)
    tmp_folder = script_dir + PATHDELIM + zip_data_folder + PATHDELIM + app_id
    if os.path.exists(tmp_folder) == False:
        try:
            os.mkdir(tmp_folder)
        except:
            print '[warning] create tmp folder failed'
            return False
    # unpackage the .zip file
    try:
        z = ZipFile(fname, "r")
        try:
            z.extractall(tmp_folder)
        except:
            print '[error] failed to extract .zip package'
    except:
        print '[error] failed to read .zip package'
        
    csvfilepath = tmp_folder + PATHDELIM + [i for i in z.namelist() if i[-3:] == "csv"][0]
    if os.path.isfile(csvfilepath) == False:
        print '[error] csv file not found in zip'
        return False
    else:
        print '[info] csv file found: %s' % csvfilepath
        return csvfilepath

def csv_modifier(csvfile):
    """modifier the csv file info, return a dict variant"""
    csvdata = {}
    res = codecs.open(csvfile,'r','utf_8')
    app_id=get_app_id(csvfile)
    tmpcsvpath = script_dir + PATHDELIM + zip_data_folder + PATHDELIM + app_id + PATHDELIM+"tmpcsv.csv"
    outputFile=codecs.open(tmpcsvpath, 'w', 'utf-8')
    for i in res:
        if "\r\n" in i:
            i=re.sub("\r\n", "\b", i)
            outputFile.write(str(i).encode("utf-8"))
        else:
            outputFile.write(str(i).encode("utf-8"))
    outputFile.close()
    for i in codecs.open(tmpcsvpath, 'r', 'utf-8'):        
        # there is a problem with this device, this is hard coded into the script for now!!
        i = re.sub("Nokia 2710 Navigation Edition.","Nokia 2710 Navigation Edition,", i)
        i = re.sub("Nokia 8800 Arte","Nokia 8800", i)
        i = re.sub("Nokia 6650d","Nokia 6650 Fold AT&T", i)
        i = re.sub("\r\n", "\b", i)
        key = i.split(",")[0].strip()  # first column is key
        value = i[len(key)+1:].strip() # rest of the line is value
#        print key
#        print value
        csvdata[unicode(key)] = re.sub("\"","", unicode(value))
        
    # special cases that need to be fixed
    # Countries 包含 Latin America对应的Language选择 ,如果Spanish is in language，则加上American Spanish；如果Portuguese is in the language,则加上Brazilian Portuguese，这两者都需要把English选上
    if "Latin America" in csvdata["Country Distribution"]:
        if "Spanish" in csvdata["Language Distribution"] and "American Spanish" not in csvdata["Language Distribution"]:
            csvdata["Language Distribution"] += ',Latin American Spanish'
            if "English" not in csvdata["Language Distribution"]:
                csvdata["Language Distribution"] += ',English'
        if "Portuguese" in csvdata["Language Distribution"] and "Brazilian Portuguese" not in csvdata["Language Distribution"]:
            csvdata["Language Distribution"] += ',Brazilian Portuguese'
            if "English" not in csvdata["Language Distribution"]:
                csvdata["Language Distribution"] += ',English'

    if "All Europe" in csvdata["Country Distribution"]:
        csvdata["Country Distribution"] = re.sub("All Europe","Europe", csvdata["Country Distribution"])   
    if "Netherland" in csvdata["Country Distribution"] and "Netherlands" not in csvdata["Country Distribution"] :
        csvdata["Country Distribution"] = re.sub("Netherland","Netherlands", csvdata["Country Distribution"])
    if "Russia" in csvdata["Country Distribution"] and "Russia Federation" not in csvdata["Country Distribution"]:
        csvdata["Country Distribution"] = re.sub("Russia", "Russian Federation", csvdata["Country Distribution"])
    if "Czech" in csvdata["Country Distribution"] and "Czech Republic" not in csvdata["Country Distribution"]:
        csvdata["Country Distribution"] = re.sub("Czech", "Czech Republic", csvdata["Country Distribution"])
    if "Middle East" in csvdata["Country Distribution"]:
        csvdata["Country Distribution"] = re.sub("Middle East", "Middle East and Africa", csvdata["Country Distribution"])
    elif "Africa" in csvdata["Country Distribution"]:
        csvdata["Country Distribution"] = re.sub("Africa", "Middle East and Africa", csvdata["Country Distribution"])
    if "Middle East and Africa" in csvdata["Country Distribution"] and 'Farsi (Persian)' in csvdata["Language Distribution"]:
        csvdata["Country Distribution"] += ',Afghanistan,Armenia,Bahrain,Iran,Iraq,Jordan,Kuwait,Lebanon,Maldives,Oman,Pakistan,Palestine,Qatar,Saudi Arabia,United Arab Emirates,Wallis and Futuna,Yemen'
        csvdata["Country Distribution"] = re.sub("Middle East and Africa,", "", csvdata["Country Distribution"])

    if "Ivory Coast" in csvdata["Country Distribution"]:
        csvdata["Country Distribution"] = re.sub("Ivory Coast","Côte dIvoire", csvdata["Country Distribution"])

    print '[info] Country Distribution:\t'+csvdata["Country Distribution"]

    if ("Traditional Chinese") in csvdata["Language Distribution"]:
        csvdata["Language Distribution"] = re.sub("Traditional Chinese", "Chinese TW Traditional,Chinese HK", csvdata["Language Distribution"])#"Chinese TW, Traditional,Chinese HK,Chinese (Simplified)", csvdata["Language Distribution"])
    if ("Simplified Chinese") in csvdata["Language Distribution"]:
        csvdata["Language Distribution"] = re.sub("Simplified Chinese", "Chinese (Simplified)", csvdata["Language Distribution"])    
        
    print '[info] Language Distribution:\t'+csvdata["Language Distribution"]
    try:
        resdir = script_dir + PATHDELIM + zip_data_folder + PATHDELIM + app_id + PATHDELIM
        csvdata["Application icon filename"]        = resdir + csvdata["Application icon filename"]
        csvdata["Java screenshot 1 filename"]  = resdir + csvdata["Java screenshot 1 filename"]
        csvdata["Java screenshot 2 filename"] = resdir + csvdata["Java screenshot 2 filename"]
        csvdata["Java screenshot 3 filename"] = resdir + csvdata["Java screenshot 3 filename"]
        csvdata["WRT screenshot 1 filename"]  = resdir + csvdata["WRT screenshot 1 filename"]
        csvdata["WRT screenshot 2 filename"] = resdir + csvdata["WRT screenshot 2 filename"]
        csvdata["WRT screenshot 3 filename"] = resdir + csvdata["WRT screenshot 3 filename"]
        csvdata["Java binary jar filename"] = resdir + csvdata["Java binary jar filename"]
        csvdata["Java binary jad filename"] = resdir + csvdata["Java binary jad filename"]
        csvdata["Widget binary filename"] = resdir + csvdata["Widget binary filename"]
    except:
        pass
    csvdb={} 
    for key, val in csvdata.items():
        key = re.sub(' |/', '_',key)
        csvdb[key]=val
    
    for i in csv_key_std:
        if i not in csvdb.keys():
            csvdb[i]='NULL'
            if csvdb[i] == '':
                csvdb[i]='NULL'
    return csvdb
    

def main():
    zip_data_dir = check_zip_folder()
    if zip_data_dir:
        csvlist = check_zipped_csv_file(zip_data_dir)
        if csvlist == []:
            print '[error] Pls check the .zip package is properly stored.'
            return
    else:
        print '[error] System error, pls check the work folder.' 
    # create a table
#    if table_creator('appwizard_db', 'appwizard_table'):
    if table_creator('appwizard_db', 'appwizard_table'):
        for i in csvlist:
            csvdata = csv_modifier(i)
            insert_table('appwizard_db', 'appwizard_table', csvdata)

if __name__ == '__main__': 
    main()