import pandas as pd
# coor,name,desc
files = ['أسماء ثانوية.csv', 'أسماء رئيسة.csv', 'تجمع مياه.csv', 'جبال.csv','طرق صحراوية.csv', 'مواقع اثرية.csv',  'موارد مياه.csv' , 'نفود.csv']
file_path = 'tabuk_map/'
# ,  'نفود.csv'
for file_name in files:
    new_coors = []
    coor_types = []
    df = pd.read_csv(file_path + file_name)
    print(f"{file_name} length:  {len(df)}")
    for index, row in df.iterrows():
        print(index)
        if row['coor'].startswith('POINT'):
            coor_values = row['coor'].replace('POINT (', '').replace(')', '').split()
            lon = float(coor_values[0])
            lat = float(coor_values[1])
            new_coors.append([[lon, lat]])
            coor_types.append('POINT')
        elif row['coor'].startswith('LINESTRING'):
            coordinates = row['coor'].replace('LINESTRING (', '').replace(')', '').split(', ')
            points = []
            for coord in coordinates:
                lon, lat, _ = coord.split()
                points.append([float(lon), float(lat)])
            new_coors.append(points)
            coor_types.append('LINESTRING')
        else:
            new_coors.append(None)
            coor_types.append(None)
    df['lon_lat'] = new_coors
    df['coor_type'] = coor_types
    df.drop(columns=['coor', 'desc'], inplace=True)
    df.to_csv('new_poi/tab_m/'+file_name, index=False)
