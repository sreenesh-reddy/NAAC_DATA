import pdfplumber
import pandas as pd
import os
from helper1 import extractState
from helper2 import extractGender

# 📂 Directory containing PDFs
pdf_directory = "test"  
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



def select_exception(tables):
    selected_tables = []
    for page_num, table in tables:
        # print(table)
        # print('-'*50)
        if table.empty or table.shape[0] < 1 or table.shape[1] < 2:
            continue  # Skip empty or malformed tables

        first_cell = str(table.iloc[0, 0]).strip()  # First row, first column
        second_cell = str(table.iloc[0, 1]).strip()  # First row, second column

        # ✅ Use .startswith() for partial matches
        if first_cell == "Date":
            selected_tables.append(table)  # ✅ Append the full table, not just first few rows!

    return selected_tables


def select_exception2(tables):
    selected_tables = []
    for page_num, table in tables:
        # print(table)
        # print('-'*50)
        if table.empty or table.shape[0] < 1 or table.shape[1] < 2:
            continue  # Skip empty or malformed tables

        first_cell = str(table.iloc[0, 0]).strip()  # First row, first column
        second_cell = str(table.iloc[0, 1]).strip()  # First row, second column

        # ✅ Use .startswith() for partial matches
        if first_cell == "25":
            selected_tables.append(table)  # ✅ Append the full table, not just first few rows!

    return selected_tables


def select_exception3(tables):
    selected_tables = []
    for page_num, table in tables:
        # print(table)
        # print('-'*50)
        if table.empty or table.shape[0] < 1 or table.shape[1] < 2:
            continue  # Skip empty or malformed tables

        first_cell = str(table.iloc[0, 0]).strip()  # First row, first column
        second_cell = str(table.iloc[0, 1]).strip()  # First row, second column

        # ✅ Use .startswith() for partial matches
        if first_cell == "23":
            selected_tables.append(table)  # ✅ Append the full table, not just first few rows!

    return selected_tables

def select_exception4(tables):
    selected_tables = []
    for page_num, table in tables:
        # print(table)
        # print('-'*50)
        if table.empty or table.shape[0] < 1 or table.shape[1] < 2:
            continue  # Skip empty or malformed tables

        first_cell = str(table.iloc[0, 0]).strip()  # First row, first column
        second_cell = str(table.iloc[0, 1]).strip()  # First row, second column

        # ✅ Use .startswith() for partial matches
        if first_cell == "26":
            selected_tables.append(table)  # ✅ Append the full table, not just first few rows!

    return selected_tables

def select_exception5(tables):
    selected_tables = []
    for page_num, table in tables:
        # print(table)
        # print('-'*50)
        if table.empty or table.shape[0] < 1 or table.shape[1] < 2:
            continue  # Skip empty or malformed tables

        first_cell = str(table.iloc[0, 0]).strip()  # First row, first column
        second_cell = str(table.iloc[0, 1]).strip()  # First row, second column

        # ✅ Use .startswith() for partial matches
        if first_cell == "24":
            selected_tables.append(table)  # ✅ Append the full table, not just first few rows!

    return selected_tables


# ✅ Process all PDFs in the directory
all_data = []
first_pdf = True  # Flag to write headers only for the first file

for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):  
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"📂 Processing: {pdf_file}")

        # ✅ Extract tables
        tables = extract_tables_with_pdfplumber(pdf_path)
        matching_tables = [select_required_tables1(tables), select_required_tables2(tables), 
                           select_required_tables3(tables), select_required_tables4(tables)]

        # ✅ Extract first table
        df1 = matching_tables[0][0]  
        df1_cleaned = df1[[1, 3]].dropna().reset_index(drop=True).T
        df1_cleaned.columns = df1_cleaned.iloc[0]  
        df1_cleaned = df1_cleaned[1:].reset_index(drop=True)  

        # ✅ Extract second table
        df2 = matching_tables[1][0]  
        df2_cleaned = df2.set_index(1).T.drop(0).reset_index(drop=True)  
        df2_cleaned.replace(r'\n', ' ', regex=True, inplace=True)  

        # ✅ Extract third table

        df3 = matching_tables[2][0].set_index(1).T.drop(0).reset_index(drop=True)  

        if 'Statutory Regulatory Authorities' in df3.columns:
            df3=df3.drop(columns=["Statutory Regulatory Authorities"])
        if "If the institution is not affiliated to a university and is\noffering programmes recognized by any Statutory\nRegulatory Authorities (SRA), are the programmes\nrecognized by Association of Indian Universities(AIU)\nor other appropriate Government authorities as\nequivalent to UG / PG Programmes of a University" in df3.columns:
            df3=df3.drop(columns=["If the institution is not affiliated to a university and is\noffering programmes recognized by any Statutory\nRegulatory Authorities (SRA), are the programmes\nrecognized by Association of Indian Universities(AIU)\nor other appropriate Government authorities as\nequivalent to UG / PG Programmes of a University"])


        # ✅ Extract state & gender data
        df4 = extractState(pdf_path).reset_index(drop=True)  
        df5 = extractGender(pdf_path).reset_index(drop=True)  

        # ✅ Extract Date of Establishment & MHRD Upload Date


        if(matching_tables[3]!=[]):
            df=matching_tables[3][0]
            # ✅ Extract required data into a dictionary
            data = {
                "Date of establishment of IQAC": [df.iloc[0, 2]],  
                "Date of uploading data on MHRD website for All India Survey on Higher Education (AISHE)":
                    [df.iloc[3, 2].replace("\nView Document", " ")]  # Use str.replace() correctly
            }
        else:
            Exception_tables=select_exception(tables)
            if(Exception_tables!=[]):
                data={
                    "Date of establishment of IQAC": [Exception_tables[0].iloc[1,0]],  
                    "Date of uploading data on MHRD website for All India Survey on Higher Education (AISHE)":
                    [Exception_tables[1].iloc[1,0]]
            }
            else:
                Exception_tables=select_exception2(tables)
                if(Exception_tables!=[]):
                    data={
                        "Date of establishment of IQAC": [Exception_tables[0].iloc[2,2]],  
                        "Date of uploading data on MHRD website for All India Survey on Higher Education (AISHE)":
                        [Exception_tables[0].iloc[5,2].replace('\nView Document', " ")]
                    }
                else:
                    Exception_tables=select_exception3(tables)
                    if(Exception_tables!=[]):
                        data={
                        "Date of establishment of IQAC": [Exception_tables[0].iloc[4,2]],  
                        "Date of uploading data on MHRD website for All India Survey on Higher Education (AISHE)":
                        [Exception_tables[0].iloc[7,2].replace('\nView Document', " ")]
                        }
                    else:
                        Exception_tables=select_exception4(tables)
                        
                        if(Exception_tables!=[]):
                            data={
                            "Date of establishment of IQAC": [Exception_tables[0].iloc[1,2]],  
                            "Date of uploading data on MHRD website for All India Survey on Higher Education (AISHE)":
                            [Exception_tables[0].iloc[4,2].replace('\nView Document', " ")]
                            }
                        else:
                            Exception_tables=select_exception5(tables)
                            data={
                                "Date of establishment of IQAC": [Exception_tables[0].iloc[3,2]],  
                                "Date of uploading data on MHRD website for All India Survey on Higher Education (AISHE)":
                                [Exception_tables[0].iloc[6,2].replace('\nView Document', " ")]
                            }

        

        df8 = pd.DataFrame(data)
        # ✅ Concatenate all extracted data
        df_combined = pd.concat([df1_cleaned, df2_cleaned, df3, df4, df5, df8], axis=1)
        all_data.append(df_combined)
        # # ✅ Append to CSV (write headers only for the first file)
        # df_combined.to_csv(output_csv, mode='a', header=first_pdf, index=False)
        # first_pdf = False  # After first PDF, all other files are appended without headers

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
