
FROM python:3.10.0

#creating WORKDIR inside of image
WORKDIR /project

#adding the directory to our image
ADD . /project

#installing the packages(dependencies) required for our flask application into the image
RUN pip install -r requirements.txt

#running the flask app in a container
CMD ["python", "main.py"]































#will be utilizing an ubuntu image
#FROM ubuntu:16.04 

#installing python packages within our ubuntu image
#RUN apt-get update -y && \ 
 #   apt-get install -y python-pip python-dev

#COPY requirements.txt .

#installing the packages into our ubuntu image
#RUN pip install -r requirements.txt








#FROM python:3.10.0

#Making a directory for our application
#WORKDIR /application

#installing dependencies/packages into our docker image
#COPY requirements.txt .

#downloading dependecies into image
#RUN pip install -r requirements.txt

#Copying Source Code
#COPY main.py .
#COPY user.py .

#Running the application
#CMD ["python", "main.py"]
