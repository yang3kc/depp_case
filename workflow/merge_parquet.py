import sys
import pandas as pd

input_paths = sys.argv[1:-1]
output_path = sys.argv[-1]

dfs = []
for input_path in input_paths:
    temp_df = pd.read_parquet(input_path)
    dfs.append(temp_df)

merged_df = pd.concat(dfs)

merged_df.to_parquet(output_path, index=None)
