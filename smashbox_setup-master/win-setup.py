import sys, os, subprocess, shutil, argparse

run_time="16:55"
cleanup_time="10:00"


def install_and_import(pkg):
    import importlib, site
    
    os.system(sys.executable + " -m easy_install " + pkg)

    reload(site)
    importlib.import_module(pkg)
    globals()[pkg] = importlib.import_module(pkg)


def get_vers(vers):
    proc = subprocess.Popen(["\Python27\python.exe", os.path.join(os.getcwd(), "get_vers.py"), "-v", vers], stdout=subprocess.PIPE, shell=True)
    (out, err)=proc.communicate()
    if proc.returncode != 0:
        print out
        sys.exit(1)
    else:
        return out.rstrip()


def install_cernbox(vers):
    print '\033[94m' + "Installing cernbox client " + vers + " for Windows" + '\033[0m' + '\n'
    wget.download("https://cernbox.cern.ch/cernbox/doc/Windows/cernbox-" + vers +"-setup.exe")
    os.system("cernbox-" + vers +"-setup.exe /S")
    os.remove("cernbox-" + vers +"-setup.exe")


def get_repo():
    wget.download("https://github.com/cernbox/smashbox/archive/master.zip")
    
    import zipfile
    with zipfile.ZipFile("smashbox-master.zip", 'r') as zip_ref:
        zip_ref.extractall("C:\\")

    os.remove("smashbox-master.zip")


def install_cron_job(endpoint):
    import sys

    print '\n' + '\033[94m Installing cron job for smashbox execution \033[0m'  + '\n'
    this_exec_path = os.path.join("C:\\", "Python27", "python.exe")
    this_exec_path += " " + os.path.join("C:\\", "smashbox-master", "bin", "smash")
    this_exec_path += " -a -d --keep-going " + os.path.join("C:\\", "smashbox-master", "lib")
    this_exec_path += " -c " + os.path.join("C:\\", "smashbox-master", "etc", "smashbox-" + endpoint + ".conf")
    print this_exec_path

    cmd = "schtasks /Create /SC DAILY /RU system /TN Smashbox-" + endpoint + " /RL HIGHEST /ST " + run_time + " /TR " + '"' + this_exec_path + '"' + " /F" # /F is to force the overwrite of the existing scheduled task
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if (len(stderr) > 0):
        print "The task cannot be created on Windows - ", stderr
    else:
        print "The task has been successfully installed"


def cron_cleanup():
    print '\n' + '\033[94m Installing cron job for cleanup \033[0m'  + '\n'
    this_exec_path = os.path.join("C:\\", "Python27", "python.exe")
    this_exec_path += " " + os.path.join("C:\\", "smashutil", "cleanup.py")

    cmd = "schtasks /Create /SC DAILY /RU system /TN Smashbox-Cleanup /RL HIGHEST /ST " + cleanup_time + " /TR " + '"' + this_exec_path + '"' + " /F"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if (len(stderr) > 0):
        print "The task cannot be created on Windows - ", stderr
    else:
        print "The task has been successfully installed"


def cron_update_repo():
    print '\n' + '\033[94m Installing cron job for repo update \033[0m'  + '\n'
    this_exec_path = os.path.join("C:\\", "Python27", "python.exe")
    this_exec_path += " " + os.path.join("C:\\", "smashutil", "update_repo.py")

    cmd = "schtasks /Create /SC DAILY /RU system /TN Smashbox-Update_Repo /RL HIGHEST /ST 10:30 /TR " + '"' + this_exec_path + '"' + " /F"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if (len(stderr) > 0):
        print "The task cannot be created on Windows - ", stderr
    else:
        print "The task has been successfully installed"


def get_oc_sync_cmd_path():
    return ['C:\Program Files (x86)\cernbox\cernboxcmd.exe', '--trust']


def generate_config_smashbox(oc_account_name, oc_account_password, endpoint, ssl_enabled, kibana_activity):
    new_smash_conf = os.path.join("C:\\", "smashbox-master", "etc", "smashbox-" + endpoint + ".conf")
    shutil.copyfile(os.path.join(os.getcwd(), "auto-smashbox.conf"), new_smash_conf)
    f = open(new_smash_conf, 'a')

    f.write('oc_account_name = ' + oc_account_name + '\n')
    f.write('oc_account_password = ' + oc_account_password + '\n')
    f.write('oc_server = ' + '"{}"'.format(endpoint + ".cern.ch" + "/cernbox/desktop") + '\n')
    f.write('oc_ssl_enabled = ' + ssl_enabled + '\n')

    oc_sync_path = get_oc_sync_cmd_path()
    f.write('oc_sync_cmd = ' + str(oc_sync_path) + '\n')
    f.write('kibana_activity = ' + '"{}"'.format(kibana_activity) + '\n')

    f.close()


def check_privileges():
    print("Administrative permissions required. Detecting permissions..." + '\n')
    error = 0

    error = os.system("net session >nul 2>&1")
    if error !=0:
        print "Failure: Current permissions inadequate." + '\n'
        exit(0)
    else:
        print "Success: Administrative permissions confirmed!" + '\n'





parser=argparse.ArgumentParser(description='Get wanted version and return folder name')

parser.add_argument('--vers', '-v', dest="version", action="store", type=str, help='cernbox wanted version')
parser.add_argument('--username', '-u', dest="username", action="store", type=str, help='cernbox client username')
parser.add_argument('--password', '-p', dest="password", action="store", type=str, help='cernbox client password')
parser.add_argument('--kibana_activity', '-k', dest="kibana_activity", action="store", type=str, help='kibana activity')

args = parser.parse_args()

if not args.version:
    print "Pease specify cernbox wanted version ie. -v 2.3.3"
    sys.exit(1)

if not args.username:
    print "Pease specify cernbox client username ie. -u USERNAME"
    sys.exit(1)
else:
    username = "'" + args.username + "'"

if not args.password:
    print "Pease specify cernbox client password ie. -p PASSWORD"
    sys.exit(1)
else:
    password = "'" + args.password + "'"

if not args.kibana_activity:
    print "Pease specify kibana activity ie. -k KIBANA_ACTIVITY"
    sys.exit(1)




check_privileges()

install_and_import('wget')
install_and_import('pycurl')
install_and_import('requests')

vers = get_vers(args.version)

install_cernbox(vers)

get_repo()

shutil.copyfile(os.path.join(os.getcwd(), "auto-smashbox.conf"), os.path.join("C:\\", "smashbox-master", "etc", "smashbox.conf"))
generate_config_smashbox(username, password, "cernbox", "True", args.kibana_activity)

install_cron_job("cernbox")

smashutil_path = os.path.join("C:\\", "smashutil")
if not os.path.exists(smashutil_path):
    print smashutil_path
    os.makedirs(smashutil_path)

shutil.copyfile(os.path.join(os.getcwd(), "cleanup.py"), os.path.join("C:\\", "smashutil", "cleanup.py"))
cron_cleanup()

shutil.copyfile(os.path.join(os.getcwd(), "update_repo.py"), os.path.join("C:\\", "smashutil", "update_repo.py"))
cron_update_repo()
