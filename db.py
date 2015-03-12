#encoding:UTF-8

from zip_data_reader import *
import sqlite3
from threading import Thread
from Queue import Queue

q = Queue()

def db_connect(dbname):
    dbname = script_dir + PATHDELIM + dbname
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
#    column_list = [i + ' text' + ',' for i in csvdata.keys()]
#    sqllecture=''
#    for i in column_list:
#        sqllecture += i
    return c

def table_creator(dbname, tablename):
    """ create a table 'tablename' in database 'dbname', return a bool variant"""
    c = db_connect(dbname)
#    column_list = [i + ' text' + ', ' for i in csvdata.keys()]
#    sqlstring = ''
#    for i in column_list:
#        sqlstring += i
    columns = ','.join([i for i in csv_key_std])
    c.execute('''create table %s (%s)''' % (tablename, columns))
#    c.execute('''create table %s
#    (Supplied_Publish_to_Ovi_Username text,
#    Supplied_Publish_to_Ovi_Email text, 
#    Company_Name text,
#    Street_Address text,
#    City text,
#    Province_State_District text,
#    Zip_Postal_Code text, 
#    Country text,
#    Company_Description text,
#    Company_Website text,
#    File_Type text,
#    Java_Certificate_Expiry_Date text,
#    Does_your_content_contain_encryption text,
#    Do_you_have_the_legal_right_to_distribute_this_content text,
#    Does_your_content_adhere_to_Content_Guidelines text,
#    Content_Item_Name text,
#    Display_Name text,
#    Description text,
#    Category text,
#    Price_Point text,
#    Keywords text,
#    Support_Email_Address text,
#    Support_Website text,
#    Version text,
#    Country_Distribution text,
#    Language_Distribution text,
#    Company_logo_filename text,
#    Application_icon_filename text,
#    Application_screenshot_1_filename text,
#    Application_screenshot_2_filename text,
#    Application_screenshot_3_filename text,
#    WRT_screenshot_1_filename text,
#    WRT_screenshot_2_filename text,
#    WRT_screenshot_3_filename text,
#    Java_binary_jar_filename text,
#    Java_binary_jad_filename text,
#    Widget_binary_filename text,
#    User_first_name text,
#    User_last_name text,
#    User_email text,
#    User_phone text,
#    Device_Distribution_for_WRT text,
#    Device_Distribution_for_Java text)''' % tablename)

    return True 
#    except:
#        print '[error] create table failed'
#        return False
#    return True

def insert_table(dbname,tablename,csvdata):
    conn = sqlite3.connect(dbname)
    c=conn.cursor()
    csvdata=sorted(csvdata.items(), key=lambda csvdata:csvdata[0])
    csvdata=[i[1] for i in csvdata]
    c.execute('insert into %s values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' % tablename, tuple(csvdata))
    conn.commit()
    return True

def select_from_db(tablename, conn):#(dbname, tablename):
#    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from %s' % tablename)
#    r = c.fetchall()
#    count = c.rowcount
    rows = c.fetchall()
    for r in rows:
        q.put(r)
#    r = c.fetchone()
    return q