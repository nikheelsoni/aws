# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:07:32 2020

@author: nikhe
"""

import boto3

class AWS():
    
    regions = []
    
    def __init__(self,service,region):
        self.boto3Client = boto3.client(service,region_name=region)
        
    def Regions(self):
        response = self.boto3Client.describe_regions()
        for i in range(len(response["Regions"])):
            self.regions.append(response["Regions"][i]["RegionName"])
        
class EC2(AWS):
    
    def __init__(self):
        pass
    
    def describeInstances(self):
        response = self.boto3Client.describe_instances()
        return response
    
class Instances():
        
    def __init__(self,name,instanceID,state,privateIP,publicIP,AMI):
        self.name = name
        self.instanceID = instanceID
        self.state = state
        self.privateIP = privateIP
        self.publicIP = publicIP
        self.AMI = AMI
        
def printInstances(client,region):
    
    response = EC2.describeInstances(client)
    
    myInstances = []
    
    for i in range(len(response["Reservations"])):
        
        temp = response["Reservations"][i]["Instances"][0]
        
        try:
            tags = temp["Tags"]
            for i in range(len(tags)):
                if(tags[i]["Key"]=="Name"):
                    name = tags[i]["Value"]        
        except:
            name = "-"
         
        instanceID = temp["InstanceId"]
        state = temp["State"]["Name"]
        privateIP = temp["PrivateIpAddress"]
        
        try:
            publicIP = temp["PublicIpAddress"]
        except:
            publicIP = "-"
        
        AMI = temp["ImageId"]
        
        myInstances.append(Instances(name,instanceID,state,privateIP,publicIP,AMI))
        
    if(len(myInstances)==0):
        return
    
    print ("\n{:-^114}\n".format(region))
        
    for i in range(len(myInstances)):
        print ("{:30} {:20} {:8} {:15} {:15} {:20}".format(
                myInstances[i].name,
                myInstances[i].instanceID,
                myInstances[i].state,
                myInstances[i].publicIP,
                myInstances[i].privateIP,
                myInstances[i].AMI,
                )
        )
    
    return
    
def main():
            
    client = AWS("ec2","eu-west-1")
    client.Regions()
    
    for i in range(len(AWS.regions)):
        client = AWS("ec2",AWS.regions[i])
        printInstances(client,AWS.regions[i])
    
if __name__ == "__main__":
    
    main()
