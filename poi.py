from flask import Flask, render_template
import csv
import ast

app = Flask(__name__)

@app.route('/')
def index():
    points = []
    lines = []
    with open('new_poi/saudi_map/saudi_map.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            lon_lat = ast.literal_eval(row['lon_lat'])
            print(lon_lat[0])
            if row['coor_type'] == 'POINT':
                points.append(lon_lat[0])
            elif row['coor_type'] == 'LINESTRING':
                lines.append(lon_lat)

    return render_template('raq.html', points=points, lines=lines)

if __name__ == '__main__':
    app.run(debug=True)
