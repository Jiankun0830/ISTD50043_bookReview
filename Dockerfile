# python-app
# ├── Dockerfile
# └── src
#     └── app.py
#     └── requirements.txt

FROM python:3.6

MAINTANER jiankun_lu@mymail.sutd.edu.sg

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# Create app directory
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./

RUN pip3 install -r requirements.txt

# Bundle app source
COPY src /app

EXPOSE 8080
CMD [ "python3", "app.py" ]