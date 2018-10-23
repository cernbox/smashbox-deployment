import sys, os, shutil

def install_and_import(pkg):
    import importlib, site
    
    os.system(sys.executable + " -m easy_install " + pkg)

    reload(site)
    importlib.import_module(pkg)
    globals()[pkg] = importlib.import_module(pkg)


import os
path = os.path.join("C:\\", "smashbox-master", "etc")
if os.path.exists(path):
    for f in os.listdir(path):
        if f.startswith('smashbox') and f.endswith('.conf'):
            print f
            shutil.move(os.path.join(path, f), os.path.join("C:\\", "smashutil", f))
        
        


install_and_import('wget')

if os.path.exists("C:\\smashbox-master"):
    shutil.rmtree("C:\\smashbox-master")

wget.download("https://github.com/cernbox/smashbox/archive/master.zip")
    
import zipfile
with zipfile.ZipFile("smashbox-master.zip", 'r') as zip_ref:
    zip_ref.extractall("C:\\")

os.remove("smashbox-master.zip")

path = os.path.join("C:\\", "smashutil")
for f in os.listdir(path):
    if f.startswith('smashbox') and f.endswith('.conf'):
        print f
        shutil.move(os.path.join(path, f), os.path.join("C:\\", "smashbox-master", "etc", f))
