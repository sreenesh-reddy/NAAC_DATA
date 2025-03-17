import pandas as pd
import os

# Load the CSV file
input_csv = "part1_data2_files/part_5.csv"  # Change this to your CSV file name
df = pd.read_csv(input_csv)

# Get total rows and split size
num_rows = len(df)
split_size = num_rows // 10  # Approximate rows per split

# Create output folder
output_folder = "part1_part5_data_files"
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

# main=[]
# temp=['11.64147, 92.73832', '11.63566, 92.71702', '11.66570, 92.75129', '11.66370, 92.73775', '11.67295, 92.72687', '11.67058, 92.73677', '11.64531, 92.75278', '12.87569, 92.92441', '11.63466, 92.71458', '15.74032, 78.00845', '15.74695, 78.06745', '14.47960, 78.76452', '14.38454, 80.04453', '18.29563, 83.90502', '16.83966, 82.22907', '15.46087, 78.48069', '15.48649, 78.48326', '14.65875, 77.56783', '13.55444, 78.50699', '13.21984, 79.11083', '14.76777, 78.51246', '15.79518, 78.07701', '13.65876, 79.49000', '17.90691, 83.20619', '16.24626, 80.64713', '18.31031, 82.89676', '18.12532, 83.43114', '17.29151, 82.09874', '14.44924, 78.23433', '17.56196, 82.97867', '16.56887, 81.52507', '14.46064, 78.85576', '17.99417, 83.41574', '17.68373, 83.01652', '15.30137, 78.51235', '12.78977, 78.36470', '18.11120, 83.41078', '17.73723, 83.32841', '18.10407, 83.40177', '16.74441, 81.06289', '18.10142, 83.41809', '14.44590, 78.80654', '15.16194, 79.28625', '14.90910, 78.00914', '14.44000, 78.79863', '14.08202, 78.16734', '14.89709, 77.96744', '14.77247, 78.51385', '18.10666, 83.39549', '16.47620, 79.88785', '18.10724, 83.40094']
# main=temp[0:25]
# main.append('18.28984,83.90312')
# main2=temp[25:]
# main3=main+main2
# print(len(main3))

# import pandas as pd
# df = pd.read_csv("part1_part1_data_files/part_1.csv") 
# df["lat,long"] = main3
# df.to_csv("part1_part1_data_files/part_1.csv", index=False)

# print(df)
