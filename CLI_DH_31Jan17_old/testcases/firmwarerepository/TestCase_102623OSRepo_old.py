'''
Created on Nov 6, 2014

@author: waseem.irshad
'''
import os
import sys
run_dir=os.path.abspath(os.path.dirname(__file__))
current_dir = os.getcwd()
os.chdir(run_dir)
sys.path.insert(0,os.path.abspath('../../discoverresources'))
sys.path.append(os.path.abspath('../../util'))
sys.path.append(os.path.abspath('../../testcases/common'))
sys.path.append(os.path.abspath('../../createdeploytemplate'))
sys.path.append(os.path.abspath('../../testcases/firmwarerepository'))

from DiscoverResourceBaseClass import DiscoverResourceTestBase
import globalVars
from encodings import raw_unicode_escape
import os

class Test_102623osRepo(DiscoverResourceTestBase):
    
    td_Id=""
    
    def __init__(self):
        DiscoverResourceTestBase.__init__(self)
        self.tc_Id = self.getTestCaseID(__file__)
        
     
    def cleanUpRepository(self):
        response,status = self.getResponse("GET", "osRepository")
        print " GET RESPONSE : "
        print response
        if "No information found" in response:
            print " No repository found"
        else:
            try:
                for repos in response:
                    resDel,statDel = self.getResponse("DELETE", "osRepository", refId=str(repos["id"]))
            except:
                print " unable to remove repository " 
                
        
    def createOSRepositoryfromISOPath(self, imageType, name, sourcePath):
        
        status = self.createOSRepository(imageType, name, sourcePath)
        if status == True:
            self.log_TestData(["", "", "",str(self.tc_Id),'Success',"Repository Created Successfully with name : %s"%name])
        else:
            self.log_TestData(["", "", "",str(self.tc_Id),'Failed',"Failed to create Repository with name : %s"%name])
        
        
            
        
        
if __name__ == "__main__":
    test = Test_102623osRepo()
    #test.test_Login()
    test.cleanUpRepository()
    test.createOSRepositoryfromISOPath("hyperv", "win2012",globalVars.osRepositoryPathR2)
    
        
        
        
