# import csv
# import json
#
# # Path to the input CSV file
# csv_file_path = 'merged_data.csv'
#
# # Path to the output JSON file
# json_file_path = 'merged_data.json'
import math

# # List to store the JSON objects
# data = []
#
# # Read the CSV file
# with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         # Convert each row to a dictionary and append it to the data list
#         data.append(row)
#
# # Write the data list to a JSON file without escaping non-ASCII characters
# with open(json_file_path, mode='w', encoding='utf-8') as file:
#     json.dump(data, file, indent=4, ensure_ascii=False)
import pandas as pd
import json

df = pd.read_csv('merged_data.csv')
result = []
for _, row in df.iterrows():
    tags = {k: v for k, v in row.items() if pd.notnull(v) and k not in ['type', 'brand_id', 'lat', 'lon']}
    tags = {k: v for k, v in tags.items() if v}  # Remove empty values
    tags['city'] = row['city']
    tags['branch_postal_code'] = row['branch_postal_code']
    tags['building_number'] = row['building_number']
    tags['brand_name_en'] = row['brand_name_en']
    tags['brand_name_ar'] = row['brand_name_ar']
    tags['brand_logo_link'] = row['brand_logo_link']
    tags['brand_website'] = row['brand_website']
    tags['brand_size'] = row['brand_size']
    tags['brand_price_range'] = row['brand_price_range']
    tags['brand_instagram_link'] = row['brand_instagram_link']
    tags['brand_type'] = row['brand_type']
    tags['brand_categories'] = row['brand_categories']
    tags['branch_rating'] = row['branch_rating']
    tags['branch_status'] = row['branch_status']
    tags['branch_opening_hours'] = row['branch_opening_hours']
    tags['branch_amenities'] = row['branch_amenities']
    tags['branch_accessibility_facilities'] = row['branch_accessibility_facilities']
    tags['branch_national_short_address'] = row['branch_national_short_address']
    tags['branch_payment_methods'] = row['branch_payment_methods']
    tags['branch_phone_number'] = row['branch_phone_number']
    tags['street_aname'] = row['street_aname']
    tags['district'] = row['district']
    tags['branch_reviews'] = row['branch_reviews']
    # Remove keys with NaN values from tags
    tags = {k: v for k, v in tags.items() if pd.notnull(v)}
    result.append({
        'type': 'amenity',
        # 'id': row['branch_id'],
        'geometry': {
            "type": "POINT",
            "coordinates": [
                [row['lon'], row['lat']]
            ]
        },
        'tags': tags
    })
# Read the existing JSON file
with open('new_poi/saudi_map/saudi_map.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

# Append each existing data to the result
for datum in existing_data:
    result.append(datum)

# Write the merged data to a new JSON file
with open('fully.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4)