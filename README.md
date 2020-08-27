# aws-scripts
scripts for working with aws resources

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
