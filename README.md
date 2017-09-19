# Logs Analysis

Third project from Udacity's [Full-Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### About

For this project I built a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.


### How to setup

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html).

Download data file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip, find ```newsdata.sql``` and put it in __vagrant__ directory (which is shared with your virtual machine).

Clone this repo into __vagrant__ folder:

```
cd vagrant
git clone https://github.com/dimak1/udacity-fsnd-project3.git
```

### How to run

Start virtual machine and log in to it:

```
cd vagrant
vagrant up
vagrant ssh
```

Once logged in, load the data and create database:
```
cd /vagrant
psql -d news -f newsdata.sql
```

Once created, run __logs-analysis.py__:
```
python3 logs-analysis.py
```

Program should connect to database, query the tables and print results as shown in ```output.txt```
