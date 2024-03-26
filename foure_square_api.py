import requests
import csv

headers = {
    "accept": "application/json",
    "Authorization": "fsq3iBxt+KVJWF5THZsljoKtkL6oICOMWzqFxqij0aBAb5M="
}
header = {
    "accept": "application/json",
}

# to fetch fsq_id from Foursquare API
def get_fsq_id(lat, lon, chain):
    url = f"https://api.foursquare.com/v3/places/search?ll={lat},{lon}&query=Coffee Shop&radius=100&chains={chain}&open_now=true"
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    fsq_id = data["results"][0]["fsq_id"] if data.get("results") else "0"
    print(fsq_id)
    return fsq_id

# to fetch working_hours from Foursquare API
day_mapping = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}
def gethours(fsq_id):
    url = f"https://api.foursquare.com/v2/venues/{fsq_id}/hours?v=20240312&hourFormat=12&oauth_token=3IWPEWBGV2Z452M1C30RXFTDSEJV3VUAOMN4QAEJKDWPVXMQ"
    response = requests.get(url, headers=header)
    data = response.json()
    print(data)
    opening_hours = []
    print(len(data['response']['hours']))
    if len(data['response']['hours']) > 0:
        for timeframe in data['response']['hours']['timeframes']:
            days = ', '.join([str(day) for day in timeframe['days']])
            start_time = f"{timeframe['open'][0]['start'][:2]}:{timeframe['open'][0]['start'][2:]} AM"
            end_time = f"{timeframe['open'][0]['end'][:2]}:{timeframe['open'][0]['end'][2:]} PM"
            opening_hours.append({"days": days, "open": start_time, "close": end_time})
    else:
        for timeframe in data['response']['popular']['timeframes']:
            days = ', '.join([str(day) for day in timeframe['days']])
            start_time = f"{timeframe['open'][0]['start'][:2]}:{timeframe['open'][0]['start'][2:]} AM"
            end_time = f"{timeframe['open'][0]['end'][:2]}:{timeframe['open'][0]['end'][2:]} PM"
            opening_hours.append({"days": days, "open": start_time, "close": end_time})
    formatted_opening_hours = [
        f'"{", ".join([day_mapping[int(day)] for day in oh["days"].split(",")])}: {oh["open"]} - {oh["close"]}"' for oh
        in opening_hours]
    return formatted_opening_hours

# Load CSV file
with open('quant_data/dropped_data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    rows = list(csv_reader)

# Add fsq_id to each row
for row in rows:
    lat = row['lat']
    lon = row['lon']
    chain = row['brand_name_ar']
    fsq_id = get_fsq_id(lat, lon, chain)
    row['fsq_id'] = fsq_id
    if fsq_id != "0":
        print(f"my {fsq_id}here")
        row['branch_opening_hours'] = gethours(fsq_id)

# Save the updated data to a new CSV file
with open('quant_data/dropped_data_with_fsq_id.csv', mode='w', newline='') as file:
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Successfully added fsq_id to the CSV file.")


