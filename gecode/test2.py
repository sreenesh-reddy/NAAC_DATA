import pandas as pd
import os

# Load the CSV file
input_csv = "part_1.csv"  # Change this to your CSV file name
df = pd.read_csv(input_csv)

# Get total rows and split size
num_rows = len(df)
split_size = num_rows // 10  # Approximate rows per split

# Create output folder
output_folder = "data2_files"
os.makedirs(output_folder, exist_ok=True)

# Split and save each part
for i in range(10):
    start_idx = i * split_size
    end_idx = start_idx + split_size if i < 9 else num_rows  # Last split takes the remaining rows

    part_df = df.iloc[start_idx:end_idx]
    output_file = os.path.join(output_folder, f"part_{i+1}.csv")
    part_df.to_csv(output_file, index=False)
    print(f"✅ Saved {output_file}")

print("🎉 CSV file successfully split into 10 parts!")
# import pandas as pd

# excel_file = "data.xlsx"  # Change this to your Excel file
# df = pd.read_excel(excel_file)  # Reads the first sheet by default

# # Convert to CSV
# csv_file = "data.csv"  # Output file name
# df.to_csv(csv_file, index=False)