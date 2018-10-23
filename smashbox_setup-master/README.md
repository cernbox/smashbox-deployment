# smashbox_setup

SETUP SMASHBOX IN WINDOWS

1. Download and install python 2.7 form here: https://www.python.org/downloads/windows/
2. Download smashbox reposiroty form here: https://github.com/giorgosalex/smashbox_setup
3. Extract the zipped file
4. (Modify if you need the time of cronjobs install in win-setup.py: in win-setup.py 2 vars run_time and cleanup_time )
5. Open cmd as administrator
6. cd in the smashbox_setup-master you downloaded and extracted
7. Run: "C:\Python27\python.exe win-setup.py -v VERSION -u USERNAME -p PASSWORD -k KIBANA_ACTIVITY"

Where VERSION is the cernbox version you want (ie. 2.4.2), USERNAME/PASSWORD your cernbox credentials

ALTERNATIVE:

1. Download and install python 2.7 form here: https://www.python.org/downloads/windows/
2. Download and install git: https://git-scm.com/download/win
3. Run git bash as administrator
4. Clone smashbox repository: https://github.com/giorgosalex/smashbox_setup
5. Do steps 4, 5, 6, 7, mentioned above


TO SEE THE CRONJOBS:
in search tab search for 'task scheduler' and run as administrator.
there you will find a cronjob with the name of 'smashbox-cernbox'
if you click it you have some options on the right to run/stop 
You can also modify some attributes by right clicking and going to properties


SETUP SMASHBOX IN CC7

Run the following commands as root:
1. yum install git
2. git clone https://github.com/giorgosalex/smashbox_setup.git
3. cd smashbox_setup/
4. ./setup.sh -v VERSION -u USERNAME -p PASSWORD -k KIBANA_ACTIVITY

CRONJOBS:
crontab -l to see all cronjobs
crontab -e to modify them

Where VERSION is the cernbox version you want (ie. 2.4.2), USERNAME/PASSWORD your cernbox credentials
