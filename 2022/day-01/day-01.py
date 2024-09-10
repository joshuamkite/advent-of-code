import numpy as np
import pandas as pd

# open local input file 'with' autoclose and read lines
with open('input') as f:
    contents = f.readlines()

# Remove newline characters and convert to pandas DataFrame
contents = [line.strip()for line in contents]
df = pd.DataFrame(contents, columns=['Numbers'])

# Replace empty strings with NaN
df.replace("", np.nan, inplace=True)

# change the column to numeric
df['Numbers'] = pd.to_numeric(df['Numbers'])

# Split df into smaller DataFrames at the NaN rows
df_list = np.split(df, df[df.isnull().all(1)].index)

# Create a list to store the sums and their indices
sums_and_indices = []

# iterate over df_list and store each sum with its index
for i, df in enumerate(df_list):
    if df['Numbers'].notna().any():  # Check if DataFrame contains any non-NaN values
        sums_and_indices.append((df['Numbers'].sum(), i+1))

# Sort sums and indices in descending order by sum
sums_and_indices.sort(reverse=True)

# Get the indices of the top 3 Dataframes
top_3 = sums_and_indices[:3]

for sum_value, index in top_3:
    print(f"elf {index} is carrying {int(sum_value)} calories")

# Calculate and print the total of the top 3 sums
total_top_3 = sum(sum_value for sum_value, index in top_3)
print(
    f"The total calories carried by the top 3 elves are {int(total_top_3)} calories.")
