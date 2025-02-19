import pdfplumber
import pandas as pd
import json
import os
from test import extractProgram

# 📂 Directory containing PDFs
pdf_directory = "data2/Group_3"  # Change this to your actual path
output_csv = "extracted_data3.csv"  # Output CSV file

# ✅ List to store extracted data from all PDFs
data_list = []
pdf_counter = 0  # Counter for processed PDFs

# ✅ Loop through all PDFs in the directory
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):  # Process only PDF files
        pdf_path = os.path.join(pdf_directory, pdf_file)
        pdf_counter += 1  # Increment counter

        # Data storage for each PDF
        data = {
            "AISHE ID": None,
            "Institution Track ID": None,
            "Name of the College": None,
            "Programme Details": []
        }

        name_extracted = False  # Ensure name is extracted only once

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    lines = text.split("\n")
                    capturing = False  # Flag to track when to start capturing
                    college_name = []

                    for i, line in enumerate(lines):
                        cleaned_line = line.strip()  # Remove extra spaces

                        if "AISHE ID" in cleaned_line:
                            data["AISHE ID"] = cleaned_line.split(":")[-1].strip()
                        if "Institution Track ID" in cleaned_line:
                            data["Institution Track ID"] = cleaned_line.split(":")[-1].strip()

                        # ✅ Start capturing when "Name of the College" is found
                        if "Name of the College" in cleaned_line and not name_extracted:
                            capturing = True
                            name_extracted = True  # Ensure name is captured only once
                            parts = cleaned_line.split("Name of the College")
                            if len(parts) > 1 and parts[1].strip():
                                college_name.append(parts[1].strip())  # Append text after keyword
                            continue  # Move to next line

                        # ✅ Stop capturing when "View Document" or "Old Name of the Institution" is found
                        if "View Document" in cleaned_line and capturing or "Old Name of the Institution" in cleaned_line and capturing:
                            capturing = False
                            break  # Stop capturing immediately

                        # ✅ Capture all lines between start and end boundaries
                        if capturing:
                            college_name.append(cleaned_line)

                    # ✅ Store full college name only once
                    if name_extracted and college_name:
                        full_name = " ".join(college_name).strip()
                        data["Name of the College"] = full_name

                # Extract program details correctly across pages
                data["Programme Details"] = extractProgram(pdf_path)

        # ✅ Convert Programme Details to JSON **without backslashes**
        data["Programme Details"] = json.dumps(data["Programme Details"], ensure_ascii=False)

        # ✅ Append extracted data to the list
        data_list.append(data)

        # ✅ Print progress
        print(f"✅ Processed {pdf_counter}: {pdf_file}")

# ✅ Convert list to DataFrame
df = pd.DataFrame(data_list)

# ✅ Save to CSV file
df.to_csv(output_csv, index=False, quoting=0)  # quoting=0 prevents extra quotes

print(f"\n✅ All {pdf_counter} PDFs successfully saved to {output_csv}")
