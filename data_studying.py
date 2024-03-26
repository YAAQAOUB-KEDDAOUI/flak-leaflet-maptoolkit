import pandas as pd

rud_poi_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample_pro.csv'
rud_poi = pd.read_csv(rud_poi_path)

# Create a DataFrame with only the dropped rows
dropped_data = rud_poi[rud_poi['branch_opening_hours'].isnull()]

# Save the dropped data to a CSV file
dropped_data.to_csv('quant_data/dropped_data.csv', index=False)

# Calculate and print the counts and ratios of null values
null_counts = rud_poi.isnull().sum()
total_counts = rud_poi.shape[0]
null_ratios = (null_counts / total_counts) * 100

print("Ratio of Null Values (%):")
print(pd.DataFrame({"Total null": null_counts, "Ratio": null_ratios.values}))

# Remove the dropped rows from the original DataFrame
rud_poi_cleaned = rud_poi.drop(dropped_data.index)

# Save the cleaned DataFrame to a new CSV file
rud_poi_cleaned.to_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_cleaned.csv', index=False)
