import camelot
import fitz  # PyMuPDF
import pandas as pd
import json

def extract_tables_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_tables = []

    for page_num in range(len(doc)):
        # Extract tables from each page using Camelot
        tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1), flavor='stream')
        
        for table in tables:
            df = table.df
            df.replace("", pd.NA, inplace=True)
            df.dropna(axis=1, how='all', inplace=True)  # Remove empty columns
            df.fillna("", inplace=True)  # Fill remaining NaNs with empty strings
            all_tables.append((page_num + 1, df))  # Store page number and table data

    return all_tables

# ✅ Function to clean multiline program names
def clean_multiline_data(table):
    new_rows = []
    temp_row = ["", ""]  # Temporary row buffer (2 columns)
    start = False

    for i in range(table.shape[0]):
        if table.shape[1] < 2:
            continue  # Skip if there aren't enough columns

        # ✅ Detect when a new row starts
        if table.iloc[i, 1] != "":
            if start:
                new_rows.append(temp_row.copy())  # Save previous concatenated row
            temp_row = ["", ""]  # Reset buffer
            start = True  # Start capturing new entry

        # ✅ Concatenate both columns properly
        for col in range(2):
            if table.iloc[i, col]:
                temp_row[col] += " " + str(table.iloc[i, col]).strip()

    # ✅ Append the last accumulated row
    if start:
        new_rows.append(temp_row)

    # ✅ Convert list of rows into DataFrame
    df_cleaned = pd.DataFrame(new_rows, columns=["Program Name", "Number"])
    return df_cleaned

# ✅ Function to find, clean, and convert the table to JSON
def find_and_jsonify_table(tables, keyword):
    for page_num, table in tables:
        table.fillna("", inplace=True)

        # ✅ Check if the first row contains the keyword
        if table.iloc[0, 0].strip().lower() == keyword.lower():
            cleaned_table = table.iloc[2:].reset_index(drop=True)  # Remove first two rows
            cleaned_table = clean_multiline_data(cleaned_table)  # Clean multiline data
            
            # ✅ Convert the table to a dictionary (first column as key, second as value)
            table_dict = dict(zip(cleaned_table.iloc[:, 0], cleaned_table.iloc[:, 1]))
            return page_num, table_dict  # Return JSON data

    return None, None  # Return None if not found

def extract(pdf_path):
    #pdf_path = "data2/Group_1/table2.pdf"

    # ✅ Extract tables from the PDF
    tables = extract_tables_from_pdf(pdf_path)

    # ✅ Find and convert the specific table to JSON
    page, json_table = find_and_jsonify_table(tables, "Number of programmes offered")

    # ✅ Print the JSON output if found
    if json_table is not None:
        print(f"\n📄 Table Found on Page {page} (Fixed & Converted to JSON):\n")
        return(json.dumps(json_table))
    else:
        return {}


