sudo apt update
sudo apt -y install python3
sudo apt -y install python3-pip

cd ../src/

pip3 install -r requirements.txt

sudo python3 app.py
