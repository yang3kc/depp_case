import sys
import ujson as json
from depppack import Tweet
import pandas as pd

input_path = sys.argv[1]
output_path = sys.argv[-1]

tweet_info_list = []
with open(input_path) as f:
    for line in f:
        tweet = json.loads(line)
        tweet_obj = Tweet(tweet)
        tweet_id = tweet_obj.get_post_ID()
        user_id = tweet_obj.get_user_ID()

        tweet_type = "original"
        retweet_id = None
        retweet_user_id = None
        if tweet_obj.is_retweet:
            tweet_type = "retweet"
            retweet_id = tweet_obj.retweet_object.get_post_ID()
            retweet_user_id = tweet_obj.retweet_object.get_user_ID()

        if tweet_obj.is_quote:
            tweet_type = "quote"
            retweet_id = tweet_obj.quote_object.get_post_ID()
            retweet_user_id = tweet_obj.quote_object.get_user_ID()

        tweet_info_list.append(
            [
                tweet_id,
                tweet_obj.get_link_to_post(),
                tweet_obj.get_value(["created_at"]),
                tweet_obj.get_value(["source"]),
                tweet_obj.get_value(["retweet_count"]),
                tweet_obj.get_value(["favorite_count"]),
                tweet_obj.get_text(),
                tweet_type,
                retweet_id,
                retweet_user_id,
                user_id,
                tweet_obj.get_value(["user", "created_at"]),
                tweet_obj.get_value(["user", "followers_count"]),
                tweet_obj.get_value(["user", "friends_count"]),
                tweet_obj.get_value(["user", "statuses_count"]),
                tweet_obj.get_value(["user", "screen_name"]),
                tweet_obj.get_value(["user", "name"]),
                tweet_obj.get_value(["user", "verified"]),
                tweet_obj.get_value(["user", "profile_image_url"]),
                tweet_obj.get_value(["user", "description"]),
            ]
        )

tweet_info_df = pd.DataFrame(
    tweet_info_list,
    columns=[
        "tweet_id",
        "link",
        "created_at",
        "source",
        "retweet_count",
        "like_count",
        "text",
        "tweet_type",
        "retweet_id",
        "retweet_user_id",
        "user_id",
        "user_created_at",
        "user_followers_count",
        "user_friends_count",
        "user_tweet_count",
        "screen_name",
        "name",
        "verified",
        "profile_image_url",
        "description",
    ],
)
tweet_info_df.to_parquet(output_path, index=None)
