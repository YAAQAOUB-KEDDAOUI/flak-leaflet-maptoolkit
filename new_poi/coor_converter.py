import pandas as pd

files = ['أسماء ثانوية.csv', 'أسماء رئيسة.csv', 'تجمع مياه.csv', 'جبال.csv', 'حدود.csv', 'طرق صحراوية.csv',
         'موارد مياه.csv', 'مواقع اثرية.csv', 'نفود.csv']
file_nam = 'أسماء ثانوية.csv'
file_path = '../makah_map/'
for file_name in files:
    df = pd.read_csv(file_path + file_name)
    print(f"{file_name} length:  {len(df)}")

# df[['lon', 'lat']] = df['coor'].str.extract(r'POINT \((\d+\.\d+) (\d+\.\d+)')
#
# df['coor_type'] = "POINT"
# df['lon'] = df['lon'].astype(float)
# df['lat'] = df['lat'].astype(float)
# df.drop(columns=['coor', 'desc'], inplace=True)
# df.to_csv('mak_m/أسماء ثانوية.csv', index=False)
# print(df)
