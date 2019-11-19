wget https://kindle-metadata.s3.amazonaws.com/kindle-metadata-after-correction.json
sudo apt-get update
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt install python3-pip
pip3 install pymongo
sudo apt-get install -y mongodb-org
sudo service mongod start
mongoimport --db book_metadata --collection metadata --file kindle-metadata-after-correction.json
pip3 install pymongo
python3 assign_best_sellers.py
mongo <mongo_util.js
sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf
#sudo sed -i "s/#security:/security:\n  authorization: 'enabled'/g" /etc/mongod.conf
sudo service mongod restart
