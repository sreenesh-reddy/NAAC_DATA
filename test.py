import camelot
import fitz  # PyMuPDF
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_tables = []

    for page_num in range(len(doc)):
        tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1), flavor='stream')
        
        for table in tables:
            df = table.df
            df.replace("", pd.NA, inplace=True)
            df.dropna(axis=1, how='all', inplace=True)
            df.fillna("", inplace=True)
            all_tables.append((page_num + 1, df))

    return all_tables

def clean_multiline_data(tables):
    cleaned_tables = []
    for item in tables:
        table=item
        new_rows = []
        temp_row = ["", "", "", "",""]  # Temporary row buffer (4 columns)
        start = False
        # print('==================')
        # print(table)
        # print('==================')
        for i in range(item.shape[0]):
            if table.shape[1] < 4:
                #print("skipped",table.shape[1])  
                continue  # Skip if columns are less than expected

            # If column 3 contains 'Permanent' or 'Temporary', it marks the start of a new entry
            if table.iloc[i, 3] in ["Permanent", "Temporary"]:
                if start:
                    new_rows.append(temp_row.copy())  # Save previous concatenated row
                temp_row = ["", "", "", "",""]  # Reset buffer

                start = True  # Start capturing new entry
                temp_row[4] = table.iloc[i, 3]  # Store the last column (status)
            elif(table.shape[1] > 4 and table.iloc[i, 4] in ["Permanent", "Temporary"]):
                if start:
                    new_rows.append(temp_row.copy())  # Save previous concatenated row
                temp_row = ["", "", "", "",""]  # Reset buffer

                start = True  # Start capturing new entry
                temp_row[4] = table.iloc[i, 4]



            # Concatenate the first three columns (if non-empty)
            if(table.shape[1] > 4):
                for col in range(4):  
                    if table.iloc[i, col]:  
                        temp_row[col] += " " + str(table.iloc[i, col]).strip()
            else:
                for col in range(3):  
                    if table.iloc[i, col]:  
                        temp_row[col] += " " + str(table.iloc[i, col]).strip()

        # Append the last accumulated row
        if start:
            new_rows.append(temp_row)

        # Convert list of rows into DataFrame
        df_cleaned = pd.DataFrame(new_rows, columns=["Program", "Department", "University Affiliation","SRA Recognition", "Status"])
        cleaned_tables.append((df_cleaned))
        # print('========AFTER CLEANED==========')
        # print(df_cleaned)
        # print('==================')

    return cleaned_tables


def tables_between_boundaries(tables, start_boundary, end_boundary):
    selected_tables=[]
    start_found = False
    for page_num, table in tables:
      
        table.fillna("", inplace=True)

        if not start_found and str(table.iloc[0, 0]).strip() == start_boundary:
            start_found = True
            table = table.iloc[2:].reset_index(drop=True) 
        
        if start_found and str(table.iloc[0, 0]).strip() == end_boundary:
            break
        
        if start_found:
            selected_tables.append(table)
    return selected_tables
            

def extractProgram(pdf_path):
# pdf_path = 'data2/table2.pdf'
    tables = extract_tables_from_pdf(pdf_path)
    selectedTables=tables_between_boundaries(tables,'Programme Details', '27')

    cleaned_tables = clean_multiline_data(selectedTables)
    if(cleaned_tables):
        df=pd.concat(cleaned_tables,axis=0, ignore_index=True)
        return df.to_json(orient="records")
    else:
        return []
