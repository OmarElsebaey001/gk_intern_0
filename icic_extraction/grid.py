import re 
import pandas as pd
import pdfplumber
def get_text_from_pdf_with_plumber(apdf):
    tot = ''
    with pdfplumber.open(apdf) as pdf:
        for p in pdf.pages:
            tot += "\n"+p.extract_text()
    return tot 
def get_meta_from_contract(contract_cont):
    contract_note_no = re.findall("Contract Note No.*?:(.*)",contract_cont)[0]
    trade_date = re.findall ("TRADE DATE\s*?:\s*(\d{2}-\d{2}-\d{4}).*",contract_cont)[0]
    settlemnt_no = re.findall ("SETTLEMENT NO.*:\s*(\d+).*",contract_cont)[0]
    settlement_date = re.findall ("SETTLEMENT DATE.*:\s*(\d{2}-\d{2}-\d{4}).*",contract_cont)[0]
    mob_num = re.findall ("Mob No:\s*(\d*).*",contract_cont)[0]
    ucc_no = re.findall("UCC of Client\s*:\s*(\d*)",contract_cont)[0]
    pan_of_client = re.findall ("PAN of Client\s*:\s*(.*)",contract_cont)[0]
    meta_contract = [contract_note_no,trade_date,settlemnt_no,settlement_date,mob_num,ucc_no,pan_of_client]
    return meta_contract
def get_summary_table(contract_cont):
    seperate_summary_table = re.findall("Transaction Tax(.*?)\s*Brokerage Charges Charges.*?Buy(.*?)Sell(.*?)Total Payable / Receivable(.*?)\n",contract_cont,re.DOTALL)
    return seperate_summary_table
def get_detailed_table (contract_cont):
    seperate_detailed_table = re. findall("\d+\s+\d+\s+\d+\s+[\d{2}:\d{2}].*",contract_cont)
    return seperate_detailed_table
def extract_transaction_from_detailed_table(detailed_table):
    transactions=[]   
    for record in detailed_table :
        records_list = record.split()
        name = " ".join(records_list[5:len(records_list)-7])
        del records_list[5:len(records_list)-7]
        records_list.insert(5,name)
        transactions.append(records_list)
    return transactions
def extract_transaction_from_summary_table (summary_table):
    summary_table_data = []
    for transaction  in summary_table:
        clean_transaction = tuple(element.strip() for element in transaction)
        clean_transaction_lis = list(clean_transaction)
        company_name = clean_transaction_lis.pop(0)
        transaction_record = [x.split() for x in clean_transaction_lis ]
        transaction_record.insert(0,company_name)
        summary_table_data.append(transaction_record)
    return summary_table_data
def get_meta_table(contract_cont):
    pay_in_obligtion =re.findall("Pay in Obligation\s+.*(\d{5}\.\d+)",contract_cont)[0]
    exchange_trans_charges = re.findall(" Exchange Transaction Charges.*(\d+\.\d+)",contract_cont)[0]
    sebi_fees = re.findall("SEBI Turnover Fees.*(\d+\.\d+)",contract_cont)[0]
    total_taxable = re.findall("Total Taxable value of supply.*(\d+\.\d+)",contract_cont)[0]
    cgst = re.findall("CGST.*(\d+\.\d+)",contract_cont)[0]
    sgst = re.findall ("SGST.*(\d+\.\d+)",contract_cont)[0]
    igst = re.findall("IGST.*(\d+\.\d+)",contract_cont)[0]
    net_amount_payable = re.findall("Net amount payable by Client.*(\d{5}.\d+)",contract_cont)[0]
    meta_table = [pay_in_obligtion,exchange_trans_charges,sebi_fees,total_taxable,cgst,sgst,igst,net_amount_payable]
    return meta_table
def seperate_final_summary_table (contract_cont):
    summary_table_str = re.search("Transaction settled by delivery-Purchase.*Securities Transaction Tax .*?\n",contract_cont,re.DOTALL)[0]
    return summary_table_str
def extract_meta_summary_table(summary_table):
    total_meta_summary = re.findall("TOTAL.*\s+(\d+\.\d+).*",summary_table)[0]
    securties_meta_summary = re.findall("Securities Transaction Tax.*\s+(\d+\.\d+).*",summary_table)[0]
    return total_meta_summary,securties_meta_summary
def extract_transaction_summary_table (summary_table):
    transacton_summary_table = re.findall(".*\d+\s\d+\.\d+\s+\d+\.\d+",summary_table)
    records = [i.split() for i in transacton_summary_table]
    return records
def extract_final_summary_table(summary_table):
    meta_summary = extract_meta_summary_table(summary_table)
    transaction_summary = extract_transaction_summary_table(summary_table)
    return (transaction_summary,meta_summary)
def get_data_from_contract (contract_path):
    f_content = get_text_from_pdf_with_plumber(contract_path)
    meta_contract = get_meta_from_contract(f_content)
    summary_table_extraction = get_summary_table(f_content)
    detailed_table_extraction = get_detailed_table(f_content)
    transaction_detailed_table = extract_transaction_from_detailed_table(detailed_table_extraction)
    transaction_summary_table = extract_transaction_summary_table(summary_table_extraction)
    extra_meta = get_meta_table(f_content)
    final_summary_table = seperate_final_summary_table(f_content)
    final_summary_res = extract_final_summary_table(final_summary_table)
    final_res = [meta_contract,transaction_detailed_table,transaction_summary_table,extra_meta,final_summary_res]
    return final_res


