import csv
import pandas as pd

# Define the fieldnames for the CSV file
fieldnames = [
    "city",
    "branch_postal_code",
    "building_number",
    "lat",
    "lon",
    "subtype_name",
    "branch_id",
    "brand_name_en",
    "brand_name_ar",
    "brand_logo_link",
    "brand_website",
    "brand_size",
    "brand_price_range",
    "brand_instagram_link",
    "brand_type",
    "brand_categories",
    "branch_rating",
    "branch_status",
    "branch_opening_hours",
    "branch_amenities",
    "branch_accessibility_facilities",
    "branch_national_short_address",
    "branch_payment_methods",
    "branch_phone_number",
    "street_aname",
    "street_ename",
    "district",
    "branch_reviews"
]

# Read the datasets
dataset1 = pd.read_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_pro.csv')

dataset2 = pd.read_csv('quant_data/Sheet 1-almalqa-poi.csv')

dataset2.rename(columns={'CentroidX': 'lon', 'CentroidY': 'lat'}, inplace=True)
dataset2.rename(columns={'neighborhood_aname': 'district'}, inplace=True)
dataset2.rename(columns={'short_address': 'branch_national_short_address'}, inplace=True)
dataset2.rename(columns={'postal_code': 'branch_postal_code'}, inplace=True)
dataset2.rename(columns={'point_aname': 'brand_name_ar', 'point_ename': 'brand_name_en'}, inplace=True)
dataset1.rename(columns={'street': 'street_aname'}, inplace=True)
dataset1.rename(columns={'type': 'brand_type'}, inplace=True)


# Merge the datasets into a single list
merged_data = []

for _, data1_row in dataset1.iterrows():
    merged_row = {field: data1_row.get(field, "") for field in fieldnames}
    merged_data.append(merged_row)

for _, data2_row in dataset2.iterrows():
    merged_row = {field: data2_row.get(field, "") for field in fieldnames}
    merged_data.append(merged_row)

# Write the merged data to a CSV file
with open("merged_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)

print("Merged data written to merged_data.csv")
