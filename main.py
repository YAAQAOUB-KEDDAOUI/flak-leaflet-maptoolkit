import requests
from flask import Flask, render_template, request

app = Flask(__name__)

global rote_data
rote_data = {"cor": [], "instruction": [], }


def update_rote_data(r_data):
    global rote_data
    rote_data["cor"] = r_data['paths'][0]['points']['coordinates']
    rote_data["instruction"] = r_data['paths'][0]['instructions']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('map_form.html')


@app.route('/simulate_route', methods=['GET'])
def simulate_route():
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
