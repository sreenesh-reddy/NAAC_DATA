import pdfplumber
import pandas as pd
import os
from helper1 import extractState
from helper2 import extractGender
from helper3 import extractDate
# 📂 Directory containing PDFs
pdf_directory = "data2/Group_1"  
output_csv = "yellow.csv"  # Output CSV file

# ✅ Function to extract tables from PDF
def extract_tables_with_pdfplumber(pdf_path):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)  
                df.fillna("", inplace=True)  
                all_tables.append((page_num + 1, df))  
    return all_tables

# ✅ Filtering functions (same logic as before)
def select_required_tables1(tables):
    return [table for page_num, table in tables if not table.empty and table.shape[1] >= 2 
            and str(table.iloc[0, 0]).strip() == "" and str(table.iloc[0, 1]).strip() == "Date of submission"]

def select_required_tables2(tables):
    return [table for page_num, table in tables if not table.empty and table.shape[1] >= 2 
            and str(table.iloc[0, 0]).strip() == "1" and str(table.iloc[0, 1]).strip() == "Application For"]

def select_required_tables3(tables):
    for page_num, table in tables:
        if page_num == 2:
            return [table]
    return []

def select_required_tables4(tables):
    return [table for page_num, table in tables if not table.empty and table.shape[1] >= 2
            and str(table.iloc[0, 0]).strip().replace(".", "").isdigit()
            and str(int(float(table.iloc[0, 0]))) == "27"
            and str(table.iloc[0, 1]).startswith("Date of establishment of IQAC")]


# ✅ Process all PDFs in the directory
all_data = []
first_pdf = True  # Flag to write headers only for the first file

for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):  
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"📂 Processing: {pdf_file}")

        tables = extract_tables_with_pdfplumber(pdf_path)
        matching_tables = [select_required_tables1(tables), select_required_tables2(tables), 
                           select_required_tables3(tables), select_required_tables4(tables)]

        df1 = matching_tables[0][0]  
        df1_cleaned = df1[[1, 3]].dropna().reset_index(drop=True).T
        df1_cleaned.columns = df1_cleaned.iloc[0]  
        df1_cleaned = df1_cleaned[1:].reset_index(drop=True)  

        df2 = matching_tables[1][0]  
        df2_cleaned = df2.set_index(1).T.drop(0).reset_index(drop=True)  
        df2_cleaned.replace(r'\n', ' ', regex=True, inplace=True)  

        df3 = matching_tables[2][0].set_index(1).T.drop(0).reset_index(drop=True)  

        if 'Statutory Regulatory Authorities' in df3.columns:
            df3=df3.drop(columns=["Statutory Regulatory Authorities"])
        if "If the institution is not affiliated to a university and is\noffering programmes recognized by any Statutory\nRegulatory Authorities (SRA), are the programmes\nrecognized by Association of Indian Universities(AIU)\nor other appropriate Government authorities as\nequivalent to UG / PG Programmes of a University" in df3.columns:
            df3=df3.drop(columns=["If the institution is not affiliated to a university and is\noffering programmes recognized by any Statutory\nRegulatory Authorities (SRA), are the programmes\nrecognized by Association of Indian Universities(AIU)\nor other appropriate Government authorities as\nequivalent to UG / PG Programmes of a University"])


        # ✅ Extract state & gender data
        df4 = extractState(pdf_path).reset_index(drop=True)  
        df5 = extractGender(pdf_path).reset_index(drop=True)  

        # ✅ Extract Date of Establishment & MHRD Upload Date
        df8 =extractDate(pdf_path)

        df_combined = pd.concat([df1_cleaned, df2_cleaned, df3, df4, df5, df8], axis=1)
        all_data.append(df_combined)


def rename_duplicate_columns(df):
    seen = {}
    new_columns = []
    
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")  # Append a suffix
        else:
            seen[col] = 0
            new_columns.append(col)
    
    df.columns = new_columns
    return df

# Apply renaming to all DataFrames
all_data = [rename_duplicate_columns(df) for df in all_data]

finaldf=pd.concat(all_data,axis=0,ignore_index=True)
import numpy as np

finaldf.replace(r'^\s*$', np.nan, regex=True, inplace=True)
finaldf=finaldf.dropna(axis=1,how='all')
finaldf = finaldf.dropna(how='all')
finaldf.columns = finaldf.columns.str.strip()

print(finaldf)
finaldf.to_csv('yellow.csv', header=first_pdf, index=False)
print(f"\n✅ Data from all PDFs successfully saved to {output_csv}")
