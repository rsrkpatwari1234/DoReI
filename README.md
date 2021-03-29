# DoReI - doNate&Quest
## Bridge the gap to help the needy
DoReI is a Web Application through which people can donate and request for books and various stationery items (such as pens, pencils, bags etc) to
or from the organisation. It allows keeping records of all the donations, transactions and items donated or requested by users. It maintains these transactions at the software level while the physical transaction of collecting the books from donors and delivering them is verified by the managers of the application. Two seperate portals and interfaces for the user and manager helps in accomplishing this aim.

## Demo of the project
Demo of the application can be found at the youtube link : 

## Prerequisites :
- [Django](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Introduction)
- Front end development tools

## Testing :
- Used virtual python environment on a linux machine

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
 

