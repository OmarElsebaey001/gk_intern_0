import pytest
import sys
dyn_abs = "/".join(__file__.split('/')[0:-2])
sys.path.append(dyn_abs)
from icici_v0 import get_data_from_contract
import glob 
import os 
import filecmp
out_dir = dyn_abs+"/output_dir/"
if  os.path.exists(out_dir):
    shutil.rmtree(out_dir)
    os.mkdir(out_dir)
else :
    os.mkdir(out_dir)

files_list = glob.glob(dyn_abs+"/pdf_files/*.pdf")

@pytest.mark.parametrize("test_input", files_list)
def test_sanity(test_input):
    get_data_from_contract(test_input)

@pytest.mark.parametrize("test_input", files_list)
def test_functionality(test_input):
    res = get_data_from_contract(test_input)
    csv_file = os.path.basename(test_input).replace('.pdf','.csv')
    res.to_csv(out_dir+csv_file,index=False)
    assert filecmp.cmp(out_dir+csv_file, dyn_abs+"/golden/"+csv_file,shallow=True)
