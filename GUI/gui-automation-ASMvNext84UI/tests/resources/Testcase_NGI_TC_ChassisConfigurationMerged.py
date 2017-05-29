'''
Author: Ankit.Manglic
Created Date: June 09, 2016
Description: This test case contains the verification for following 5 test cases:
2998, 3001, 3003, 3014, 3021
'''
from tests.globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    This test case contains the verification for following 5 test cases:
        2998, 3001, 3003, 3014, 3021.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialization
        """
        Manager.Manager.__init__(self, tc_id, *args, **kwargs)
        
    def postRunCleanup(self):
        """
        Creating Post Run setup to be executed after running the test case
        Cleans the data created by this script
        """
        
        self.logout()
    
    
    @BaseClass.TestBase.func_exec
    def test_functionality(self):        
        """
        This is the execution starting function
        """
        self.browserObject = globalVars.browserObject
        
        #Check for current logged in user
        self.verifyCurrentUser(userRole='Administrator', loginAsUser=True)
        #Flag for register/unRegister iDRAC on DNS 
        registeriDracDNS=False
        #Configure Chassis and verify configuration values
        self.chassisConfiguration("172.31.60.78", "HclTestChassis", "TestDns", "HclTestDC", "cold", "Rack5", "5", "fxser177", "IOMA1-test",registeriDracDNS=registeriDracDNS)
        
        self.postRunCleanup()