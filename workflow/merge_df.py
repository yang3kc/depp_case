import sys
import pandas as pd

input_paths = sys.argv[1:-1]
output_path = sys.argv[-1]

dfs = []
for input_path in input_paths:
    temp_df = pd.read_csv(input_path)
    dfs.append(temp_df)

merged_df = pd.concat(dfs)

merged_df.to_csv(output_path, index=None)
