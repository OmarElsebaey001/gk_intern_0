import re
from xml.dom.minidom import Element 
import pandas as pd
import pdfplumber
import glob
def get_text_from_pdf_with_plumber(apdf):
    tot = ''
    with pdfplumber.open(apdf) as pdf:
        for p in pdf.pages:
            tot += "\n"+p.extract_text()
    return tot 

files = glob.glob('icici_cont/*.pdf')
#for i in files:
   #print(get_text_from_pdf_with_plumber(i))
all = open("res.txt",'r').readlines()
for i,v in enumerate(all): 
    if bool(re.match("^Buy ",v)) :
        print(all[i-1].strip())