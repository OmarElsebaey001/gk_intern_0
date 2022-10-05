import glob
import time
import os 
import shutil
import traceback
from contextlib import redirect_stdout
from grid import get_data_from_contract

files = glob.glob('icici_cont/*.pdf')
dir = os.path.join("output_dir")
if  os.path.exists(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)
else :
    os.mkdir(dir)
dir_error = os.path.join("errors")
if  os.path.exists(dir_error):
    shutil.rmtree(dir_error)
    os.mkdir(dir_error)
else :
    os.mkdir(dir_error)
passed = 0
fail_sanity = 0 

for file in files : 
    try:
        print("Processing: ", file)
        start = time.time()
        name = file.replace("icici_cont/","")
        name = name.replace("pdf",".txt")
        df = str( get_data_from_contract(name))
        with open("output_dir/"+name, "w") as f:
            f.write(df)
        end = time.time()
        print("Time:",round((end- start),2),"seconds")
        passed+=1
    except ValueError  :
        tb = traceback.format_exc()
        name = file.replace("cici_cont/","")
        name = name.replace(".PDF",".log") 
        print ("excption ocuured for file :",name)
        with open ("errors\\" + name ,"w") as f:
            f.write(tb)
            fail_sanity += 1
print(f"Current: PASS={passed} FAIL_S={fail_sanity}")