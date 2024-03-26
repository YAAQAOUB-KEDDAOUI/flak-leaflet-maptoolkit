# import pandas as pd
#
# # Read the CSV files into DataFrames
# rud_poi_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample.csv'
# extended_rud_path = "quant_data/RUD_R&C_POIs_Detailed_Sample_processed.csv"
# rud_poi = pd.read_csv(rud_poi_path)
# df1 = pd.read_csv(extended_rud_path)
# print(df1.isna().sum())
#
# rud_poi = rud_poi.dropna()
# print(rud_poi.shape)
#
# # Merge the DataFrames based on a common key column
# merged_df = df1.merge(rud_poi, on='branch_national_short_address', how='outer')
# merged_df = merged_df.drop_duplicates()
# merged_df.to_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_full.csv', index=False)
#
# df3 = pd.read_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_full.csv')
# print(df3.isna().sum())

# import pandas as pd
#
# # Load the CSV file
# data = pd.read_csv('quant_data/RUD_R&C_POIs_Detailed_Sample.csv')
#
# # Iterate over the rows and drop rows where branch_national_short_address is null
# for index, row in data.iterrows():
#     if pd.isnull(row['branch_national_short_address']):
#         data.drop(index, inplace=True)
#
# # Save the updated DataFrame
# data.to_csv('updated_file.csv', index=False)
import pandas as pd
file1 = pd.read_csv('updated_file.csv')
file2 = pd.read_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_processed.csv')
print(len(file1))
# merged_file = pd.concat([file1, file2], axis=1)
# merged_file.to_csv('RUD_R&C_POIs_Detailed_Sample_pro.csv', index=False)

# import pandas as pd
#
# data = pd.read_csv('RUD_R&C_POIs_Detailed_Sample_pro.csv')
#
# # Drop the column you want to remove
# column_to_drop = 'postal_code'
# data.drop(columns=[column_to_drop], inplace=True)
#
# # Save the updated DataFrame to a new CSV file
# data.to_csv('updated_file.csv', index=False)