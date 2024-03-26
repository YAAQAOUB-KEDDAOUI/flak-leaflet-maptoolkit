import pandas as pd


dfs = []  # List to store DataFrames


df = pd.read_csv('saudi_map/saudi_map.csv')
dfs.append(df)

# Concatenate all DataFrames in the list
result_df = pd.concat(dfs, ignore_index=True)

result_df.to_json('saudi_map/saudi_map.json', orient='records', lines=True, force_ascii=False)
