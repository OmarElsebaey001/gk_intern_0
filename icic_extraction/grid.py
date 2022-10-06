import re
from tkinter import Y
from xml.dom.minidom import Element 
import pandas as pd
import pdfplumber
import glob 
from difflib import SequenceMatcher 
import pandas as pd

def get_text_from_pdf_with_plumber(apdf):
    tot = ''
    with pdfplumber.open(apdf) as pdf:
        for p in pdf.pages:
            tot += "\n"+p.extract_text()
    return tot 
x =get_text_from_pdf_with_plumber("/Users/mostafazeiada/Desktop/mostafa/gk_intern_0/icic_extraction/icici_cont/12272021.pdf")
def get_meta_from_contract(contract_cont):
    """
    This function to get meta data for contract
    and it return alist of basic inf for contract
    """
    contract_note_no = re.findall("Contract Note No.*?([a-zA-Z0-9]*\/\d+\/\d+)",contract_cont)[0].strip()
    trade_date = re.findall ("TRADE DATE\s*?:\s*(\d{2}-\d{2}-\d{4}).*",contract_cont)[0]
    settlement_date = re.findall ("SETTLEMENT DATE.*?(\d+-\d+-\d+).*",contract_cont)[0]
    mob_num = re.findall ("Mob No:\s*(\d*).*",contract_cont)[0]
    ucc_no = re.findall("UCC of Client\s*:\s*(\d*)",contract_cont)[0]
    pan_of_client = re.findall ("PAN of Client\s*:\s*(.*)",contract_cont)[0]
    meta_contract = [contract_note_no,trade_date,settlement_date,mob_num,ucc_no,pan_of_client]
    return meta_contract
def get_summary_table_list(contract_cont):
    seperate_summary_table= re.findall("(.*)Service Tax.*\n(Buy.*)\n(Sell.*)?\n",contract_cont,)
    #buy = "Sell  0 0.00 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000"
    #sell = "Sell  0 0.00 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000"
    return seperate_summary_table

def get_detailed_table_list (contract_cont):
    seperate_detailed_table = re. findall("\d{2}:\d{2}.*(?:Buy|Sell).*",contract_cont)
    return seperate_detailed_table
def extract_transaction_from_detailed_table(detailed_table):
    """
    Input is detailed tables list 
    and it return  list of detailed tables data
    """
    transactions=[]   
    for record in detailed_table :
        record_clean = re.sub("NSE","",record)
        record_clean = re.sub('BSE',"",record_clean)
        numbers = re.findall("(?:Sell|Buy)\s+\d+\s+\d+\.\d+.*",record)[0].split()
        mini_meta = re.findall("(.*)(?:Sell|Buy)\s+\d+\s+\d+\.\d+.*",record)[0].split()
        records_list = mini_meta+numbers
        name = " ".join(records_list[2:len(records_list)-6])
        del records_list[2:len(records_list)-6]
        records_list.insert(2,name)
        transactions.append(records_list)
    return transactions
def extract_transaction_from_summary_table (summary_table):
    """
    input is summary table list 
    and it returns list of summary table data
    """
    summary_table_data = []
    for transaction  in summary_table:
        clean_transaction = tuple(element.strip() for element in transaction)
        clean_transaction = tuple(Element.replace("Brokerage Charges","")for Element in clean_transaction)
        clean_transaction = tuple(Element.replace("Charges","")for Element in clean_transaction)
        clean_transaction = tuple(Element.replace("and Clearing","")for Element in clean_transaction)
        clean_transaction_lis = list(clean_transaction)
        company_name = clean_transaction_lis.pop(0)
        transaction_record = [x.split() for x in clean_transaction_lis ]
        transaction_record.insert(0,company_name)
        summary_table_data.append(transaction_record)
    return summary_table_data

def clean_trans_summary(sum_update):
    res = []
    for i in sum_update:
        if i[1][1]!= "0":
            res.append(i[1]+[i[0],i[-1]])
        if i[2][1] != "0":
            res.append(i[2]+[i[0],i[-1]])
    return res

def flatten_transaction_table (meta,clean_trans):
    return [i+meta for i in clean_trans]

def get_totals_table(contract_cont):
    pay_in_obligtion = re.findall("Pay\s.*(?:in|out) Obligation\s+.*?(\d+\.\d+)",contract_cont)[0]
    if len (re.findall("Exchange Transaction .*Charges.*?(\d+\.\d+)",contract_cont)) == 0 :
        exchange_trans_charges = 0 
    else :
        exchange_trans_charges = re.findall("Exchange Transaction .*Charges.*?(\d+\.\d+)",contract_cont)[0]
    if len (re.findall("SEBI Turnover Fees.*?(\d+\.\d+)",contract_cont)) == 0 :
        sebi_fees = 0 
    else :
        sebi_fees = re.findall("SEBI Turnover Fees.*?(\d+\.\d+)",contract_cont)[0]
    if len (re.findall("Total Taxable value of supply.*?(\d+\.\d+)",contract_cont))==0:
        total_taxable = 0 
    else :
        total_taxable = re.findall("Total Taxable value of supply.*?(\d+\.\d+)",contract_cont)[0]
    if len (re.findall("CGST.*(\d*\.\d+)",contract_cont)) == 0 :
        cgst = 0 
    else : 
        cgst = re.findall("CGST.*?(\d*\.\d+)",contract_cont)[0]
    if len(re.findall ("SGST.*(\d*\.\d+)",contract_cont)) == 0 :
        sgst = 0 
    else : 
        sgst = re.findall ("SGST.*?(\d*\.\d+)",contract_cont)[0]
    if len(re.findall("IGST.*(\d*\.\d+)",contract_cont)) == 0 : 
        igst = 0 
    else : 
        igst = re.findall("IGST.*?(\d*\.\d+)",contract_cont)[0]
    if len(re.findall("Net amount (?:payable|receivable) by Client.*?(\d+\.\d+)",contract_cont))== 0:
        net_amount_payable = 0
    else :
        net_amount_payable = re.findall("Net amount (?:payable|receivable) by Client.*?(\d+\.\d+)",contract_cont)[0]
    
    meta_table = [pay_in_obligtion,exchange_trans_charges,sebi_fees,total_taxable,cgst,sgst,igst,net_amount_payable]
    return meta_table
def seperate_final_summary_table (contract_cont):
    summary_table_str = re.search("Transaction settled by delivery-Purchase.*Securities Transaction Tax .*?\n",contract_cont,re.DOTALL)[0]
    return summary_table_str
def extract_meta_summary_table(summary_table):
    total_meta_summary = re.findall("TOTAL.*\s+(\d+\.\d+).*",summary_table)[0]
    securties_meta_summary = re.findall("Securities Transaction Tax.*\s+(\d+\.\d+).*",summary_table)[0]
    return total_meta_summary,securties_meta_summary
def extract_transaction_final_summary_table (summary_table):
    transacton_summary_table = re.findall(".*\d+\s\d+\.\d+\s+\d+\.\d+",summary_table)
    records = [i.split() for i in transacton_summary_table]
    return records
def extract_final_summary_table(summary_table):
    meta_summary = extract_meta_summary_table(summary_table)
    transaction_summary = extract_transaction_final_summary_table(summary_table)
    return (transaction_summary,meta_summary)

def transform_detailed_table_to_name_isin_dict(tb):
    adict = {}
    for i in tb:
        adict[i[2]] = i[1]
    return adict 

def map_src_to_dst(res):
    src = []
    dest = []
    adict = {}
    for i in res:
        if not(i[1] in src) and not(i[2] in dest):
            src.append(i[1])
            dest.append(i[2])
            adict[i[1]] = i[2]
    return adict
def generate_match_percentage(summ_names,trans_names):
    res = []
    for i in summ_names : 
        for j in trans_names : 
            match0 = 100*round(SequenceMatcher(None, i.lower(), j.lower()).ratio(),2)
            res.append([match0,i,j])
    res.sort(reverse=True)
    return res 

def get_detailed_name(s,d):
    res = generate_match_percentage(s,d)
    adict = map_src_to_dst(res)
    return adict

def update_summary_with_fetched_isin(st,ddict):
    for i in st :
        name = i[0].strip()
        try:
            isin = ddict[name]
        except:
            res = get_detailed_name([name],ddict.keys())
            isin = ddict[res[name]]
        i.append(isin)
    return st

def get_data_from_contract (contract_path):
    f_content = get_text_from_pdf_with_plumber(contract_path)
    meta_contract = get_meta_from_contract(f_content)
    summary_table_extraction = get_summary_table_list(f_content)
    detailed_table_extraction = get_detailed_table_list(f_content)
    transaction_detailed_table = extract_transaction_from_detailed_table(detailed_table_extraction)
    trans_table_dict = transform_detailed_table_to_name_isin_dict(transaction_detailed_table)
    transaction_summary_table = extract_transaction_from_summary_table(summary_table_extraction)
    summary_table_updated = update_summary_with_fetched_isin(transaction_summary_table,trans_table_dict)
    clean_summ = clean_trans_summary(summary_table_updated)
    flatten_trans = flatten_transaction_table(meta_contract,clean_summ)
    contract_df = pd.DataFrame(flatten_trans)
    cols = ['Trans_Type','Quantity','Gross_Value','Total_Brokerage','Exchange_Trans_Charges','SEBI','Total_GST','Stamp_Duty','STT','Net_Payable_Recievable']
    cols += ['Company','ISIN','ContracT_Note_No','Trade_Date','Settlement_Date','Mobile_No','UCC','PAN']
    contract_df.columns = cols
    return contract_df

if __name__ == "__main__" : 
    files = glob.glob('icici_cont/*.pdf')
    tot = pd.DataFrame()
    for i in files:
        print("Contract: ", i )
        try:
            res = get_data_from_contract(i)
            res['file'] = "/Users/mostafazeiada/Desktop/mostafa/gk_intern_0/icic_extraction/icici_cont/" + i
            tot = pd.concat([tot,res])
        except:
            print("FAILED ON : ", i )
        print("="*30)
    tot.to_csv("ici_x.csv",index=False)


