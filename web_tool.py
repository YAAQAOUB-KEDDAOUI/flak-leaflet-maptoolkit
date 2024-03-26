import csv
import json
import requests
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
upload_file_path = ''
processing = True
success = False

rud = pd.read_csv('quant_data/RUD_R&C_POIs_Detailed_Sample.csv')
almalqa = pd.read_csv('quant_data/Sheet 1-almalqa-poi.csv')
rud_col = rud.columns.tolist()
almalqa_col = almalqa.columns.tolist()
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


@app.route('/home')
def home():
    return render_template('map.html')


@app.route('/data')
def get_data():
    with open('uploads/fully.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return jsonify(data)


def processing_fun():
    global processing, success
    compare()
    time.sleep(2)
    processing = False
    success = True


@app.route('/', methods=['GET', 'POST'])
def index():
    global processing
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload_form.html', message='No file part')

        file = request.files['file']
        if file.filename == '':
            return render_template('upload_form.html', message='No selected file')

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if not os.path.exists(file_path):
                return render_template('upload_form.html', message='Error: File could not be saved')

            df = pd.read_csv(file_path)
            file_col = df.columns.tolist()
            if file_col == rud_col:
                if len(df) > 100:
                    return render_template('upload_form.html', message='Error: File could not be saved please make sure '
                                                                       'the file length < 100')

            global upload_file_path
            upload_file_path = file_path
            print(upload_file_path)
            global processing
            processing = True
            processing_thread = threading.Thread(target=processing_fun)
            processing_thread.start()
            return render_template('loading.html')

    return render_template('upload_form.html')


def compare():
    global upload_file_path
    file = pd.read_csv(upload_file_path)
    file_col = file.columns.tolist()
    merged_data = []

    if file_col == rud_col:
        print("Rud data")
        drop_short_address_nan()
        rud_coordinate()
        data = pd.read_csv(upload_file_path)
        data.rename(columns={'street': 'street_aname'}, inplace=True)
        data.rename(columns={'type': 'brand_type'}, inplace=True)
        for _, data1_row in data.iterrows():
            merged_row = {field: data1_row.get(field, "") for field in fieldnames}
            merged_data.append(merged_row)


    elif file_col == almalqa_col:
        print("Almalqa data")
        file.rename(columns={'CentroidX': 'lon', 'CentroidY': 'lat'}, inplace=True)
        file.rename(columns={'short_address': 'branch_national_short_address'}, inplace=True)
        file.rename(columns={'postal_code': 'branch_postal_code'}, inplace=True)
        file.drop(['neighborhood_aname', 'neighborhood_ename'], axis=1, inplace=True)
        for _, data2_row in file.iterrows():
            merged_row = {field: data2_row.get(field, "") for field in fieldnames}
            merged_data.append(merged_row)
    else:
        print("Can't operate with that format")

    if os.path.exists(upload_file_path):
        os.remove(upload_file_path)
        print(f"File '{upload_file_path}' deleted successfully")
    df1 = pd.read_csv("uploads/dataset.csv")


    file = file[~file.isin(df1)].dropna()

    # Append the differences to df1
    with open("uploads/dataset.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_data)
    connvert_json()


def drop_short_address_nan():
    rud_poi_path = upload_file_path
    rud_poi = pd.read_csv(rud_poi_path)
    rud_poi.dropna(subset=['branch_national_short_address'], inplace=True)
    rud_poi.to_csv(upload_file_path, index=False)


@app.route('/status')
def status():
    global processing, success
    print(upload_file_path)
    return jsonify({'processing': processing, 'success': success})


# using the national API to get the coordinates
def rud_coordinate():
    base_url = "https://apina.address.gov.sa/NationalAddress/v3.1/Address/address-free-text?"
    query_params = {
        "language": "A",
        "format": "json",
        "page": "1",
        "api_key": "70c9eb19bd454478a659ddb36214dc52"
    }
    global upload_file_path
    rud_poi_path = upload_file_path
    rud_poi = pd.read_csv(rud_poi_path)
    rud_poi = rud_poi['branch_national_short_address'].dropna()
    rud_poiA = rud_poi[:100]
    processed_file_path = 'uploads/dataset.csv'
    processed_df = pd.read_csv(processed_file_path) if os.path.exists(processed_file_path) else pd.DataFrame()

    results = []
    for shortadress in rud_poiA:
        query = {"addressstring": shortadress, **query_params}
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
                        'branch_national_short_address': shortadress,
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
                        'branch_national_short_address': shortadress,
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
                    'branch_national_short_address': shortadress,
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
                'branch_national_short_address': shortadress,
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
    combined_df = pd.concat([processed_df, new_processed_df], ignore_index=True, axis=1)
    combined_df.to_csv('uploads/dataset.csv', index=False)
    print("Done")


def connvert_json():
    df = pd.read_csv('uploads/dataset.csv')
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
        tags = {k: v for k, v in tags.items() if pd.notnull(v)}
        result.append({
            'type': 'amenity',
            'geometry': {
                "type": "POINT",
                "coordinates": [
                    [row['lon'], row['lat']]
                ]
            },
            'tags': tags
        })
    with open('uploads/fully.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
