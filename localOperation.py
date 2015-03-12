#encoding:UTF-8
import os
import sys
import platform
import tempfile
import data
import re
gPathDelim=''
def isZip(filename):
    extList = ["zip"]
    if "." not in filename: return False
    #1 in rsplit makes sure the it only get the right most dot
    elif filename.rsplit(".",-1)[-1].lower() in extList: return True
    else: return False

def getAppID(fname):
    fstr = fname.split('appwizard')[-1]
    fstr2 = re.findall('_([0-9]+)_', fstr)
    if len(fstr2) == 0:
        fstr2 = re.findall('([0-9]+)_', fstr)
    return fstr2[0]

def initPathDelimeter():
    global gPathDelim
    # this is only important for this script because we are interfacing
    # with dumpsis.exe which does not like unix style path delimiters ie: /
    if platform.system() == 'Windows':
        gPathDelim = '\\'
    else:
        gPathDelim = '/'
def getWorkFolders():
    TestDir = getMainDir() + gPathDelim + data.TestPath
    if '\\' in TestDir:
        TestDir = TestDir.replace('\\', '/')
    
    ReportsDir = getMainDir() + gPathDelim + data.ReportsPath
    if '\\' in ReportsDir:
        ReportsDir = ReportsDir.replace('\\', '/')
    
    if os.path.exists(ReportsDir) == False:
        os.mkdir(ReportsDir)
        if os.path.exists(ReportsDir) == False:
            return False
            
    if os.path.exists(TestDir) == False:
        os.mkdir(TestDir)
        if os.path.exists(TestDir) == False:
            return False
    return TestDir,ReportsDir
    print '[info] Test folder: ' + TestDir
    print '[info] Reports folder: ' + ReportsDir

def getMainDir():
    # py2exe's - works for both scripts and services
    if hasattr(sys, "frozen"):
        ##Neusoft: sys.executable返回Python解释器的名字：pythonw.exe
        return os.path.dirname(sys.executable)
    # running as a python script based service, this will crash if the python script is not running as a service
    # import servicemanager
    # if servicemanager.RunningAsService():
        # last entry on the path seems to be good int this case
    #   return sys.path[-1]
    # plain python script
    ##Neusoft: 返回脚本所在目录，argv返回脚本名字
    return os.path.dirname(sys.argv[0])

def createTmpFolder(fname):
    global gTempDir
    if len(fname) == 0:
    
        # the tempdir in windows has a path that is too long and files fail to upload
        ##Neusoft: splitdrive将路径名拆分并返回一个元组(drive, tail)
        if platform.system() == 'Windows':
            gTempDir = os.path.splitdrive(tempfile.gettempdir())[0] + "/" + "wiztmp" + "/"
        else:
            gTempDir = tempfile.gettempdir() + "/" + "wiztmp" + "/"
        #tmpdir = tempfile.gettempdir() + "/" + args[0] + "/"
        #tmpdir = getMainDir() + "/" + 'tmp' + "/"
        
        # make sure that the path is not using windows path style
        if '\\' in gTempDir:
            gTempDir = gTempDir.replace('\\', '/')
        
        if os.path.exists(gTempDir) == False:
            os.mkdir(gTempDir)
            if os.path.exists(gTempDir) == False:
                print '[error] Failed temporary folder creation : %s' % gTempDir
                return False
        
        print '[info] Created temporary folder: ' + gTempDir
    else:
        if os.path.exists(gTempDir+fname) == False:
            os.mkdir(gTempDir+fname)
            if os.path.exists(gTempDir+fname) == False:
                print '[error] Failed temporary folder creation : %s' % gTempDir+fname
                return False
        
        print '[info] Temporary folder: ' + gTempDir+fname
        
    return True

def csvLoader():
    pass

def main():
    TestDir,ReportsDir=getWorkFolders()
    dirList = os.listdir(TestDir)
    for ind, fname in enumerate(dirList):
        fname = TestDir + '/' + fname

        if os.path.isfile(fname) == False:
            print '[info] Skipping: %s' % fname
            continue
        print '[info] Found file: %s' % fname
        
        if isZip(fname):
            print '[info] Confirmed as Zip File: %s' % fname
           # create appID
            appID = getAppID(fname)
        if createTmpFolder(appID+'/') == False:
            raise

if __name__=="__main__":
    main()
