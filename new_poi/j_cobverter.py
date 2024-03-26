import json

# Read the JSON file
with open('saudi_map/saudi_map.json', 'r', encoding='utf-8') as f:
    data = f.readlines()

# Process each record and convert it to the desired format
result = []
for line in data:
    record = json.loads(line)
    if record['coor_type'] == 'POINT':
        geometry = {
            "type": "POINT",
            "coordinates": eval(record['lon_lat'])
        }
    elif record['coor_type'] == 'LINESTRING':
        geometry = {
            "type": "LINESTRING",
            "coordinates": eval(record['lon_lat'])
        }
    else:
        # Handle other types if needed
        geometry = {}


    result.append({
        "type": "node",
        "geometry": geometry,
        "tags": {
            "city": record.get("city", ""),
            "category": record.get("category", ""),        }
    })

# Save the result as a new JSON file
with open('converted_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
