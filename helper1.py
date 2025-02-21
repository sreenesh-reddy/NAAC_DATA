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

# ✅ Function to filter tables where the first row, first column contains 'State'
def select_state_tables(tables):
    selected_tables = []
    
    for page_num, table in tables:
        # Ensure table is not empty and has at least one row
        if table.empty or table.shape[0] == 0:
            continue

        first_cell = str(table.iloc[0, 0]).strip().lower()  # Normalize case
        if first_cell == "state":
            selected_tables.append((page_num, table))

    return selected_tables

# ✅ Function to convert DataFrame to JSON (first row as keys)
def table_to_json(df):
    if df.shape[0] < 2:  # Ensure there is at least one data row
        return []

    keys = df.iloc[0].tolist()  # First row as keys
    values = df.iloc[1:].values.tolist()  # Remaining rows as values
    json_data = [dict(zip(keys, row)) for row in values]  # Convert to JSON format

    return json_data

# ✅ Run Extraction

def extractState(pdf_path):
    #pdf_path = "data2/Group_1/table2.pdf"
    tables = extract_tables_with_pdfplumber(pdf_path)

    # ✅ Filter only tables with 'State' in the first row, first column
    state_tables = select_state_tables(tables)

    # ✅ Convert and print selected tables as JSON
    if state_tables:
        for page, df in state_tables:
            df = df.reset_index(drop=True)
            df = df.drop(df.columns[-1], axis=1)  # Remove old index
            df.columns = df.iloc[0]  # Set first row as headers
            df = df[1:].reset_index(drop=True)  # Drop the first row and reset index
            df = df.reset_index(drop=True)
             # Remove the old header row

             # Remove the old header row
            # json_output = table_to_json(df)  # Convert to JSON format
            # return(json.dumps(json_output))  # Pretty-print JSON
            return df
    else:
        return pd.DataFrame()

