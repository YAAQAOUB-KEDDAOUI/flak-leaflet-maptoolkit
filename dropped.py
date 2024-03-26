import pandas as pd

# Load the CSV file into a DataFrame
rud_poi_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample_pro.csv'
rud_poi = pd.read_csv(rud_poi_path)

# Drop the null values from the specified column
cleaned_data = rud_poi.dropna(subset=['lon', 'lat'])

# Separate the dropped data or data with "error" into a new DataFrame
dropped_data = rud_poi[~rud_poi.index.isin(cleaned_data.index)]

# Filter the data with "error"
error_data = dropped_data[dropped_data['lat'].str.contains('Error', case=True, na=True)]

# Save the dropped data or data with "error" into a new CSV file
dropped_data.to_csv('dropped_data.csv', index=False)
error_data.to_csv('error_data.csv', index=False)

# Print shapes and data (if needed)
print("Shape of cleaned data:", cleaned_data.shape)
print("Shape of dropped data:", dropped_data.shape)
print("Shape of error data:", error_data.shape)
