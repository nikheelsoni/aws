# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:52:17 2020

@author: nikheel
"""

import boto3
import datetime
import botocore

'''
PAGINATION CONFIG

MaxItems - Limits the maximum number of total returned items returned while paginating.
PageSize - Controls the number of items returned per page of each result.
'''

def daysOld(creationDate):
    creationDate = creationDate.replace(tzinfo=None).date()
    difference = (datetime.datetime.now().date() - creationDate).days
    return difference

def deleteSnapshots(page_iterator,age):
    
    response = input("Deleting snapshots is a destructive operation and cannot be undone. Do you want to continue? (Y/N): ")
    if(response.lower() not in ["yes","y"]):
        print ("Not deleting any snapshots. Exiting program")
        return

    for page in page_iterator: 
        response = page["Snapshots"]  
        for i in range(len(response)):   
            snapshotID = response[i]["SnapshotId"]
            createdDate = response[i]["StartTime"]   
            x = daysOld(createdDate)
            if(x>age):
                print ("Deleting Snapshot {} that is {} days old".format(snapshotID,x))
                try:
                    client.delete_snapshot(SnapshotId=snapshotID)
                except botocore.exceptions.ClientError as Error:
                    print (Error)

def describeSnapshots(page_iterator,age):
    
    print("{:=^45}".format("")) 
    print ("{:22} {:13} {:8}".format("SnapshotID","Creation Date","Days Old"))

    for page in page_iterator: 
            response = page["Snapshots"]  
            for i in range(len(response)):   
                snapshotID = response[i]["SnapshotId"]
                createdDate = response[i]["StartTime"]   
                x = daysOld(createdDate)
                if(x>age):
                    print ("{} {:13} {}".format(snapshotID,str(createdDate.date()),x))
    print("{:=^45}".format("")) 
                    
if __name__ == '__main__':
    
    client = boto3.client("ec2",region_name="eu-west-1")
    paginator = client.get_paginator('describe_snapshots')
    page_iterator = paginator.paginate(OwnerIds=['self'],PaginationConfig={'PageSize': 10})
    
    
    print("1. Describe Snapshots")
    print("2. Delete Snapshots")
    response = input("Please select an option (1/2): ")
    if response not in ["1","2"]:
        print ("Invalid option. Please try again")
    else:
        age = input("Enter number of days snapshot is older than: ")
        try:
            age = int(age)
            if(response == "1"):
                describeSnapshots(page_iterator,age)
            if(response == "2"):
                deleteSnapshots(page_iterator,age)
        except ValueError:
            print ("Invalid value. Please try again")
            
        
