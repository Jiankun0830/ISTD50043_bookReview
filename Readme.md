# SUTD 50.043 Database group project for online book-self web application
## Documentation
Please see the full documentation avialble at
https://github.com/Jiankun0830/ISTD50043_bookReview/blob/master/documentation.pdf

## Live Demo
http://34.203.234.152/home_page \
http://44.229.150.14/home_page


## Setup
Run this command in your terminal
```
curl https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/setup.sh | sudo bash
```
### Setup Reminder
1. Please make sure there are more >= 3 elastic ip address quota on this region (Singapore) for use, this is very important :)
Please input the aws credentials and number of datanode you want to choose, you will have the option of number of datanodes NUM= 1,3,7
2. We will set up all the ec2 instances in region ap-southeast-1 (Singapore) , and all the AMI images for instances are within Singapore region. 
3. To access to the front end, as we screenshotted in the report, there are 3 ways to find the IP address of the web server. Once we find the IP address for the web app, just paste it on the browser, you will automatically be directed to the homepage. e.g. http://35.161.123.244
4. To access the output file of analytics, we already scp to the local machine. Therefore, it will be automatically stored in current directory (your local machine) where you execute setup.sh after the analytics part finish execution
5. Reminder: In later part of the execution script for production backend setup, i.e. setting up mongoDB, mySQL may take 3~5 minutes to setup due to the installation, therefore it may looks that it ‘hangs’ at that stage :)
When the script finished executing, please wait for 4-5 minus for the server to finish setting up.



## Requirements 
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
