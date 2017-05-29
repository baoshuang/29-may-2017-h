# -*- coding: utf-8 -*-
'''
Created on May 28, 2015

@author: dheeraj_si
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

from TemplateBaseClass import TemplateTestBase
import json
import globalVars
import time
import xml.etree.cElementTree as ET
from DiscoverResourceBaseClass import DiscoverResourceTestBase
import serverPoolValue
import inputForWorkFlowCases

class Testcase(TemplateTestBase,DiscoverResourceTestBase):
    """
   Create a server pool with 2 13G blades
   
Create and Publish a template that deploys 2 rack servers (ESX 5.1 and 5.5) with 2 existing volumes to a VMWare cluster and 
grant rights to standard user 1�

Standard user1 Deploys the cluster template for blades for ESXi.
Standard user1 scales up servers on ESXi deployment 

    """ 
    
    tc_Id=""
    def __init__(self):
        TemplateTestBase.__init__(self)
        DiscoverResourceTestBase.__init__(self)
        self.tc_Id = self.getTestCaseID(__file__)
    
    def createStandardUser(self):
        print " Going to create Standard User "
        self.authenticate()
        payload = self.readFile(globalVars.userPayload)        
        payload = payload.replace("user_name", inputForWorkFlowCases.StdUserName_1).replace("user_pwd", inputForWorkFlowCases.Std_User_Password_1).replace("user_domain", 
                    inputForWorkFlowCases.StdUserDomain).replace("user_role",inputForWorkFlowCases.StdUserRole).replace("login_user", "admin")            
        response =  self.getResponse("POST", "User", payload)
        self.userSeqId = response[0]["userSeqId"]
        print " Standard user created with seqID : %s"%str(self.userSeqId)
            
    def preRunSetup(self):
        
        respCSP = self.cleanServerPool()
        response =self.getDeviceList()
        discoveredDevicesValue=response[0]
        servers = []
        serverType = serverPoolValue.TestCase_78810
        for device in discoveredDevicesValue:
            devicetype=device['deviceType']
            serverModel=device['model']
            if (devicetype == "BladeServer" and serverType in serverModel):
                servers.append(device)
        
        if(len(servers) > 0):
            poolName = globalVars.serverPoolName
            response = self.createServerPool(servers,poolName)
        else:
            print " No BladeServers found of type : '%s'",str(serverType)
            

        
    def test_createAndPublishTemplate(self):
        
        response = self.authenticate()
        self.setNetworkList()
        payload = self.readFile(globalVars.filename_WorkFlow6_Case1)
        self.getResources()
        self.log_data(" Going to Create Template :: ")
        storageId =""
        vcenterId=""
        self.storageRes = self.getReqResource(limit=1, resourceType='COMPELLENT', deviceType=None)
        if len(self.storageRes) == 0:
            print "Required no. of Storage not available"
        else:
            storageId = self.storageRes[0]["refid"]
        self.vcenterRes = self.getReqResource(limit=1, resourceType='VCENTER', deviceType=None)
        if(len(self.vcenterRes)) == 0:
            print " Required no. of vcenter not found "
        else:
            vcenterId = self.vcenterRes[0]["refid"]
        result = self.getResponse("GET", "User", refId=str(self.userSeqId))
        if result is None:
            return " could not get the User information"
        print " Going to replace values for Standard user in payload : "
        payload = payload.replace("$seqId",str(result[0]["userSeqId"])).replace("$StdUserName_1",result[0]["userName"]).replace("$StdUserDomain",result[0]["domainName"]).replace("$StdUserRole",result[0]["role"])
        payload = payload.replace("$serversource",inputForWorkFlowCases.serversource)
        
        templateResponse= self.createTemplateWorkFlows(payload,vcenterId,storageId) 
        if templateResponse.status_code in (200, 201, 202, 203, 204):
            print " Template published. Going to login by Standard USer "
            self.authenticateForWorkflow(inputForWorkFlowCases.StdUserName_1, inputForWorkFlowCases.Std_User_Password_1)
            result  = json.loads(templateResponse.content)
            templateIdValue = result['id']
            globalVars.publishedTemplateID= templateIdValue
                                    
            self.log_TestData(["", "", "",str(self.tc_Id),'Success','Template created  and published Successfully','Server : Blade Server'])
            self.log_data( 'Successfully created  and published Template ')
            self.test_deployTemplate()
            
        else:
            self.log_TestData(["", "", "",str(self.tc_Id),'Failed','Failed to create/published template'])
            self.log_data( 'Failed to create/published template ')
            
    def test_deployTemplate(self):
        print " Going to Deploy Template by Standard User : "
        testCaseID=self.getTestCaseID(__file__)
        templateResult= self.getPublishedTemplateData(globalVars.publishedTemplateID)
        self.writeFile(globalVars.publishedTemp_filename, templateResult)
        tree = ET.ElementTree(file =globalVars.publishedTemp_filename)
        root = tree.getroot()
        ET.ElementTree(root).write(globalVars.publishedTemp_filename, xml_declaration=False)
        DeplName='WorkFlow1_Case1'
        deplyDesc='Deploy 2 servers with ESXI 5.5 with 2 Compllent storage volumes and a cluster with HA and DRS Enable and Red hat VM '
        self.log_data(" Going to Deploy Template :: ")
        deployResponse = self.deployTemplate(DeplName,deplyDesc)
        if deployResponse.status_code in (200, 201, 202, 203, 204):            
            
            #Get Deployment Id
            deploymentRefId = self.getDeploymentId(DeplName)
            loop = 60
            deploymentLogSubPath = '/opt/Dell/ASM/deployments/'
            deploymentLogPath= deploymentLogSubPath + str(deploymentRefId)
            
            while loop:
                resDS, statDS = self.getDeploymentStatus(deploymentRefId)
                if resDS.lower() in ("in_progress"):
                    time.sleep(120)
                else:
                    if resDS.lower() in ("complete"):
                        self.log_TestData(["", "", "",str(self.tc_Id),'Success','Template Deployed Successfully','Server : Blade Server', "deploymentLogPath: %s"%deploymentLogPath])
                        self.log_data( 'Successfully Deployed Service for the Deployment Name : %s'%DeplName)
#                         self.log_data( 'Now going to call the teardown of service ')
#                         self.runWebServiceAPI(str(self.tc_Id), "Pass", "Run in regression test")
#                         self.cleanDeployedService(deploymentRefId)
#                         self.test_cleanDeployedTemplates(deploymentRefId)
#                         self.log_data( 'Now going to call the teardown of Template ')
#                         self.test_cleanePublishedTemplates()
                        break
                    else:
                        print "Deployment Status: %s"%resDS
                        self.log_TestData(["", "", "",str(self.tc_Id),'Failed','Deployment Service Failed','Server : Blade Server', "deploymentLogPath: %s"%deploymentLogPath  ])
                        self.log_data('Deployment Service Failed for the Deployment Name : %s'%DeplName)
                        self.runWebServiceAPI(str(self.tc_Id), "Fail", "Run in regression test")
#                         self.log_data( 'Now going to call the teardown of service ')
#                         self.cleanDeployedService(deploymentRefId)
#                         self.test_cleanDeployedTemplates(deploymentRefId)
                        break
            loop -= 1
            self.log_data( 'Going to ScaleUp by standard user  for the testcase id : %s'%str(testCaseID))
            self.test_scaleUpServerbyStdUser(globalVars.publishedTemplateID, deploymentRefId, DeplName, deplyDesc)
        else:
            self.log_TestData(["", "", "",str(self.tc_Id),'Failed','Deployment Service Failed'])
            self.log_data('Deployment Service Failed for the Deployment Name : %s'%DeplName)
            
    def test_scaleUpServerbyStdUser(self, templateID, deploymentRefId, DeplName, deplyDesc):
        print " Going to scaleUp Template by Standard User : "
        logger = self.getLoggerInstance()
        testCaseID=self.getTestCaseID(__file__)
        payload = self.readFile(globalVars.filename_WorkFlow6_Case1_esxi_scaleup_server_stdsuer)
        payload = payload.replace("$serversource",inputForWorkFlowCases.serversource)
        scaleUpResponse = self.scaleUpdeployWorkFlowsTemplate(templateID, deploymentRefId, DeplName, deplyDesc, payload)
        logger.info( "printing the response from the scaleUp deploy template")
        logger.debug( scaleUpResponse.content)
        logger.info( "printing the status code")
        logger.info( scaleUpResponse.status_code)
        if scaleUpResponse.status_code in (200, 201, 202, 203, 204):            
            
            #Get Deployment Id
            #deploymentRefId = self.getDeploymentId(DeplName)
            loop = 60
            deploymentLogSubPath = '/opt/Dell/ASM/deployments/'
            deploymentLogPath= deploymentLogSubPath + str(deploymentRefId)
            
            while loop:
                resDS, statDS = self.getDeploymentStatus(deploymentRefId)
                if resDS.lower() in ("in_progress"):
                    time.sleep(120)
                else:
                    if resDS.lower() in ("complete"):
                        print "Deployment Status: %s"%resDS
                        self.log_TestData(["", "", "",str(testCaseID),'Success',' scaleUp Template by Standard USer Deployed Successfully', 'Server : Blade Server', "deploymentLogPath: %s"%deploymentLogPath])
                        self.log_data( 'Successfully ScaleUped Service by Standard User for the Deployment Name : %s'%DeplName)
                        #self.log_data( 'Now going to call the teardown of service ')
                        #self.cleanDeployedService(deploymentRefId)
                        #self.test_cleanDeployedTemplates(deploymentRefId)
#                         self.log_data( 'Now going to call the teardown of Template ')
#                         self.test_cleanePublishedTemplates()
                        break
                    else:
                        print "Deployment Status: %s"%resDS
                        self.log_TestData(["", "", "",str(testCaseID),'Failed','Deployment ScaleUped Service Failed', 'Server : Blade Server',  "deploymentLogPath: %s"%deploymentLogPath])
                        self.log_data('Deployment ScaleUped Service Failed for the Deployment Name : %s'%DeplName)
#                         self.log_data( 'Now going to call the teardown of Template ')
#                         self.test_cleanePublishedTemplates()
                        break
            loop -= 1
            self.log_data( 'Going to ScaleUp by standard user  for the testcase id : %s'%str(testCaseID))
            self.test_scaleUpVolumebyStdUser(globalVars.publishedTemplateID, deploymentRefId, DeplName, deplyDesc)
        else:
            self.log_TestData(["", "", "",str(testCaseID),'Failed','Failed to deploy scaleUp Service'])
            self.log_data('Deployment scaleUp Service Failed for the Deployment Name : %s'%DeplName)
            
    def test_scaleUpVolumebyStdUser(self, templateID, deploymentRefId, DeplName, deplyDesc):
        print " Going to scaleUp storage by Standard User : "
        logger = self.getLoggerInstance()
        testCaseID=self.getTestCaseID(__file__)
        payload = self.readFile(globalVars.filename_WorkFlow6_Case1_esxi_scaleup_storage_stduser)
        payload = payload.replace("$serversource",inputForWorkFlowCases.serversource)
        scaleUpResponse = self.scaleUpdeployWorkFlowsTemplate(templateID, deploymentRefId, DeplName, deplyDesc, payload)
        logger.info( "printing the response from the scaleUp deploy template")
        logger.debug( scaleUpResponse.content)
        logger.info( "printing the status code")
        logger.info( scaleUpResponse.status_code)
        if scaleUpResponse.status_code in (200, 201, 202, 203, 204):            
            
            #Get Deployment Id
            #deploymentRefId = self.getDeploymentId(DeplName)
            loop = 60
            deploymentLogSubPath = '/opt/Dell/ASM/deployments/'
            deploymentLogPath= deploymentLogSubPath + str(deploymentRefId)
            
            while loop:
                resDS, statDS = self.getDeploymentStatus(deploymentRefId)
                if resDS.lower() in ("in_progress"):
                    time.sleep(120)
                else:
                    if resDS.lower() in ("complete"):
                        print "Deployment Status: %s"%resDS
                        self.log_TestData(["", "", "",str(testCaseID),'Success',' scaleUp of storage Standard USer Deployed Successfully', 'Server : Blade Server', "deploymentLogPath: %s"%deploymentLogPath])
                        self.log_data( 'Successfully ScaleUped Service by Standard User for the Deployment Name : %s'%DeplName)
                        #self.log_data( 'Now going to call the teardown of service ')
                        #self.cleanDeployedService(deploymentRefId)
                        #self.test_cleanDeployedTemplates(deploymentRefId)
#                         self.log_data( 'Now going to call the teardown of Template ')
#                         self.test_cleanePublishedTemplates()
                        break
                    else:
                        print "Deployment Status: %s"%resDS
                        self.log_TestData(["", "", "",str(testCaseID),'Failed','Deployment ScaleUped Service Failed', 'Server : Blade Server',  "deploymentLogPath: %s"%deploymentLogPath])
                        self.log_data('Deployment ScaleUped Service Failed for the Deployment Name : %s'%DeplName)
#                         self.log_data( 'Now going to call the teardown of Template ')
#                         self.test_cleanePublishedTemplates()
                        break
            loop -= 1
        else:
            self.log_TestData(["", "", "",str(testCaseID),'Failed','Failed to deploy scaleUp Service'])
            self.log_data('Deployment scaleUp Service Failed for the Deployment Name : %s'%DeplName)


        
    def test_cleaneServerPool(self):
        
        response = self.cleanServerPool()
        logger = self.getLoggerInstance()
        logger.debug('Clean Server Pool Response is')
        logger.info(response)
        
    def test_cleanDeployedTemplates(self, deploymentRefId):
        
        response = self.teardownServices(deploymentRefId)
        logger = self.getLoggerInstance()
        logger.debug('Cleaning Deployed  Services  Response is')
        logger.info(response)
        logger.info(response)
        self.log_data("Cleaning Deployed  Services  Response is :%s"%str(response))

                
        
        
    def test_cleanePublishedTemplates(self):
        
        response = self.cleanUpTemplates()
        logger = self.getLoggerInstance()
        logger.debug('Cleaning Published Template Response is')
        logger.info(response)
        self.log_data("Cleaning Published Template Response is :%s"%str(response))


        
       
        

if __name__ == "__main__":
    test = Testcase()
    test.getCSVHeader()
    #test.preRunSetup()
    test.createStandardUser()
    test.test_createAndPublishTemplate()  

