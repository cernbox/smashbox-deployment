smashbox-deployment
========

This repository contains the scripts and documentation to easily deploy CERNBox client-testing configurations with smashbox framework. Analysis and visualization of test results can be monitor with kibana using the kibana-plugin in `smashbox/python/monitoring/kibana_monitoring.py`.

We deploy smashbox with the following purposes:
   * Regression-testing
   * Behaviour comparison of the sync client with different configurations: platforms, cernbox client versions and endpoints
   * Test the sync client installation on different platforms (e.g., Windows, CentOS, MacOSX)

Currently, it is possible to deploy smashbox in your current machine, a cluster of VMs in OpenStack or within a set of containers using Docker. Finally, this document also describes how to visualize and analyse the test results with kibana (instructions)

project tree   
=================

This repository is organised in the following way:

<pre>
   smashbox-deployment
   ├── documentation/         : procedures to manually set up a machine for continuos testing and monitoring
   ├── docker/                : scripts, docker files and configuration used to automatically deploy and continuosly run smashbox tests in a set of containers
   │   └── Dockerfiles/       : dockerfiles used to build different images for each platform
   │   └── setup.d            : these are the main scripts used to deploy the specified architecture
   ├── kibana/                : this folder contains json files that stores kibana dashboards configurations
   ├── setup/                 : this folder contains setup scripts and tools to automatically setup the machine
       └── auto-smashbox.conf : default configuration file for smashbox
       └── cbox_vers.json     : json table which contains all available cernbox client versions for each platform
       └── cleanup.py         : script to clean up space in Windows
       └── cleanup.sh         : script to clean up space in Linux/Mac
       └── get_vers.py        : script to extract correct cernbox version form json table
       └── linux_distr.py     : script to extract OS platform version
       └── setup.sh           : setup script for Linux-CC7
       └── ubuntu-setup.sh    : setup script for Linux-Ubuntu
       └── update_repo.py     : script to update smashbox repositor in Windows
       └── win-setup.py       : setup script for Windows
   └── README               : this file

</pre>

** `cbox_vers.json` is a table with 3 columns. 1st column is version for Linux, 2nd for MacOS and 3rd for Windows.

Instructions
=================
  - [Deploy and set up a testing cluster of VMs (Openstack)](#openstack)
    - [Windows setup](#windows)
    - [linux-CC7 setup](#cc7)
  - [Deploy and set up a testing cluster of containers (Docker)](#docker)
  - [Monitoring and Analysis with kibana](#monitoring)

<h3 id="openstack"> Deploy and set up a testing cluster of VMs (Openstack)</h3>

If you want to set up a machine for continuos testing and monitoring with smashbox, you can execute the corresponding setup script depending your OS. This script is developed to automatically and dinamically install the OwnCloud client, configure smashbox and install the cron job. The steps to use these scripts are the following:

** After creation of a new Windows VM you have to contact CDA to remove the machine form their automatic cernbox client update campaign.

<h4 id="windows"> WINDOWS </h4>

###### (1) Download and install python 2.7:
Python 2.7 is required. You can download it here: https://www.python.org/downloads/windows/ 

###### (2) Download and install git: 
You can download and install git here: https://git-scm.com/download/win

###### (3) Run git bash as administrator:
In Windows search tab search for 'Git Bash', right click and open as administrator

###### (4) Clone smashbox repository:
In git bash run: git clone https://github.com/cernbox/smashbox-deployment.git

###### (5) Modify if you need the time of cronjobs:
In `win-setup.py`, 2 variables run_time and cleanup_time indicate what time should the smashbox and cleaup processes run. You can modify them to the time you want.

###### (6) Open cmd as administrator:
In Windows search tab search for 'Command Prompt', right click and open as administrator

###### (7) Locate and change current directory in cmd:
Locate where you cloned the smashbox-deployment folder, from cmd `cd` in the `smashbox-deployment/setup/` folder

###### (8) Run setup script:
From cmd run the following command:
`C:\Python27\python.exe win-setup.py -v VERSION -u USERNAME -p PASSWORD -k KIBANA_ACTIVITY`

<h4 id="cc7"> LINUX-CC7 </h4>

###### (1) Install python 2.7:
Python 2.7 is required. If your machine is an openstack VM then python 2.7 is already installed. Else you need to download and install python 2.7.

###### (2) Install git:
In terminal run the following command: `sudo yum install git`

###### (3) Clone smashbox repository:
In terminal run the following command: git clone https://github.com/cernbox/smashbox-deployment.git

###### (4) Change current directory in terminal to the directory you cloned:
In terminal: `cd smashbox-deployment/setup/`

###### (5) Run setup script:
In terminal run the following command: `./setup.sh -v VERSION -u USERNAME -p PASSWORD -k KIBANA_ACTIVITY`

** `VERSION` is the cernbox client version you want, `USERNAME/PASSWORD` are your credentials for cernbox and `KIBANA_ACTIVITY` is variable so 'Kibana-Monitoring' can identify the data that are sent. It is described bellow in monitoring section.


<h3 id="docker">Deploy and set up a testing cluster of containers (Docker)</h3>

If you want to set up the cluster with containers. You should run the following commands:
```
docker build -t debian-smashbox
docker run -it -e SMASHBOX_OC_ACCOUNT_NAME="XXXX" -e  SMASHBOX_OC_ACCOUNT_PASSWORD="YYYYYY" -e SMASHBOX_OC_SERVER="cernbox.cern.ch" debian-smashbox:latest bash
```

The `docker build` should make reference to the dockerfile with the image desired to set up. Then, it is also neccesary to define the following environment variables:

```
  SMASHBOX_OS
  SMASHBOX_CLIENT_VERSION
  SMASHBOX_OC_SERVER
  SMASHBOX_OC_ACCOUNT_NAME
  SMASHBOX_OC_ACCOUNT_PASSWORD
  SMASHBOX_TESTDIR
  SMASHBOX_SSL_ENABLED
```

<h3 id="monitoring">Monitoring and Analysis with kibana</h3>

The goal of this section is to provide a convenient monitoring tool for the deployed smashbox testing architecture. For this purpose it has been choosen kibana for visualization and elasticsearch to store tests results.

In order to visualize the test results in kibana; first it is needed to provide the following parameters in `smashbox/etc/smashbox.conf`

  - **kibana_monitoring_host**. This is the host machine where you have running kibana. *For example: kibana_monitoring_host = "http://monit-metrics"*
  - **kibana_monitoring_port**. This is the port to communicate with ELK. *For example:  kibana_monitoring_port = "10012"*
  - **kibana_activity**. This is an additional parameter to be able to identify the data that you are sending to ELK. *For example: kibana_activity = "smashbox-regression"*

The kibana web interface is accessible in https://monit-kibana.cern.ch.

If you don't have yet the dashboard configured. You can download the json file `kibana\cernbox-smashbox.json`; then you need to go to the tab "management" in kibana and import this json file as a saved of object.

![Alt text](/kibana/img/import-kibana-dashboard.png?raw=true "import-kibana-dashboard")

The dashboard has been designed to monitor the failed tests running smashbox with different OwnCloud client versions and different platforms. For regression testing, tests are executed periodically according to the csv file provided in the deployment and the  schedule specified there.

![Alt text](/kibana/img/smashbox-dashboard.png?raw=true "smashbox-dashboard")

** Note: This section is based on the current deployed ELK architecture at CERN. In order to easily deploy an ELK architecture there is a document describing the procedure `kibana/elk-docker.pdf`.
