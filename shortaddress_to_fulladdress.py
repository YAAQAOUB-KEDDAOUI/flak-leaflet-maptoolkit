import os

import pandas as pd
import requests
import time

def postalToCoor():
    base_url = "https://apina.address.gov.sa/NationalAddress/v3.1/Address/address-free-text?"
    query_params = {
        "language": "A",
        "format": "json",
        "page": "1",
        "api_key": "39477d43b27c477bbb581066477909cb"
    }

    rud_poi_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample.csv'
    rud_poi = pd.read_csv(rud_poi_path)
    rud_poi = rud_poi['branch_national_short_address'].dropna()
    rud_poiA = rud_poi[:100]
    print(rud_poi.shape)
    print(rud_poi)

    processed_file_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample_processed.csv'
    processed_df = pd.read_csv(processed_file_path) if os.path.exists(processed_file_path) else pd.DataFrame()

    results = []
    for postal_code in rud_poiA:  # Iterate through the values directly
        query = {"addressstring": postal_code, **query_params}

        time.sleep(5)  # To avoid rate limiting
        response = requests.get(base_url, params=query)
        print(response.url)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data['statusdescription'] == 'SUCCESS':
                if 'Addresses' in data and len(data['Addresses']) > 0:
                    result = data['Addresses'][0]
                    result_data = {
                        'branch_national_short_address': postal_code,
                        'building_number': result.get('BuildingNumber', ''),
                        'street': result.get('Street', ''),
                        'district': result.get('District', ''),
                        'city': result.get('City', ''),
                        'postal_code': result.get('PostCode', ''),
                        'latitude': result.get('Latitude', ''),
                        'longitude': result.get('Longitude', '')
                    }
                    results.append(result_data)
                else:
                    results.append({
                        'branch_national_short_address': postal_code,
                        'building_number': '',
                        'street': '',
                        'district': '',
                        'city': '',
                        'postal_code': '',
                        'latitude': 'Error',
                        'longitude': 'Error'
                    })
            else:
                results.append({
                    'branch_national_short_address': postal_code,
                    'building_number': '',
                    'street': '',
                    'district': '',
                    'city': '',
                    'postal_code': '',
                    'latitude': 'Error',
                    'longitude': 'Error'
                })
        else:
            results.append({
                'branch_national_short_address': postal_code,
                'building_number': '',
                'street': '',
                'district': '',
                'city': '',
                'postal_code': '',
                'latitude': 'Error',
                'longitude': 'Error'
            })

    new_processed_df = pd.DataFrame(results)

    # Save the updated DataFrame to the original file
    rud_poi = rud_poi[100:]
    rud_poi.to_csv(rud_poi_path, index=False)
    # Save the processed data to a new CSV file
    combined_df = pd.concat([processed_df, new_processed_df], ignore_index=True)
    combined_df.to_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_processed.csv', index=False)

    print("Done")

postalToCoor()
