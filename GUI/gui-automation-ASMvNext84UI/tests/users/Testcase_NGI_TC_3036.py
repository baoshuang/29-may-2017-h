'''
Author: P.Suman
Created Date: Dec 22, 2015
Description: Change admin password- Delladmin uppercase, should throw error
'''
from tests.globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    Change admin password- Delladmin uppercase, should throw error
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
        #Check for current logged in user
        self.verifyCurrentUser(userRole='Administrator', loginAsUser=True)
        
    def postRunCleanup(self):
        """
        Creating Post Run setup to be executed after running the test case
        """
        self.logDesc("Post Run Cleanup")

    def runTestCase(self):
        """
        Running Test Case
        """
        self.logDesc("Running Test Case")
        #Edit 'admin' password
        self.editLocalUser(self.loginUser, userPassword="DELLADMIN",  
                        verifyUser=False, negativeScenario=True)
    
    @BaseClass.TestBase.func_exec
    def test_functionality(self):        
        """
        This is the execution starting function
        """
        self.browserObject = globalVars.browserObject

        self.preRunSetup()
        
        self.runTestCase()
        
        self.postRunCleanup()
    