import pandas as pd

# Read the existing CSV file into a pandas DataFrame
# existing_df = pd.read_csv('r_m.csv')

# Read the new CSV file into a pandas DataFrame
new_df = pd.read_csv('new_file.csv')

# Concatenate the existing DataFrame with the new DataFrame
combined_df = pd.concat([existing_df, new_df], ignore_index=True)

# Save the combined DataFrame to the existing CSV file
combined_df.to_csv('r_m.csv', index=False)
