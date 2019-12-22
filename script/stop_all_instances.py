import boto3
from botocore.exceptions import ClientError

import pprint


ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')


response = ec2_client.describe_instances(
    Filters=[
        {
            'Name':'key-name',
            'Values': [
                'group7-bigdata-ec2-key*'
            ]
        }
    ]
)

instances = response['Reservations']

to_terminate = []
for i in instances:
    for o in i['Instances']:
        if o['State']['Name'] != 'terminated': to_terminate.append(o['InstanceId'])


ec2.instances.filter(InstanceIds = to_terminate).terminate()


print(f'Instances {to_terminate} has terminated successfully')
