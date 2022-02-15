# Getting started with online-member-directory application

This project uses django framework

## Setup local environment

### python

install latest python

### virtual environment

Create a virtual environment using below command

python -m venv <set-a-name>

For example, python -m venv env

## activate virtual environment

linux / max => source env/bin/activate \
windows     => env/bin/activate.bat

command prompt should change for instance

[tmohan@sairam online-member-directory]$ source env/bin/activate \
(env) [tmohan@sairam online-member-directory]$

## install requirements packages

pip install -r requirements.txt

## launch the Application

1. python manage.py makemigrations
2. python manage.py migrate
3. python mange.py runserver

or if you have using linux or mac machine then run following commands

./simple.sh

## create .env file

create .env file and get the content of the file from your team members

## Reference documents

List of tasks are captured here (https://docs.google.com/spreadsheets/d/12-JFNXF-xMm4LTLOVvtU-hCHyq2TKfR3E-KI_g9BgjY/edit#gid=0)

## Data Model changes

Pull Request #44 changes data model of members table. If your local database has member table then  then do the following \
1. comment out Member data model in models.py file \
2. save and run ./simple.sh
3. git checkout main
4. git pull
5. run ./simple.sh command and this should create new member
6. using import utility import member_data.csv file
