python3 -m pip3 install flintrock

read -p "Enter number of slaves: " NUM

flintrock launch good_shelf_grp7 \
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

python3 analytics_script/setup_masternode.py good_shelf_grp7
