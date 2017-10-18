import os
import time
import shutil

threshold = 10000000000
current_path = os.path.dirname(os.path.abspath(__file__))

prev_result = int((os.popen("du -b " + current_path + "/smashbox/etc/smashdir").read()).split("\t")[0])

if(result>threshold):
   shutil.rmtree("./smashbox/etc/smashdir")
   # to do backup test results and update smashbox repository

# check if smashbox has started
while(prev_result==result):
      os.system("python " + current_path + "/smashbox/bin/smash --keep-going -a " + current_path + "/smashbox/lib/")
      result = int((os.popen("du -b " + current_path + "/smashbox/etc/smashdir").read()).split("\t")[0])

