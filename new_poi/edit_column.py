import pandas as pd

# files = ['أسماء ثانوية.csv', 'أسماء رئيسة.csv', 'تجمع مياه.csv', 'جبال.csv','طرق صحراوية.csv','موارد مياه.csv', 'مواقع اثرية.csv' ,'نفود.csv' ]
files =['albaha_map','aljouf_map','alqassim_map', 'aseer_map', 'hail_map', 'jizan_map', 'madinah_map','makkah_map','najran_map', 'northern_border_map', 'riyadh_map', 'sharqia_map', 'tabuk_map']
file_path = 'saudi_map/'

dfs = []
for file_name in files:
    df = pd.read_csv(file_path + file_name+'/'+ file_name+'.csv')
    df['city'] = file_name[:-4]
    dfs.append(df)

result_df = pd.concat(dfs, ignore_index=True)
result_df.to_csv(file_path+'saudi_map.csv', index=False)