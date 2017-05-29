'''
Created on Feb 4, 2015

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
import time

class Test_102637(DiscoverResourceTestBase):
    
    td_Id=""
    
    def __init__(self):
        DiscoverResourceTestBase.__init__(self)
        self.tc_Id = self.getTestCaseID(__file__)
        
        
    def TestCase_102637(self):
        response,status = self.createRepoFromFTPShare()
        print " Response : %s"%str(response)
        if status:
            refId = response["id"]
        if status == True:
            self.log_TestData(["", "", "",str(self.tc_Id),'Success','Repository Created Successfully'])
        else:
            self.log_TestData(["", "", "",str(self.tc_Id),'Failed','Failed to create Repository'])
        
        while True:
            resFR, statFR = self.getResponse("GET", "FirmwareRepository",refId=refId)
            if not statFR:
                print " Could not get response from FirmwareRepository : %s"%str(resFR)
            print " response from GET FirmwareRepository : %s"%str(resFR)
            
            dStatus = resFR['downloadStatus']
            if dStatus.lower()=='available':
                print " Repository Download Succesfull : %s"%str(resFR)
                break
            elif dStatus.lower=='error':
                print " Repository download failed %s"%str(resFR)
                break
            else:
                time.sleep(180)
                print " Downloading firmware packages for Repository : %s"%str(resFR)
            
        
        
if __name__ == "__main__":
    test = Test_102637()
    test.TestCase_102637()
    os.chdir(current_dir)
        
        
        
