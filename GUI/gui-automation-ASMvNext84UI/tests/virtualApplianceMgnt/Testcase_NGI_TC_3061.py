'''
Author: dheeraj.singh
Created Date: Jun 8, 2016
Description: Apply 30 perpetual license on top of 30 perpertual license, it should throw an error
Test Flow    : 1) Log into the ASM UI and navigate to the Virtual Appliance Management page, 
              2) Add 30 perpetual license on top of 30 perpertual license
'''
from tests.globalImports import *
from libs.product.pages import Resources, Dashboard
from libs.product import globalVars

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
     Apply 30 perpetual license on top of 30 perpertual license, it should throw an error

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
        utility.execLog("Please run Testcase_NGI_TC_3059 before running this test case")       
        self.verifyCurrentUser(userRole='Administrator', loginAsUser=True)
        
    def postRunCleanup(self):
        """
        Creating Post Run setup to be executed after running the test case
        Cleans the data created by this script
        """
        
        self.logout()
        
    
    def runTestCase(self):
        """
        Running Test Case
        """
        self.logDesc("Running Test Case")
        evalLicensePath = globalVars.perp_license_file_path_for_30
        messsage = 'License has already been used.'
        #Get details of Jobs    
        self.addAllTypeLicenseMan(evalLicensePath, messsage)
        #self.verifyLicenseType()

        
    @BaseClass.TestBase.func_exec
    def test_functionality(self):        
        """
        This is the execution starting function
        """
        
        self.browserObject = globalVars.browserObject

        self.preRunSetup()
        
        self.runTestCase()
         
        self.postRunCleanup()
