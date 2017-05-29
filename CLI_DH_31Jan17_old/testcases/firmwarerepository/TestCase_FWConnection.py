'''
Created on march 23, 2017

@author: raj.patel
Description:
/FirmwareRepository/connection    post

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
import time

class Testcase(DiscoverResourceTestBase):
    
    td_Id=""
    refId=""
    def __init__(self):
        DiscoverResourceTestBase.__init__(self)
        self.tc_Id = self.getTestCaseID(__file__)
        
        
        
    def testFWConection(self):
        
        response = self.authenticate()
        logger = self.getLoggerInstance()
        logger.debug('Login Response is')
        logger.info(response)
        self.log_data("Running Test Case ::: ")
        firmwareRepoPayload = self.readFile(globalVars.firmwareRepoPayload)
        SourceLocation = globalVars.nfsSourceLocationConTest
        response,status = self.testFWConnection(firmwareRepoPayload,SourceLocation)
        if status:
            self.log_TestData(["", "", "", str(self.tc_Id),'Success','FW Repository connection tested successfully'])
            
        else:
            self.log_TestData(["", "", "", str(self.tc_Id),'Failed','FW Repository connection Failed','Testcase failed'])     
        
        
if __name__ == "__main__":
    test = Testcase()
    test.getCSVHeader()
    test.testFWConection()
    os.chdir(current_dir)
    


    
        
        
        
