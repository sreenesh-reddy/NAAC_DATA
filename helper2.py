import pdfplumber
import pandas as pd
import json

def extract_tables_with_pdfplumber(pdf_path):
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)  # Convert to DataFrame
                df.fillna("", inplace=True)  # Ensure no NaN values
                all_tables.append((page_num + 1, df))  # Store page number and table data

    return all_tables

# ✅ Function to filter tables where the first row, first column contains 'Male'
def select_male_tables(tables):
    selected_tables = []
    
    for page_num, table in tables:
        # Ensure table is not empty and has at least one row
        if table.empty or table.shape[0] == 0:
            continue

        first_cell = str(table.iloc[0, 0]).strip().lower()  # Normalize case
        if first_cell == "male":  # Check for "Male" in first cell
            selected_tables.append((page_num, table))

    return selected_tables

# ✅ Function to convert DataFrame to JSON (first row as keys)
def table_to_json(df):
    if df.shape[0] < 2:  # Ensure there is at least one data row
        return {}

    keys = df.iloc[0].tolist()  # First row as keys
    values = df.iloc[1:].values.tolist()  # Remaining rows as values
    json_data = [dict(zip(keys, row)) for row in values]  # Convert to JSON format

    return json_data

# ✅ Run Extraction
def extractGender(pdf_path):
    #pdf_path = "data2/Group_1/table2.pdf"
    tables = extract_tables_with_pdfplumber(pdf_path)

    # ✅ Filter only tables with 'Male' in the first row, first column
    matching_tables = select_male_tables(tables)

    # ✅ Select only the third matching table and convert to JSON
    if len(matching_tables) >= 3:
        page, df = matching_tables[2]
        df = df.reset_index(drop=True)
        df.columns = df.iloc[0]  # Set first row as headers
        df = df[1:].reset_index(drop=True)  # Drop the first row and reset index
        df = df.reset_index(drop=True)
        return df
        # json_output = table_to_json(df)  # Convert to JSON format
        
        # #print(f"\n📄 Third Matching Table Found on Page {page} (Converted to JSON):\n")
        # return(json.dumps(json_output)) # Pretty-print JSON
    else:
        return pd.DataFrame()
    
