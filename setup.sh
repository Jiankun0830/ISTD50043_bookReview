#!/bin/bash

# --------- Linux setup ----------
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    echo "Detected Linux system"
    echo ""
    
    if ! [ -x "$(command -v python3)" ]; then
        echo -e "This script assumes you can run python3, now Installing python using sudo"
        sudo apt-get install python3-pip
    fi
    echo "This script assumes you have wget"
    if ! [ -x "$(command -v wget)" ]; then
        sudo apt-get install wget
    fi
# ------- mac setup --------------
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected MACOSX system"
    echo ""
    echo "This script assumes you have curl"
    echo "Installing curl on your machine "
    if ! [ -x "$(command -v curl)" ]; then
        brew install curl
    fi
else
    echo "This script only runs on Unix based system"
fi


mkdir -p ~/.aws
FILE=~/.aws/credientials
if [ -f "$FILE" ]; then
    touch "$FILE"
fi
FILE=~/.aws/config
if [ -f "$FILE" ]; then
    touch "$FILE"
fi

echo -e "Downloading setup scripts"
curl https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/production_backend_setup.py --output production_backend_setup.py
curl https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/analytics_script/setup_masternode.py --output setup_masternode.py



read -p "Create new python virtual environment 'goodshelf' to run command, (y/n)?" create
echo -p "You can remove the virutal environment by 'rm -rf goodshelf'"
if [ "$create" == "y" ]; then
    python3 -m venv goodshelf
    source goodshelf/bin/activate
else 
    echo "Skipped creating new environment, you need to create virtual environment to run our code"
    echo "Terminating process..."
    exit 
fi


echo -e "Installing necessary library: boto3 and paramiko"
python3 -m pip install boto3 paramiko flintrock


echo "=========== LOCAL DEPENDENCIES ARE INSTALLED ============="

read -p "Please enter your AWS access key: " KEY
read -p "Please enter your AWS secret access key: " SECRET_KEY
read -p "Please Enter number of slaves: " NUM

echo "=========== RUNNING PRODUCTION BACKEND SETUP ============="
python3 production_backend_setup.py $KEY  $SECRET_KEY



echo "=========== RUNNING ANALYTICS BACKEND SETUP =============="
flintrock launch good_shelf_grp7_$NUM \
    --num-slaves $NUM \
    --spark-version 2.4.4 \
    --hdfs-version 2.7.7 \
    --ec2-key-name group7-bigdata-ec2-key \
    --ec2-identity-file group7-bigdata-ec2-key.pem \
    --ec2-ami ami-000b133338f7f4255 \
    --ec2-user ec2-user \
    --ec2-instance-type t2.medium \
    --ec2-region us-west-2 \
    --install-hdfs \
    --install-spark

python3 setup_masternode.py good_shelf_grp7_$NUM



# -------- remove the redundant files 
rm production_backend_setup.py
rm setup_masternode.py
