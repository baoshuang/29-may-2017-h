'''
Author: P.Suman
Created Date: Oct 26, 2015
Description: Verify that on the All Resources page, the Read-only is unable to Discover, Delete, manage or 
            unmanage any of the resource.
'''
from tests.globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    Read-only unable to Discover, Delete, manage or unmanage any of the resource.
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
        
        #Verify Options
        self.verifyOptions(pageName="Resources", tabName="Resources")
