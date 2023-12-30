import os
import depppack

DATA_ROOT = "/home/yangkc/depp_case/data"
RAW_DATA_ROOT = os.path.join(DATA_ROOT, "raw_data")

INTERMEDIATE_ROOT = os.path.join(DATA_ROOT, "intermediate_data")

RAW_TWEETS = os.path.join(INTERMEDIATE_ROOT, "raw_tweets_months", "{ym}.ndjson")

YMS = depppack.YMS

YMS = ["2020-04"]

################################################################
################################################################
# Rules
TWEET_INFO = os.path.join(INTERMEDIATE_ROOT, "tweet_info", "{ym}.parquet")

rule extract_information_all:
    input: expand(TWEET_INFO, ym=YMS)

rule extract_information:
    input: RAW_TWEETS
    output: TWEET_INFO
    shell: "python extract_information.py {input} {output}"