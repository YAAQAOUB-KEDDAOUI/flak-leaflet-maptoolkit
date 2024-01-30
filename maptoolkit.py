import requests

url = "https://graphhopper.com/api/1/route"

query = {
  "key": "b16b1d60-3c8c-4cd6-bae6-07493f23e589"
}

payload = {
  "points": [
    [
      11.539421,
      48.118477
    ],
    [
      11.559023,
      48.12228
    ]
  ],
  "point_hints": [
    "Lindenschmitstraße",
    "Thalkirchener Str."
  ],
  "snap_preventions": [
    "motorway",
    "ferry",
    "tunnel"
  ],
  "details": [
    "road_class",
    "surface"
  ],
  "vehicle": "bike",
  "locale": "en",
  "instructions": True,
  "calc_points": True,
  "points_encoded": False
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers, params=query)
data = response.json()
print(data)