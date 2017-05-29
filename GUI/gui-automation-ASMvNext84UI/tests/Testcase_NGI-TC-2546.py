"""
Author: P.Suman
Created Date: Nov 24, 2015
Description: Verify that for each service on the Services page, the Read-only user is unable to Export to file.
"""

from globalImports import *

tc_id=utility.get_tc_data(__file__)

class Testcase(Manager.Manager): 
    """
    Read-only unable to Export to file on Services page.
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
        serviceName="Test Service"
        templateName = "Test Template"
        self.browserObject = globalVars.browserObject
        
        #Check for current logged in user
        self.verifyCurrentUser(userRole='Administrator', loginAsUser=True)
        
        #Create Template if not exists
        self.createSampleTemplate(templateName=templateName, publishedTemplate=True)
        
        #Get Service List
        serviceList = self.getServices(serviceName=serviceName)
        if len(serviceList) <= 0:
            self.deployService(templateName, serviceName)
        
        #Check for current logged in user
        self.verifyCurrentUser(userRole='Read only', loginAsUser=True)
        
        #Verify Options
        self.getServiceOptions(actualOptions=["Export to File", "View Details", "Update Firmware"], disableOptions=["Export to File"], serviceName=serviceName)
        
        
    