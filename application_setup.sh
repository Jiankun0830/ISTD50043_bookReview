echo -e "Installation script for Docker CE and nvidia-docker on Ubuntu 16+"

echo -e "Set non-interactive frontend"
echo -e "Script will run without any prompts"
export DEBIAN_FRONTEND=noninteractive

echo -e "\n###\n"
echo -e "Installing prerequisites for Docker CE"
echo -e "\n###\n"

apt-get update
apt-get remove docker docker-engine docker.io -y
apt-get install -y \
    apt-utils \
    apt-transport-https \
    ca-certificates \
    curl \
    wget \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

echo -e "\n###\n"
echo -e "Installing Docker CE"
echo -e "Version: latest stable"
echo -e "\n###\n"

apt-get update
apt-get install docker-ce -y

docker build -t python-docker-dev .
docker run --rm -it -p 8080:8080 python-docker-dev