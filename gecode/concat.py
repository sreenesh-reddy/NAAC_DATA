import pandas as pd

# Read two CSV files
x=4
path="part1_part"+str(x)
df1 = pd.read_csv(f"{path}_data_files/part_1.csv") 

df2 = pd.read_csv(f"{path}_data_files/part_2.csv") 
df3 = pd.read_csv(f"{path}_data_files/part_3.csv") 
df4 = pd.read_csv(f"{path}_data_files/part_4.csv") 
df5 = pd.read_csv(f"{path}_data_files/part_5.csv") 

df6 = pd.read_csv(f"{path}_data_files/part_6.csv") 
df7 = pd.read_csv(f"{path}_data_files/part_7.csv") 
df8 = pd.read_csv(f"{path}_data_files/part_8.csv") 
df9 = pd.read_csv(f"{path}_data_files/part_9.csv") 
df10 = pd.read_csv(f"{path}_data_files/part_10.csv") 


# Concatenate the DataFrames along rows (default axis=0)
df_combined = pd.concat([df1, df2,df3,df4,df5,df6,df7,df8,df9,df10])

# Save the result to a new CSV file
df_combined.to_csv(f"{path}_merged_file.csv", index=False)

print("CSV files merged successfully!")


#===================================================================
# df2=pd.read_csv('final_yellow.csv')

# df1=pd.read_csv('part1_part1_merged_file.csv')

# column_name='Name'
# matching_values = df1[column_name][df1[column_name].isin(df2['Name of the College'])].tolist()
# print(matching_values)