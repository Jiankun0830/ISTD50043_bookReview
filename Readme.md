# SUTD 50.043 Database group project for online book-self web application

## Setup
### MongoDB AWS EC2 server
1. configure the security group, allowing other devices to access mongo db on this instance.
        1. Go to your aws console to see running ec2 instances, find your ec2 instance there. Under the Security Groups, click launch-wizard. You will be brought to the page to configure security groups.
        2. At the bottom of your page, go to Inbound->Edit->Add Rule
        3. Set the following
                Type: Custom TCP Rule
                Port Range: 27017
                Source: Anywhere
        4. Click Save.

2. set up your mongodb.
```
## install wget
sudo apt-get update
sudo apt-get install wget
## download the setup script
wget --output-document=set_up_mongo.sh https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mongo_script/set_up_mongo.sh?token=AJBKBGV7UH5LDQ5JDPFJ43C53VDLM
## run the setup script
bash ./set_up_mongo.sh
rm set_up_mongo.sh
echo "Finished setting up mongoDB"
```

### Setting up mysql on a new EC2 instance

Instruction for using our automated script for mysql's installation, data downloading, data sql-loading


```
sudo apt-get update
sudo apt-get install wget

echo "setting up mysql"
wget --output-document=new_instance_setup_sql.sh https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mysql_script/new_instance_setup_sql.sh?token=AKWIWQVCR3OQUX6WTMR2WUK53VE7K
bash ./new_instance_setup_sql.sh
rm new_instance_setup_sql.sh
echo "Finished setting up mysql"
```

### Setting up webserver
```
git clone https://github.com/Jiankun0830/ISTD50043_bookReview -b release/0.1.0 && cd ISTD50043_bookReview/script/
bash ./application_setup.sh
```

## requirements 
https://github.com/dinhtta/istd50043_project

## Reference
adapt code from https://github.com/isaychris/flask-book-reviews

## Collaborators
- Lu Jiankun 1002959
- Zhao Lutong 1002872
- Peng Shanshan 1002974
- Gao Yunyi 1002871
- Nashita Abd Tipusultan Guntaguli 1003045
- Ainul Mardhiyyah 1003115
- Hong Pengfei 1002949
