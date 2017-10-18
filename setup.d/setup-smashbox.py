from crontab import CronTab
from sys import platform

########## Get environment variables ##########

oc_account_name = os.environ['SMASHBOX_OC_ACCOUNT_NAME']
oc_account_password = os.environ['SMASHBOX_OC_ACCOUNT_PASSWORD']
oc_server = os.environ['SMASHBOX_OC_SERVER']


########## Smashbox config file ##########

os.system("cp ./auto-smashbox.conf ./smashbox/etc/smashbox.conf")
f = open('./smashbox/etc/smashbox.conf', 'a')

f.write('oc_account_name =' + '"{}"'.format(oc_account_name) + '\n')
f.write('oc_account_password =' + '"{}"'.format(oc_account_password) + '\n')
f.write('oc_server =' + '"{}"'.format(oc_server + "/cernbox/desktop") + '\n')

if oc_server=='cernbox.cern.ch':
    f.write('oc_ssl_enabled =' + "True" + '\n')
else:
    f.write('oc_ssl_enabled =' + "False" + '\n')

if platform == "linux" or platform == "linux2":  # linux
    if client_choice == "1": # cernbox
        location = os.popen("whereis cernboxcmd").read()
        path = "/" + location.split("cernboxcmd")[1].split(": /")[1] + "cernboxcmd --trust"
elif platform == "darwin":
        path = "/Applications/cernbox.app/Contents/MacOS/cernboxcmd --trust"
elif platform == "Windows":
    if client_choice == "1": # cernbox
        location = os.popen("where cernboxcmd").read()
        path = "/" + location.split("cernboxcmd")[1].split(": /")[1] + "cernboxcmd --trust" # to be changed

f.write("oc_sync_cmd =" + '"{}"'.format(path))

f.close()


########## Set up cron job ############

user = os.popen("echo $USER").read().split("\n")[0]
my_cron = CronTab(user)
current_path = os.path.dirname(os.path.abspath(__file__))
job = my_cron.new(command="python " + current_path + "/smash-run.py")
job.setall('00 18 * * *')
my_cron.write()

print("Tests results will be written in: ./smashbox/etc/smashdir \n")
print("Results are also sent to the smashbox dashboard in monit kibana service: https://monit-kibana.cern.ch")
