'''
Author: P.Suman
Created Date: Oct 30, 2015
Description: Verify that at the first login and each login, the Read-only user lands on the Dashboard page 
            and never on Getting Started page.
'''
from tests.globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    First login and each login for the Read-only user
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialization
        """
        Manager.Manager.__init__(self, tc_id, *args, **kwargs)
    
    @BaseClass.TestBase.func_exec
    def test_functionality(self):        
        """
        This is the execution starting function
        """
        self.browserObject = globalVars.browserObject
        
        #Check for current logged in user
        self.verifyCurrentUser(userRole='Read only', reLogin=True)
        
        #Verify Getting Started Page
        self.verifyGettingStarted(userRole='Read only', verifyPageLaunch=True)
        