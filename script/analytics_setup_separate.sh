wget https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/analytics_script/setup_masternode.py
wget https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/master/script/analytics_script/check_and_create_key.py
read -p "Enter number of slaves: " NUM

python3 -m pip install flintrock
python3 check_and_create_key.py group7-bigdata-ec2-key-$NUM

flintrock launch good_shelf_grp7_$NUM \
    --num-slaves $NUM \
    --spark-version 2.4.4 \
    --hdfs-version 2.7.7 \
    --ec2-key-name group7-bigdata-ec2-key-$NUM \
    --ec2-identity-file group7-bigdata-ec2-key-$NUM.pem \
    --ec2-ami ami-000b133338f7f4255 \
    --ec2-user ec2-user \
    --ec2-instance-type t2.medium \
    --ec2-region us-west-2 \
    --install-hdfs \
    --install-spark

python3 setup_masternode.py good_shelf_grp7_$NUM
rm setup_masternode.py
rm check_and_create_key.py
