'''
Author: raj.patel
Created Date: Feb 24, 2016
Description: Getting started page,select to Restore Now.
Test Flow    : 1) Log into the ASM UI and navigate to the Getting started page, 
              2) select to Restore Now.
              3)Prerequisite: BACKUPPATH  must be in same location and specified in config.ini
'''
from globalImports import *
from libs.product.pages import Resources, Dashboard

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
     Getting started page page,select to Restore Now.

    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialization
        """
       
        Manager.Manager.__init__(self, tc_id, *args, **kwargs)
      
    def preRunSetup(self):
        """
        Creating Pre-requisite Setup for running the test scenario 
        """
        self.logDesc("Pre Run Setup")        
        self.verifyCurrentUser(userRole='Administrator', loginAsUser=True)
        
    def postRunCleanup(self):
        """
        Creating Post Run setup to be executed after running the test case
        Cleans the data created by this script
        """
        self.logDesc("Post Run Cleanup")
        
        self.logout()
        
    
    def runTestCase(self):
        """
        Running Test Case
        """
        self.logDesc("Running Test Case")
        self.restoreNowFromGettingstarted()

        
    @BaseClass.TestBase.func_exec
    def test_functionality(self):        
        """
        This is the execution starting function
        """
        
        self.browserObject = globalVars.browserObject

        self.preRunSetup()
        
        self.runTestCase()
         
        self.postRunCleanup()
