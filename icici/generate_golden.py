from icic_v0 import get_data_from_contract
import glob 
import os 

files_list = glob.glob("icici_cont/*.pdf")
for i in files_list : 
    res = get_data_from_contract(i)
    final = "golden/"+os.path.basename(i).replace(".pdf",".csv")
    print("Saving to : ", final )
    res.to_csv(final,index=False)