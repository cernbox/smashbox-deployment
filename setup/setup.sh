#!/bin/bash

if [[ $# -ne 8 ]]; then
    echo "You must give exactly 8 arguments. Use: ./setup.sh -v VERSION -u USERNAME -p PASSWORD -k KIBANA_ACTIVITY"
    exit
fi

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -v|--version) #owncloud client version
    VERSION="$2"
    shift # past argument
    shift # past value
    ;;
    -u|--username) #owncloud client account name
    USERNAME="$2"
    shift
    shift
    ;;
    -p|--password) #owncloud client account password
    PASSWORD="$2"
    shift
    shift
    ;;
    -k|--kibana_activity) #kibana activity
    K_ACTIVITY="$2"
    shift
    shift
    ;;
    *)    # unknown option
    echo $1 ": no such option"
    exit
    ;;
esac
done

vers=$(python get_vers.py -v $VERSION)
echo $vers

if [[ $? != 0 ]]; then
    echo "failed: $vers" 
    exit
fi


DISTR=$(python linux_distr.py)

yum install wget -y
yum install git -y

wget http://cernbox.cern.ch/cernbox/doc/Linux/centos$DISTR-cernbox.repo
mv centos$DISTR-cernbox.repo /etc/yum.repos.d/cernbox.repo

sed -i s+/repo/+/$vers/+g /etc/yum.repos.d/cernbox.repo

yum update -y
yum install cernbox-client -y

rm /etc/yum.repos.d/cernbox.repo

git clone https://github.com/cernbox/smashbox.git /root/smashbox/

CURRENT_PATH=$(pwd)
CERNBOX_CONF_PATH='/root/smashbox/etc/smashbox-cernbox.conf'
TESTBOX_CONF_PATH='/root/smashbox/etc/smashbox-testbox.conf'
cp $CURRENT_PATH/auto-smashbox.conf $CERNBOX_CONF_PATH

echo "oc_account_name = '$USERNAME'" >> $CERNBOX_CONF_PATH
echo "oc_account_password = '$PASSWORD'" >> $CERNBOX_CONF_PATH
echo "oc_ssl_enabled = True" >> $CERNBOX_CONF_PATH
echo 'oc_sync_cmd = "/usr/bin/cernboxcmd --trust"' >> $CERNBOX_CONF_PATH
echo 'kibana_activity = "'$K_ACTIVITY'"' >> $CERNBOX_CONF_PATH

cp $CERNBOX_CONF_PATH $TESTBOX_CONF_PATH
echo 'oc_server = "cernbox.cern.ch/cernbox/desktop"' >> $CERNBOX_CONF_PATH
echo 'oc_server = "testbox.cern.ch/cernbox/desktop"' >> $TESTBOX_CONF_PATH
touch /root/smashbox/etc/smashbox.conf

crontab -l > mycron
echo "00 20 * * * python /root/smashbox/bin/smash --keep-going -a -d /root/smashbox/lib/test_* -c /root/smashbox/etc/smashbox-cernbox.conf" >> mycron
echo "00 23 * * * python /root/smashbox/bin/smash --keep-going -a -d /root/smashbox/lib/test_* -c /root/smashbox/etc/smashbox-testbox.conf" >> mycron

cp $CURRENT_PATH/cleanup.sh /root/smashbox/
echo "00 10 * * * /root/smashbox/cleanup.sh" >> mycron

crontab mycron
rm mycron

