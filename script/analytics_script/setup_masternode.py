import sys
import boto3
from botocore.exceptions import ClientError
import botocore
import paramiko

#TODO 1: good_shelf_grp7
#TODO 2: change iam instance id

cluster_name = sys.argv[1]
print('cluster name: ',cluster_name)

def print_bold(string):
    print('\033[1m'+string+'\033[0m')

def get_mastermode_ip(ec2_client,tagname):
    master_tagname = tagname + '-master'
    
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name':'tag:Name',
                'Values': [
                    master_tagname
                ]
            }
        ]
    )

    masternodes = response['Reservations'][0]['Instances']
    if len(masternodes) == 1:
        public_ip = masternodes[0]['PublicIpAddress']
        key_name = masternodes[0]['KeyName']
        print('\033[1m'+'\033[95m'+'Public ip for masternode: ',public_ip)
        print('Key required: {}.pem'.format(key_name)+'\033[0m')

        return public_ip,key_name
    else:
        print("Alarm: There are more than 1 or no master node on this ec2 instance!")

ec2_client = boto3.client('ec2')

masternode_ip,key_name= get_mastermode_ip(ec2_client,tagname = cluster_name)


key = paramiko.RSAKey.from_private_key_file(key_name+".pem")
p_client = paramiko.SSHClient()
p_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def execute_commands(cmds):
    stdin , stdout, stderr = p_client.exec_command(cmds)
    lines = stdout.readlines()
    for line in lines:
        print(line)
    if len(stderr.readlines()) != 0:
        print(stderr.readlines())    

# 2.1 Set up analytic applications on masternode
print_bold("\nSetup correlation and tf-idf applications:")
# print('\033[36m'+'\033[1m'+'This will take around '+'\033[91m'+'4/FOUR minutes'+'\033[0m')
try:
    p_client.connect(hostname=masternode_ip, username="ec2-user", pkey=key) 
    print_bold("Set up masternode on: "+str(masternode_ip))

    print_bold("\nStep1 install wget")
    execute_commands('sudo apt-get update;sudo apt-get install wget')
    print_bold("Step2 download analytics setup script")
    execute_commands("wget https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/analytics_script/analytics.sh")
    print_bold("Step3 execute analytics script")    
    execute_commands('chmod +x analytics.sh')
    execute_commands("yes | ./analytics.sh")
    execute_commands('rm analytics.sh;ls')


    # close the client connection once the job is done
    p_client.close()

except Exception as e:
    print(e)