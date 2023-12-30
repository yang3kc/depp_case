import sys
import requests
import pandas as pd
import os

index = sys.argv[1]

input_path = f"urls/url_chunk_{index}.csv.gz"
df = pd.read_csv(input_path)

log_path = f"logs/log_chunk_{index}.csv"
output_root = f"images/image_chunk_{index}"


if not os.path.isdir("images"):
    os.mkdir("images")

if not os.path.isdir(output_root):
    os.mkdir(output_root)

if os.path.isfile(log_path):
    log_df = pd.read_csv(log_path, names=["user_id", "code"])
    done_user_ids = set(log_df["user_id"])
else:
    done_user_ids = set()

with open(log_path, "a") as log_f:
    for index, row in df.iterrows():
        if index % 100 == 0:
            print(f"Working on {index}/{len(df)} ({index/len(df)*100:.2f}%)")
        user_id = row["user_id"]
        if user_id in done_user_ids:
            print(f"{user_id} already downloaded, skipping")
        else:
            url = row["url"]
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    with open(os.path.join(output_root, f"{user_id}.jpg"), "wb") as f:
                        f.write(r.content)
                    log_f.write(f"{user_id},200\n")
                else:
                    log_f.write(f"{user_id},{r.status_code}\n")
            except Exception as e:
                print(e)
                log_f.write(f"{user_id},0\n")
