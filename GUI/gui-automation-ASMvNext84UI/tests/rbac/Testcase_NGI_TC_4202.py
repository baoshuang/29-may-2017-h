'''
Created on Dec 8, 2015

@author: rajeev.kumar

Description :Verify that on the Firmware page, the Read-only can view the firmware information.

'''
from tests.globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    Firmware page, the Read-only can view the firmware information.
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
        self.verifyCurrentUser(userRole='Read only', loginAsUser=True)
        
        #Navigate to repositories Page
        self.get_RepositoriesPage("Details")
        
        self.logout()