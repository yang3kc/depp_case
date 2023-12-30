import pandas as pd
import sys
import depppack

input_path = sys.argv[1]
output_path = sys.argv[-1]

tweet_df = pd.read_parquet(input_path)
tweet_df["create_at"] = pd.to_datetime(
    tweet_df["created_at"], format=depppack.DATE_FORMAT_STR
)

tweet_df.sort_values(by=["user_id", "created_at"], inplace=True)

user_most_recent_df = tweet_df.drop_duplicates(subset=["user_id"], keep="last")

user_most_recent_df.to_parquet(output_path, index=None)
