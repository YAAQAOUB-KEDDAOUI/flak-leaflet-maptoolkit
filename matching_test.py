import pandas as pd

file1 = pd.read_csv('quant_data/RUD_R&C_POIs_Detailed_Sample_pro.csv')
file2 = pd.read_csv('quant_data/Sheet 1-almalqa-poi.csv')
if file1.shape != file2.shape:
    print("Error: The two DataFrames have different shapes.")
else:
    matching_cells = (file1 == file2).sum().sum()
    total_cells = file1.size
    matching_ratio = matching_cells / total_cells

    print(f"Matching ratio: {matching_ratio:.2f}")
