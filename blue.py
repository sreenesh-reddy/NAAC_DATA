import pdfplumber
import pandas as pd
import json
import os
from tt import extract  # Assuming extract() handles table extraction

# 📂 Directory containing PDFs
pdf_directory = "test"  # Change this to your actual path
output_csv = "extracted_data.csv"  # Output CSV file

# ✅ List to store extracted data from all PDFs
data_list = []

# ✅ Loop through all PDFs in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

if not pdf_files:
    print("❌ No PDFs found in the directory.")
else:
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"\n📂 Processing PDF: {pdf_file}\n")

        # ✅ Data storage
        data = {
            "AISHE ID": None,
            "Number of programmes offered": []
        }

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    lines = text.split("\n")

                    for line in lines:
                        cleaned_line = line.strip()  # Remove extra spaces

                        if "AISHE ID" in cleaned_line:
                            data["AISHE ID"] = cleaned_line.split(":")[-1].strip()

        # ✅ Extract program details correctly
        data["Number of programmes offered"] = extract(pdf_path)

        # ✅ Append extracted data to the list
        data_list.append(data)

    # ✅ Convert list to DataFrame
    df = pd.DataFrame(data_list)

    # ✅ Save to CSV file
    df.to_csv(output_csv, index=False, quoting=0)  # quoting=0 prevents extra quotes

    print("\n🔹 Extracted Data:")
    print(df)

    print(f"\n✅ Data successfully saved to {output_csv}")
