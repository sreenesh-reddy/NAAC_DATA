import pdfplumber
import pandas as pd

pd.set_option("display.max_colwidth", None)

def extract_tables_with_pdfplumber(pdf_path):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                df.fillna("", inplace=True)  # Remove NaN values
                all_tables.append((page_num + 1, df))  # Store page number and table
    return all_tables

def find_matching_table(tables, keyword):
    """
    Searches for a table containing a specific keyword in any column and extracts the next column's value.
    """
    selected_tables = []
    for page_num, df in tables:
        if df.empty or df.shape[0] == 0:
            continue
        # Normalize text in all columns
        df = df.applymap(lambda x: str(x).replace('\n', ' ').strip())

        for col_idx in range(df.shape[1]):  # Iterate over all columns
            col = df.iloc[:, col_idx]  # Select column
            if col.str.contains(keyword, case=False, na=False).any():
                selected_tables.append((page_num, df))
                break  # Stop once a match is found on the page

    return selected_tables

def extract_value_from_table(df, keyword):
    """
    Extracts the value from the next column after finding the keyword.
    """
    df = df.applymap(lambda x: str(x).replace('\n', ' ').strip())  # Clean text
    for col_idx in range(df.shape[1] - 1):  # Exclude last column to prevent out-of-bounds
        col = df.iloc[:, col_idx]
        if col.str.contains(keyword, case=False, na=False).any():
            value = df.loc[col.str.contains(keyword, case=False, na=False), df.columns[col_idx + 1]].values
            return str(value[0]) if len(value) > 0 else "Not Found"
    return "Not Found"

def extractDate(pdf_path):
    tables = extract_tables_with_pdfplumber(pdf_path)

    # Define the target keywords
    iqac_keyword = "Date of establishment of IQAC"
    aishe_keyword = "Date of uploading data on MHRD website"

    # Search for tables containing the target keywords
    iqac_tables = find_matching_table(tables, iqac_keyword)
    aishe_tables = find_matching_table(tables, aishe_keyword)

    # Extract values
    iqac_date = extract_value_from_table(iqac_tables[0][1], iqac_keyword) if iqac_tables else "Not Found"
    aishe_date = extract_value_from_table(aishe_tables[0][1], aishe_keyword) if aishe_tables else "Not Found"

    # Store results in a DataFrame
    ans_dict = {
        'Date of establishment of IQAC': [iqac_date],
        'Date of uploading data on MHRD website for AISHE': [aishe_date.replace('View Document','')]
    }

    return pd.DataFrame(ans_dict)

# print(extractDate('t/t.pdf'))
