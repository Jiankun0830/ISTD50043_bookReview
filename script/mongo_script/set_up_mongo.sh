wget https://kindle-metadata.s3.amazonaws.com/kindle-metadata-after-correction.json
wget --output-document=assign_best_sellers.py https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mongo_script/assign_best_seller.py?token=AJBKBGUV4PHPWUGCWNQYVLC55TQGK
wget --output-document=mongo_util.js https://raw.githubusercontent.com/Jiankun0830/ISTD50043_bookReview/release/0.1.0/script/mongo_script/mongo_util.js?token=AJBKBGVMUQR6JFDZACZ3MMC55TQOS
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
echo "Finished running best sellers"
mongo <mongo_util.js
sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf
#sudo sed -i "s/#security:/security:\n  authorization: 'enabled'/g" /etc/mongod.conf
sudo service mongod restart
rm mongo_util.js
rm assign_best_sellers.py
echo "Finished setting up mongoDB"
