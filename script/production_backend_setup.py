# For Part 1
import sys
import boto3
import pprint as pp
import os
from botocore.exceptions import ClientError
import time
# For Part 2
import botocore
import paramiko


# Take in argument of credentials and set up
# key = input("Please enter your AWS access key:")
# secret_key = input("Please enter your AWS secret access key:")
key = sys.argv[1]
secret_key = sys.argv[2]



region = "us-west-2"
# region = 'ap-southeast-1'

os.system("echo '[default]\naws_access_key_id = %s\naws_secret_access_key = %s' > ~/.aws/credentials"%(str(key),str(secret_key)))
os.system("echo '[default]\nregion = %s' > ~/.aws/config"%(str(region)))


#functions:

def print_bold(string):
    print('\033[1m'+string+'\033[0m')

#Function for creating security group
def create_security_group(security_group_name):
    response = ec2_client.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '') #Get VPC id of this aws account

    try:
        response = ec2_client.create_security_group(GroupName=security_group_name,
                                             Description="Group7:This is for SUTD 50.0043 Big Data and Database project",
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        pp.pprint('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,      ## SSH
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 27017,   ## MongoDB
                 'ToPort': 27017,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 3306,    ## mySQL
                 'ToPort': 3306,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}

            ])
        pp.pprint('Ingress Successfully Set %s' % data)

    except ClientError as e:
        pp.pprint(e)

#Function for creating a key-pair for EC2 instance
def generate_key_pairs(key_name):  # Key_name needs to be unique *
    outfile = open('{}.pem'.format(key_name),'w')
    key_pair = ec2.create_key_pair(KeyName=key_name)
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)
    # print(KeyPairOut)
    print("Finish creating EC2 key paris")
    os.system("chmod 400 {}.pem".format(key_name))



# Connection #it should automaticaly use your aws credentials and config
ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

#Part 1

# 1.1 Set up Security Group
#Check if our security group exists,otherwise create one
print_bold("\nStep 1.1 Set up Security Group:")
security_group_name='Group7_500043_ShelfRead'
try:
    response = ec2_client.describe_security_groups(GroupNames=[security_group_name])
    print("Security group: {} exits".format(security_group_name))
#     pp.pprint(response)
except ClientError as e:
#     pp.pprint(e)
    print("This security group doesn't exist,creating a new one...\n")
    create_security_group(security_group_name)


# 1.2 Set up Key-pair
# Check if our key-pair exists,otherwise create one
print_bold("\nStep 1.2 Set up Key-pair:")
key_name = "group7-bigdata-ec2-key"
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


# Check elastic IP quota (We need at least 3 elastic ip address)
filters = [
    {'Name': 'domain', 'Values': ['vpc']}
]
addresses = ec2_client.describe_addresses(Filters=filters)
# print(addresses)
if len(addresses.get("Addresses"))> 5-3:
    print('\033[1m'+'\033[91m'+"This aws account will reach AddressLimit for elastic IPs (max 5) if it is a student account."+'\033[0m')
#     raise ValueError('This aws account will reach AddressLimit for elastic IPs (max 5) if it is a student account.')


# 1.3 Create 3 instances with above key and security group
print_bold('\nStep 1.3 Create 3 instances with above key and security group')
instances = ec2.create_instances(
     ImageId='ami-06d51e91cea0dac8d',  #UBuntu 18.04LTS  Oregon
#      ImageId='ami-061eb2b23f9f8839c',  #UBuntu 18.04LTS  Singapore
     MinCount=1,
     MaxCount=3, # create 3 instances
     KeyName=key_name,
     SecurityGroups=[security_group_name,]
 )

# get instances' ID:
instance_ids = []
for instance in instances:
    print("Creating instance {} ...".format(instance.id))
    instance.wait_until_running()
    instance_ids.append(instance.id)
print('Instance ids:',instance_ids)



# 1.4 Allocate and associate elastic IP for each instance
print_bold("\nStep 1.4 Allocate and associate elastic IP for each instance")
ip_addr = {}
for instance_id in instance_ids:
    try:
        allocation = ec2_client.allocate_address(Domain='vpc')
        print("Generated elastic IP: "+allocation.get('PublicIp'))
        response = ec2_client.associate_address(AllocationId=allocation['AllocationId'],
                                         InstanceId=instance_id)
        print(response)
        ip_addr[instance_id] = allocation.get('PublicIp')
    except ClientError as e:
        print(e)
print("Wait for the instances to run.")
time.sleep(300) #Wait for a while such that the instance is running




#Part2

key = paramiko.RSAKey.from_private_key_file(key_name+".pem")
p_client = paramiko.SSHClient()
p_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


#Create dictionary of each IP to pass as environment variables:
env_dic ={}
for i in range(len(instance_ids)):
    if i == 0:
        env_dic['LC_MONGO_IP'] = ip_addr.get(instance_ids[i])
    elif i == 1:
        env_dic['LC_MYSQL_IP'] = ip_addr.get(instance_ids[i])
    elif i == 2:
        env_dic['LC_WEBSERVER_IP'] = ip_addr.get(instance_ids[i])

print('\nIP dictionary:',env_dic)

def execute_commands(cmds):
    stdin , stdout, stderr = p_client.exec_command(cmds)
    lines = stdout.readlines()
    lines_err = stderr.readlines()
    for line in lines:
        print(line)
    for line in lines_err:
        print(line)
    if len(stderr.readlines()) != 0:
        print(stderr.readlines())    

# 2.1 Set up Mongo on the 1st EC2 instance
print_bold("\nStep 2.1 Set up Mongo on the 1st EC2 instance")
print('\033[36m'+'\033[1m'+'This will take around '+'\033[91m'+'10 minutes'+'\033[0m')
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    p_client.connect(hostname=ip_addr.get(instance_ids[0]), username="ubuntu", pkey=key) ## TodoL change to 0
    print_bold("Set up mongo on elastic ip: "+ip_addr.get(instance_ids[0]))

    # Execute commands
    # Step1 install wget
    print_bold("\nStep1 install wget")
    p_client.exec_command('sudo apt-get update;sudo apt-get install wget')
        
    # Step2  download mongo setup script
    print_bold("Step2 download mongo setup script and run mongo setup script")

    execute_commands('wget --output-document=set_up_mongo.sh https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/mongo_script/set_up_mongo.sh;yes | bash set_up_mongo.sh')

           
    # Step3 run mongo setup script
#     print_bold("Step3 run mongo setup script")    
#     execute_commands('chmod +x set_up_mongo.sh')
#     execute_commands("yes | ./set_up_mongo.sh")
#     execute_commands('rm set_up_mongo.sh;ls')


    # close the client connection once the job is done
    p_client.close()

except Exception as e:
    print(e)

# 2.2 Set up MySQL on the 2nd EC2 instance
print_bold("\nStep 2.2 Set up MySQL on the 2nd EC2 instance ")
print('\033[36m'+'\033[1m'+'This will take around '+'\033[91m'+'3/FOUR minutes'+'\033[0m')
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    p_client.connect(hostname=ip_addr.get(instance_ids[1]), username="ubuntu", pkey=key)
    print_bold("Set up mysql on elastic ip: "+ip_addr.get(instance_ids[1]))
    
    # Execute commands
    # Step1 install wget
    print_bold("Step1 install wget")
    execute_commands('sudo apt-get update;sudo apt-get install wget')

    # Step2  download mysql setup script
    print_bold("Step2 download mysql setup script")
    execute_commands('wget --output-document=new_instance_setup_sql.sh https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mysql_script/new_instance_setup_sql.sh?token=AKWIWQR4G5ABTLHMIHRS5SS55UAYC;ls')
  
    # Step3 run mysq setup script
    print_bold("Step3 run mysql setup script")
    execute_commands('chmod +x new_instance_setup_sql.sh')
    execute_commands("yes | ./new_instance_setup_sql.sh")
    execute_commands('rm new_instance_setup_sql.sh;ls')
  
    # close the client connection once the job is done
    p_client.close()

except Exception as e:
    print(e)

# 2.3 Set up web server on the 3rd EC2 instance
try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    p_client.connect(hostname=ip_addr.get(instance_ids[2]), username="ubuntu", pkey=key)
    print_bold("Set up server on elastic ip: "+ip_addr.get(instance_ids[2]))

    # Execute commands
    # Step1 git clone server's code
    print_bold("Step1 git clone web server's code")
    
    execute_commands('git clone https://github.com/Jiankun0830/ISTD50043_bookReview')
        
    # Step2 run web server setup script
    print_bold("Step2 run web server's setup script")
                                                  
    execute_commands('cd ISTD50043_bookReview/script/;chmod +x application_setup.sh;ls')
    
    
    stdin, stdout, stderr = p_client.exec_command('cd ISTD50043_bookReview/script/; screen -d -m bash application_setup.sh 80 ',environment=env_dic)
    lines = stdout.readlines()
    for line in lines:
        print(line)
    err_lines = stderr.readlines()
    for err in err_lines:
        print(err)
    
    print_bold('Running App in the backend, may need to wait few minutes to download all the relevent packages...')
    print('\033[36m'+'\033[1m'+'You may need to wait for '+'\033[91m'+'4-5 minutes'+'\033[0m')                               
    
    print_bold("\033[36m"+"\nYou can view the app though {} after 4-5 minutes".format(ip_addr.get(instance_ids[2])))
    # close the client connection once the job is done
    p_client.close()

except Exception as e:
    print(e)
