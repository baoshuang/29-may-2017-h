'''
Author: P.Suman
Created Date: Jun 14, 2016
Description: Enter service tag in initial setup under license section
'''
from globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    Enter service tag in initial setup under license section
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialization
        """
        Manager.Manager.__init__(self, tc_id, *args, **kwargs)
    
    def preRunSetup(self, userOption="Delete"):
        """
        Creating Pre-requisite Setup for running the test scenario 
        """
        self.logDesc("Pre Run Setup")        
        #Login as Admin
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
        #Set Service Tag
        self.initialSetup()
        #Verify Service Tag
        self.verifyServiceTag(globalVars.serviceTag)
   
    @BaseClass.TestBase.func_exec
    def test_functionality(self):        
        """
        This is the execution starting function
        """
        self.browserObject = globalVars.browserObject

        self.preRunSetup()
        
        self.runTestCase()
        
        self.postRunCleanup()

