# DoReI
## Bridge the gap to help the needy
EchoForMe is a Web Application that reads out the latest news to the user.It is designed especially for visually impaired people to help them by reading out the daily news to them.It is a user-friendly application that can be used by people of all generations.It seeks to address challenges faced by physically challenged people or children while learning,people who focus more on verbal concepts of teaching and also for those who wish to learn the way of recitation and pronunciation of english language words.

## Demo of the project
Demo of the application can be found at the youtube link : 

## Prerequisites :
- [Django](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Introduction)
- Front end development tools
- Tested on linux machine

## Setting Up virtual Python3 environment
1.Follow the commands to create a environemnt "env" and activate it
```
sudo apt-get install python3.7-venv
python3.7 -m venv env
```

2.Activate the environment using the command below
```
source env/bin/activate
```
3.Install the required libraries in the virtual environment
```
pip3 install -r requirements.txt
```
4.To deactivate the environment,use
```
deactivate
```
## Setting up the project
1.Please follow the above steps to set up the virtual environment if you haven't already

2.Initialise the directory for git and clone the repository using the following command
```
git clone https://github.com/rsrkpatwari1234/DoReI.git
```
3.Activate the virtual environment from wherever you have made it
```
source env/bin/activate
```
3.Follow the below commands to set up the database with the required tables [in the same directory where you did step 2]
```
cd DoReI
python3 manage.py makemigrations
python3 manage.py migrate
```
4.Start the Django server using the below command
```
python3 manage.py runserver 
```
5.Follow the URL dispalyed and you will be directed to the website

## Organisation 
This project is created as a part of the Database and Management Course [CS43002] of IIT Kharagpur
 

