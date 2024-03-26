import time

import pandas as pd
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

global rote_data
rote_data = {"cor": [], "instruction": [], }

rud_poi_path = 'quant_data/RUD_R&C_POIs_Detailed_Sample_pro.csv'
almalqa_poi_path = 'quant_data/Sheet 1-almalqa-poi.csv'

rud_poi = pd.read_csv(rud_poi_path)
rud_poi = rud_poi.dropna()

almalqa_poi = pd.read_csv(almalqa_poi_path)
almalqa_poi = almalqa_poi.dropna()


def update_rote_data(r_data):
    global rote_data
    rote_data["cor"] = r_data['paths'][0]['points']['coordinates']
    rote_data["instruction"] = r_data['paths'][0]['instructions']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/osm')
def osm():
    return render_template('osm.html')


@app.route('/get_buildings', methods=['POST'])
def get_buildings():
    data = request.json
    north = data['north']
    east = data['east']
    south = data['south']
    west = data['west']
    searchQuery = data['searchQuery']
    sourceType = data['sourceType']

    if searchQuery == 'all':
        query = f'''
              [out:json];
              (
                node[amenity]({south},{west},{north},{east});
                way[amenity]({south},{west},{north},{east});
                relation[amenity]({south},{west},{north},{east});
              );
              out body;
              >;
              out skel qt;
            '''
    else:
        query = f'''
              [out:json];
              (
                node[amenity = {searchQuery}]({south},{west},{north},{east});
                way[amenity = {searchQuery}]({south},{west},{north},{east});
                relation[amenity= {searchQuery}]({south},{west},{north},{east});
              );
              out body;
              >;
              out skel qt;
            '''

    # check before requesting the coordinates based on the postal code
    print(f"west {west} , east {east}, north {north}, south {south}")
    api_response = data = {"version": 0.6, "generator": "Overpass API 0.7.61.5 4133829e",
                           "osm3s": {"timestamp_osm_base": "2024-02-14T22:53:41Z",
                                     "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."},
                           "elements": []}

    if sourceType == 'all':
        # response = requests.post('https://overpass-api.de/api/interpreter', data=query)
        # api_response = response.json()
        filtered_data = search_poi(rud_poi, south, north, west, east)
        if len(filtered_data) > 0:
            rud_poi_data = filtered_data.to_dict(orient='records')
            rud_poi_list = convert_to_json(rud_poi_data, 'rud')
            api_response['elements'].extend(rud_poi_list)
        filtered_data = search_poi(almalqa_poi, south, north, west, east, lon='CentroidX', lat='CentroidY')
        print(filtered_data)
        if len(filtered_data) > 0:
            rud_poi_data = filtered_data.to_dict(orient='records')
            rud_poi_list = convert_to_json(rud_poi_data, 'almalqa')
            api_response['elements'].extend(rud_poi_list)
    elif sourceType == 'rud':
        filtered_data = search_poi(rud_poi, south, north, west, east)
        if len(filtered_data) > 0:
            rud_poi_data = filtered_data.to_dict(orient='records')
            rud_poi_list = convert_to_json(rud_poi_data, 'rud')
            api_response['elements'].extend(rud_poi_list)
    elif sourceType == 'almalqa':
        filtered_data = search_poi(almalqa_poi, south, north, west, east, lon='CentroidX', lat='CentroidY')
        print(filtered_data)
        if len(filtered_data) > 0:
            rud_poi_data = filtered_data.to_dict(orient='records')
            rud_poi_list = convert_to_json(rud_poi_data, 'almalqa')
            api_response['elements'].extend(rud_poi_list)
    else:
        response = requests.post('https://overpass-api.de/api/interpreter', data=query)
        api_response = response.json()
    return jsonify(api_response)


def search_poi(poi, south, north, west, east, lat='lat', lon='lon'):
    filtered_data = poi[
        (poi[lat].astype(float) >= south) & (poi[lat].astype(float) <= north) & (poi[lon].astype(float) >= west) & (
                poi[lon].astype(float) <= east)]
    if lat != "error" or lon != "error":
        return filtered_data



def convert_to_json(filtered_data, poi_type):
    decoded_data = []
    if isinstance(filtered_data, list):
        filtered_data = pd.DataFrame(filtered_data)
    additional_columns = []
    if poi_type == 'rud':
        additional_columns = ['branch_rating', 'branch_status', 'branch_opening_hours', 'branch_amenities',
            'branch_accessibility_facilities', 'branch_payment_methods', 'branch_city', 'branch_postal_code',
            'branch_national_short_address', 'branch_id', 'branch_reviews']
    else:
        additional_columns = ['city', 'neighborhood_aname', 'neighborhood_ename', 'point_aname', 'point_ename',
            'postal_code', 'building_no', 'additional_no', 'short_address', 'street_aname', 'street_ename']

    for _, record in filtered_data.iterrows():
        tags = {}

        # Construct tags dictionary
        if poi_type == 'rud':
            tags.update(
                {"amenity": record['brand_type'], "name": record['brand_name_ar'], "name:ar": record['brand_name_ar'],
                    "name:en": record['brand_name_en'], "phone": record['branch_phone_number'],
                    "website": record['brand_website'], })
        else:
            tags.update({"amenity": record['type'], "name": record['subtype_name'], })

        # Add additional columns to the tags dictionary
        for col in additional_columns:
            tags[col] = record[col]

        if poi_type == 'rud':
            json_data = {"type": "node", "id": record['branch_id'], "lat": record['lat'], "lon": record['lon'],
                         "tags": tags}
        else:
            json_data = {"type": "node", "id": record['building_no'], "lon": record['CentroidX'],
                         "lat": record['CentroidY'], "tags": tags}
        decoded_data.append(json_data)

    print(len(decoded_data))
    return decoded_data


# def postalToCoor():
#     base_url = "https://nominatim.openstreetmap.org/search"
#     query_params = {"format": "json"}
#     postal = rud_poi['branch_postal_code']
#     results = []
#     print(rud_poi.isna().sum())
#     queries = [{"q": f"{postal_code},Saudi Arabia"} for postal_code in postal]
#     for query in queries:
#         response = requests.get(base_url, params={**query_params, **query})
#         print(response)
#         if response.status_code == 200:
#             results.extend(response.json())
#         else:
#             print('error')
#     print(results)
#     for result in distribute_duplicates(results):
#         # print(result['lat'])
#         rud_poi['lat'] = result['lat']
#         rud_poi['lon'] = result['lon']
#         rud_poi.to_csv(rud_poi_path, index=False)




def distribute_duplicates(data):
    # Iterate over each item in the data
    for idx, item in enumerate(data):
        # Check if the item is a duplicate
        if data.count(item) > 1:
            # Extract the bounding box coordinates
            bbox = item['boundingbox']
            min_lat, max_lat, min_lon, max_lon = map(float, bbox)
            # Calculate the new latitude and longitude for the duplicate item
            step_lat = (max_lat - min_lat) / (data.count(item) + 1)
            step_lon = (max_lon - min_lon) / (data.count(item) + 1)
            new_lat = min_lat + (idx % (data.count(item) + 1)) * step_lat
            new_lon = min_lon + (idx % (data.count(item) + 1)) * step_lon

            # Update the item with the new coordinates
            item['lat'] = str(new_lat)
            item['lon'] = str(new_lon)

    return data


@app.route('/osmall')
def osmall():
    return render_template('osm_all.html')


@app.route('/map_data', methods=['POST'])
def map_data():
    # Define the API query
    data = request.json
    north = data['north']
    east = data['east']
    south = data['south']
    west = data['west']
    api_url = 'https://overpass-api.de/api/interpreter'
    query = f'''
              [out:json];

              (
                node[amenity]({south},{west},{north},{east});
                way[amenity]({south},{west},{north},{east});
                relation[amenity]({south},{west},{north},{east});
              );
              out body;
              >;
              out skel qt;
            '''

    # Make the request to the API
    response = requests.post(api_url, data={'data': query})
    data = response.json()
    print(query)

    # Process the API response to extract relevant information
    # Assuming the API response contains a list of nodes with 'amenity' attribute
    map_data = []
    for element in data['elements']:
        if 'tags' in element:
            amenity = element['tags'].get('amenity')
            if amenity:
                map_data.append({'lat': element.get('lat'), 'lon': element.get('lon'), 'amenity': amenity})

    return jsonify(map_data)


@app.route('/form')
def form():
    return render_template('map_form.html')


@app.route('/simulate_route', methods=['GET'])
def simulate_route():
    print(rote_data["instruction"])
    return render_template('dynamic_route.html', route_data=rote_data)


@app.route('/get_route', methods=['POST'])
def get_route():
    coord1 = request.form.get('coord1')
    coord2 = request.form.get('coord2')
    trans_type = request.form.get('trans-type')
    maptoolkit_key = "b16b1d60-3c8c-4cd6-bae6-07493f23e589"
    payload = {"points": [[float(coord1.split(',')[1]), float(coord1.split(',')[0])],
                          [float(coord2.split(',')[1]), float(coord2.split(',')[0])]], "vehicle": trans_type,
               "locale": "en", "instructions": True, "calc_points": True, "points_encoded": False, }
    url = "https://graphhopper.com/api/1/route"
    query = {"key": maptoolkit_key}
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, params=query)
    data = response.json()
    print(data['paths'][0]['instructions'][0])
    update_rote_data(data)
    return render_template('route.html', route_data=data)


if __name__ == '__main__':
    app.run(debug=True)
