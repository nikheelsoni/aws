# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 13:12:06 2021

@author: nikheel
"""

import boto3
import pandas as pd
import concurrent.futures

class EC2():
    
    def get_regions(self):
        regions = []
        client = boto3.client("ec2",region_name = "af-south-1")
        response = client.describe_regions()["Regions"]
        for element in response:
            regions.append(element["RegionName"])
        return regions

    def get_name(self,tags):
        if tags:
            for element in tags:
                if element["Key"] == "Name":
                    return (element["Value"])
            
    def get_instances(self,region):
        print (region)
        ec2 = boto3.resource("ec2",region_name = region)
        data = []
        for instance in ec2.instances.all():
            data.append((
                        self.get_name(instance.tags),
                        instance.id,
                        instance.instance_type,
                        instance.state["Name"],
                        instance.private_ip_address,
                        instance.public_ip_address,
                        region,
                        instance.placement["AvailabilityZone"],
                        instance.key_name
                   ))
        return data

if __name__ == '__main__':
    
    client = EC2()
    
    regions = client.get_regions()
    data = []
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(client.get_instances, regions)
        for element in results:
            data += element
            
    df = pd.DataFrame(data)
    df.columns = ['Name', 'Instance ID', 'Instance Type', 'State', 'Private IP', 'Public IP', 'Region', 'Availability Zone', 'Key Name']
    df.to_excel("instance-inventory.xlsx", index = False)