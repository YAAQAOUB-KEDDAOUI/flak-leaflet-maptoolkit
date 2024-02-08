# flak-leaflet-maptoolkit

<img width="1309" alt="Screenshot 2024-01-30 at 9 53 03 PM" src="https://github.com/elshafee/flak-leaflet-maptoolkit/assets/60294043/ef9d2394-8046-464c-899a-279bd8dcd728">
```markdown
# Overpass API Queries

This repository contains sample queries for retrieving data from OpenStreetMap using the Overpass API.

## Building Query

### Description
Retrieves buildings within a specified geographical area.

### Request
- Method: GET
- Base URL: [https://overpass-api.de/api/interpreter](https://overpass-api.de/api/interpreter)

#### Body
```json
{
    "data": "[out:json][timeout:30];(way['building'](south,west,north,east);relation['building']['type'='polygon'](south,west,north,east););out;>;out qt;"
}
```

### Response Structure
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:50:34Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "way",
            "id": 240692613,
            "nodes": [...],
            "tags": {...}
        },
        ...
    ]
}
```

### Data Structure
- version (string): The version of the response data format.
- generator (string): The software or tool that generated the response.
- osm3s (object): Metadata related to the OpenStreetMap API.
    - timestamp_osm_base (string): The base timestamp of the OpenStreetMap data.
    - copyright (string): Information about the copyright.
- elements (array): An array containing information about the retrieved buildings.
    - type (string): The type of the OpenStreetMap element (e.g., way).
    - id (number): The unique identifier of the element.
    - nodes (array): An array of node IDs defining the geometry of the building.
    - tags (object): Key-value pairs representing additional information about the building (e.g., amenity, building).

### Sample Output
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:50:34Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "way",
            "id": 240692613,
            "nodes": [2484036813, 2484036802, ...],
            "tags": {
                "amenity": "place_of_worship",
                "building": "yes",
                "religion": "muslim"
            }
        },
        ...
    ]
}
```

## Restaurant Query

### Description
Retrieves restaurants within a specified geographical area.

### Request
- Method: GET
- Base URL: [https://overpass-api.de/api/interpreter](https://overpass-api.de/api/interpreter)

#### Body
```json
{
    "data": "[out:json][timeout:30];(node['amenity'='restaurant'](south,west,north,east););out;>;out qt;"
}
```

### Response Structure
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:51:30Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "node",
            "id": 3116650263,
            "lat": ...,
            "lon": ...,
            "tags": {
                "amenity": "restaurant",
                "name": "البارون",
                "name:ar": "البارون",
                "name:en": "Al-Baroun"
            }
        },
        ...
    ]
}
```

### Data Structure
- version (string): The version of the response data format.
- generator (string): The software or tool that generated the response.
- osm3s (object): Metadata related to the OpenStreetMap API.
    - timestamp_osm_base (string): The base timestamp of the OpenStreetMap data.
    - copyright (string): Information about the copyright.
- elements (array): An array containing information about the retrieved restaurants.
    - type (string): The type of the OpenStreetMap element (e.g., node).
    - id (number): The unique identifier of the element.
    - lat (number): Latitude coordinate of the restaurant.
    - lon (number): Longitude coordinate of the restaurant.
    - tags (object): Key-value pairs representing additional information about the restaurant (e.g., amenity, name).

### Sample Output
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:51:30Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "node",
            "id": 3116650263,
            "lat": 31.0456463,
            "lon": 31.3574865,
            "tags": {
                "amenity": "restaurant",
                "name": "البارون",
                "name:ar": "البارون",
                "name:en": "Al-Baroun"
            }
        },
        ...
    ]
}
```

## All Amenities Query

### Description
Retrieves all amenities within a specified geographical area.

### Request
- Method: GET
- Base URL: [https://overpass-api.de/api/interpreter](https://overpass-api.de/api/interpreter)

#### Body
```json
{
    "data": "[out:json];(node[amenity](south,west,north,east);way[amenity](south,west,north,east);relation[amenity](south,west,north,east););out body;>;out skel qt;"
}
```

### Response Structure
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:52:34Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type

": "node",
            "id": 1110567135,
            "lat": ...,
            "lon": ...,
            "tags": {
                "amenity": "place_of_worship",
                "religion": "muslim"
            }
        },
        ...
    ]
}
```

### Data Structure
- version (string): The version of the response data format.
- generator (string): The software or tool that generated the response.
- osm3s (object): Metadata related to the OpenStreetMap API.
    - timestamp_osm_base (string): The base timestamp of the OpenStreetMap data.
    - copyright (string): Information about the copyright.
- elements (array): An array containing information about the retrieved amenities.
    - type (string): The type of the OpenStreetMap element (e.g., node).
    - id (number): The unique identifier of the element.
    - lat (number): Latitude coordinate of the amenity.
    - lon (number): Longitude coordinate of the amenity.
    - tags (object): Key-value pairs representing additional information about the amenity (e.g., amenity, name).

### Sample Output
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:52:34Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "node",
            "id": 1110567135,
            "lat": 31.0638820,
            "lon": 31.4031921,
            "tags": {
                "amenity": "place_of_worship",
                "religion": "muslim"
            }
        },
        ...
    ]
}
```

## All Nodes Query

### Description
Retrieves all nodes within a specified geographical area.

### Request
- Method: GET
- Base URL: [https://overpass-api.de/api/interpreter](https://overpass-api.de/api/interpreter)

#### Body
```json
{
    "data": "[out:json];(node(south,west,north,east);<;);out meta;"
}
```

### Response Structure
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:53:30Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "node",
            "id": 31321356,
            "lat": ...,
            "lon": ...,
            "timestamp": "2020-01-13T15:59:16Z",
            "version": 8,
            "changeset": 79523538,
            "user": "nour_saeed",
            "uid": 9945425
        },
        ...
    ]
}
```

### Data Structure
- version (string): The version of the response data format.
- generator (string): The software or tool that generated the response.
- osm3s (object): Metadata related to the OpenStreetMap API.
    - timestamp_osm_base (string): The base timestamp of the OpenStreetMap data.
    - copyright (string): Information about the copyright.
- elements (array): An array containing information about the retrieved nodes.
    - type (string): The type of the OpenStreetMap element (e.g., node).
    - id (number): The unique identifier of the element.
    - lat (number): Latitude coordinate of the node.
    - lon (number): Longitude coordinate of the node.
    - timestamp (string): Timestamp of the last modification.
    - version (number): Version of the node.
    - changeset (number): Changeset ID associated with the node modification.
    - user (string): User who last modified the node.
    - uid (number): User ID of the user who last modified the node.

### Sample Output
```json
{
    "version": "0.6",
    "generator": "Overpass API 0.7.61.5 4133829e",
    "osm3s": {
        "timestamp_osm_base": "2024-02-08T20:53:30Z",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
    },
    "elements": [
        {
            "type": "node",
            "id": 31321356,
            "lat": 31.0933357,
            "lon": 31.3046235,
            "timestamp": "2020-01-13T15:59:16Z",
            "version": 8,
            "changeset": 79523538,
            "user": "nour_saeed",
            "uid": 9945425
        },
        ...
    ]
}
```
```

