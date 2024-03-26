import pandas as pd

# Sample data (replace with your actual file paths)
rud_poi_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample.csv'
extended_rud_path = "quant_data/RUD_R&C_POIs_Detailed_Sample_processed.csv"
common_column = 'branch_national_short_address'

# Read CSV files into DataFrames
df1 = pd.read_csv(rud_poi_path)
df2 = pd.read_csv(extended_rud_path)

# Merge DataFrames on the common column
merged_df = pd.merge(df1, df2, on=common_column, how='inner')
# Filter df1 to keep rows not present in the merged DataFrame (non-duplicates)
filtered_df1 = df1[~df1[common_column].isin(merged_df[common_column])]

# Print or save the filtered items (optional)
print("Items not present in file 2:")
print(filtered_df1)

# Save the filtered items to a new file (optional)
filtered_df1.to_csv('non_duplicates.csv', index=False)
