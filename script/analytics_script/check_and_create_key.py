import boto3
from botocore.exceptions import ClientError
import os
import paramiko
import sys

key_name =sys.argv[1]

# Take in argument of credentials and set up
key = input("Please enter your AWS access key:")
secret_key = input("Please enter your AWS secret access key:")
region = "us-west-2"

os.system("echo '[default]\naws_access_key_id = %s\naws_secret_access_key = %s' > ~/.aws/credentials"%(str(key),str(secret_key)))
os.system("echo '[default]\nregion = %s' > ~/.aws/config"%(str(region)))

ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def print_bold(string):
    print('\033[1m'+string+'\033[0m')

#Function for creating a key-pair for EC2 instance
def generate_key_pairs(key_name):  # Key_name needs to be unique *
    outfile = open('{}.pem'.format(key_name),'w')
    key_pair = ec2.create_key_pair(KeyName=key_name)
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)
    # print(KeyPairOut)
    print("Finish creating EC2 key paris")
    os.system("chmod 400 {}.pem".format(key_name))



# Set up Key-pair
# Check if our key-pair exists,otherwise create one
print_bold("\nStep 1.2 Set up Key-pair:")
key_not_exist = True

keyPairs = ec2_client.describe_key_pairs()
for key in keyPairs.get('KeyPairs'):
    if key.get('KeyName') == key_name:
        key_not_exist = False
        print("key-pair: {} exists.".format(key_name))
        break
if key_not_exist :
    print("Generating a unique key for EC2 instances")
    generate_key_pairs(key_name)

key = paramiko.RSAKey.from_private_key_file(key_name+".pem")
