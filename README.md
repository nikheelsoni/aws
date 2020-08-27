# aws-scripts
Scripts for working with aws resources. The user will be able to run these scripts in one of the following environments:
- Local machine (AWS IAM User credentials set up accordingly)
- EC2 Instance (IAM Role with relevant permissions)
- AWS Lambda (Will need to make changes to scripts accordingly along with IAM role relevant permissions)

### EC2Instances.py

Console application that pulls details from current EC2 instances in a given account for all available regions and prints it out in a table.
Details pulled include:
  - Name (based on tag)
  - Instance Id
  - State
  - Public IP address
  - Private IP address
  - AMI ID

### DeleteSnapshots.py

Console application that allows you to find EBS snapshots that are older than a specified number of days as well as delete these snapshots (USE AT OWN RISK)
