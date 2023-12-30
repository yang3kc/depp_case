import logging
import sys
from datetime import datetime


############################################################
############################################################
# Utilities
############################################################
def get_dict_val(dictionary: dict, key_list: list = []):
    """
    Return `dictionary` value at the end of the key path provided
    in `key_list`.
    Indicate what value to return based on the key_list provided.
    For example, from left to right, each string in the key_list
    indicates another nested level further down in the dictionary.
    If no value is present, a `None` is returned.
    Parameters:
    ----------
    - dictionary (dict) : the dictionary object to traverse
    - key_list (list) : list of strings indicating what dict_obj
        item to retrieve
    Returns:
    ----------
    - key value (if present) or None (if not present)
    Raises:
    ----------
    - TypeError
    Examples:
    ---------
    # Create dictionary
    dictionary = {
        "a" : 1,
        "b" : {
            "c" : 2,
            "d" : 5
        },
        "e" : {
            "f" : 4,
            "g" : 3
        },
        "h" : 3
    }
    ### 1. Finding an existing value
    # Create key_list
    key_list = ['b', 'c']
    # Execute function
    get_dict_val(dictionary, key_list)
    # Returns
    2
    ~~~
    ### 2. When input key_path doesn't exist
    # Create key_list
    key_list = ['b', 'k']
    # Execute function
    value = get_dict_val(dictionary, key_list)
    # Returns NoneType because the provided path doesn't exist
    type(value)
    NoneType
    """
    if not isinstance(dictionary, dict):
        raise TypeError("`dictionary` must be of type `dict`")

    if not isinstance(key_list, list):
        raise TypeError("`key_list` must be of type `list`")

    retval = dictionary
    for k in key_list:
        # If retval is not a dictionary, we're going too deep
        if not isinstance(retval, dict):
            return None

        if k in retval:
            retval = retval[k]

        else:
            return None
    return retval


def get_logger():
    """Create print only logger."""

    # Create logger and set level
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)

    # Configure format
    formatter = logging.Formatter(
        fmt="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
        datefmt="%Y-%m-%d_%H:%M:%S",
    )

    # Configure stream handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.setLevel(level=logging.INFO)
    logger.addHandler(ch)

    return logger


############################################################
############################################################
# Data model
############################################################
class PostBase:
    """
    Base class for social media post.
    Classes for specific platforms can inheret it.
    It defines the common functions that the children classes
    should have.
    """

    def __init__(self, post_object):
        """
        This function initializes the instance by binding the post_object

        Parameters:
            - post_object (dict): the JSON object of the social media post
        """
        if post_object is None:
            raise ValueError("The post object cannot be None")
        self.post_object = post_object

    def is_valid(self):
        """
        Check if the data is valid
        """
        raise NotImplementedError

    def get_value(self, key_list: list = []):
        """
        This is the same as the midterm.get_dict_val() function
        Return `dictionary` value at the end of the key path provided
        in `key_list`.
        Indicate what value to return based on the key_list provided.
        For example, from left to right, each string in the key_list
        indicates another nested level further down in the dictionary.
        If no value is present, a `None` is returned.
        Parameters:
        ----------
        - dictionary (dict) : the dictionary object to traverse
        - key_list (list) : list of strings indicating what dict_obj
            item to retrieve
        Returns:
        ----------
        - key value (if present) or None (if not present)
        """
        return get_dict_val(self.post_object, key_list)

    def extract_hashtag_from_string(self, text):
        """
        Get all hashtags from the post by matching the # symbol in the text
        Code modified to handle chains of #-separated hashtags
        https://stackoverflow.com/questions/2527892/parsing-a-tweet-to-extract-hashtags-into-an-array

        Returns:
            - A list of strings representing the hashtags, # symbols are not included
        """
        hashtags = []
        for part in text.split():
            if part.startswith("#"):
                hashtag_text = part[1:]
                if "#" in hashtag_text:
                    # hashtags might not be space-separated, in which case split by "#"
                    hashtags.extend(
                        [tag for tag in hashtag_text.split("#") if tag != ""]
                    )
                else:
                    hashtags.extend([hashtag_text])
        return hashtags

    def get_timestamp(self):
        """
        Return the post time-of-creation
        """
        raise NotImplementedError

    def get_post_ID(self):
        """
        Return the ID of the post as a string
        """
        raise NotImplementedError

    def get_link_to_post(self):
        """
        Return the link to the post so that one can click it and check
        the post in a web browser
        """
        raise NotImplementedError

    def get_user_ID(self):
        """
        Return the ID of the user as a string
        """
        raise NotImplementedError

    def get_URLs(self):
        """
        Return all URLs (list of dicts) embedded in the social media post
        Each element is a URL dict. Dict keys: {"raw_url", "expanded_url", "domain"}
        """
        raise NotImplementedError

    def get_hashtags(self):
        """
        Return the list of hashtags embedded in the social media post
        """
        raise NotImplementedError

    def get_text(self):
        """
        Return the text of the social media post
        """
        raise NotImplementedError

    def get_media(self):
        """
        Return the media (photo, video, etc.) embedded in the social media post
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Define the representation of the object.
        """
        return f"<{self.__class__.__name__}() object>"


class Tweet(PostBase):
    """
    Class to handle tweet object (V1 API)
    """

    def __init__(self, tweet_object):
        """
        This function initializes the instance by binding the tweet_object

        Parameters:
            - tweet_object (dict): the JSON object of a tweet
        """
        super().__init__(tweet_object)

        self.is_quote = "quoted_status" in self.post_object
        if self.is_quote:
            self.quote_object = Tweet(self.post_object["quoted_status"])

        self.is_retweet = "retweeted_status" in self.post_object
        if self.is_retweet:
            self.retweet_object = Tweet(self.post_object["retweeted_status"])

        self.is_extended = "extended_tweet" in self.post_object
        if self.is_extended:
            self.extended_object = Tweet(self.post_object["extended_tweet"])

    def is_valid(self):
        """
        Check if the tweet object is valid.
        A valid tweet should at least have the following attributes:
            [id_str, user, text, created_at]
        """
        attributes_to_check = ["id_str", "user", "text", "created_at"]
        for attribute in attributes_to_check:
            if attribute not in self.post_object:
                return False
        return True

    def get_timestamp(self):
        """
        Return tweet timestamp (int)
        """
        created_at = self.get_value(["created_at"])
        timestamp = datetime.strptime(
            created_at, "%a %b %d %H:%M:%S +0000 %Y"
        ).timestamp()
        return int(timestamp)

    def get_post_ID(self):
        """
        Return the ID of the tweet (str)
        This is different from the id of the retweeted tweet or
        quoted tweet
        """
        return self.get_value(["id_str"])

    def get_link_to_post(self):
        """
        Return the link to the tweet (str)
        so that one can click it and check the tweet in a web browser
        """
        return f"https://twitter.com/{self.get_user_sreenname()}/status/{self.get_post_ID()}"

    def get_user_ID(self):
        """
        Return the ID of the user (str)
        """
        return self.get_value(["user", "id_str"])

    def get_retweeted_post_ID(self):
        """
        Return the original post ID (str)
        This is retweeted tweet ID for retweet, quoted tweet ID for quote
        """
        if self.is_retweet:
            return self.retweet_object.get_post_ID()
        if self.is_quote:
            return self.quote_object.get_post_ID()
        return None

    def get_retweeted_user_ID(self):
        """
        Return the original user ID (str)
        This is retweeted user ID for retweet, quoted user ID for quote
        """
        if self.is_retweet:
            return self.retweet_object.get_user_ID()
        if self.is_quote:
            return self.quote_object.get_user_ID()
        return None

    def get_user_sreenname(self):
        """
        Return the screen_name of the user (str)
        """
        return self.get_value(["user", "screen_name"])

    def get_text(self):
        """
        Extract the tweet text (str)
        It will return the full_text in extended_tweet in its presence

        Parameters:
            - clean (bool, default False):
                If True, return cleaned text (strip stopwords, emojis, URLs, etc. see clean_text() for more details)
                if False, return the raw text
        """

        if self.is_extended:
            text = self.extended_object.get_value(["full_text"])
        else:
            text = self.get_value(["text"])
        return text

    def get_URLs(self, recursive=False):
        """
        Get all URLs from tweet, excluding links to the tweet itself.
        All URLs are guaranteed to be in the "entities" field (no need to extract from text)
        Prioritize extraction from "extended_tweet". This attribute always contains the superset of the Tweet payload.

        Parameters:
            - recursive (bool, default False): If True, the function will also
                extract URLs from any embedded quoted_status or retweeted_status
                object; if False, the function will ignore these objects

        Returns:
            - urls (list of str) : A list of URL strings
        """

        urls = []
        if self.is_extended:
            url_objects = self.extended_object.get_value(["entities", "urls"])
        else:
            url_objects = self.get_value(["entities", "urls"])

        if url_objects is not None:
            for item in url_objects:
                expanded_url = get_dict_val(item, ["expanded_url"])
                if (expanded_url is not None) and ("twitter.com" not in expanded_url):
                    url = expanded_url
                else:
                    url = get_dict_val(item, ["url"])
                urls.append(url)

        if recursive:
            # Also collect the URLs from the retweet and quote
            if self.is_retweet:
                urls.extend(self.retweet_object.get_URLs())
            if self.is_quote:
                urls.extend(self.quote_object.get_URLs())

        return urls

    def get_hashtags(self, recursive=False):
        """
        Get all hashtags from the tweet, '#' symbols are excluded.
        They can be found in the "entities" field.

        Parameters:
            - recursive (bool, default True): If True, the function will also
                extract URLs from any embedded quoted_status or retweeted_status
                object; if False, the function will ignore these objects

        Returns:
            - A list of strings representing the hashtags,
        """

        if self.is_extended:  # Prioritize values from "extended_tweet" if exists.
            raw_hashtags = self.extended_object.get_value(["entities", "hashtags"])
        else:
            raw_hashtags = self.get_value(["entities", "hashtags"])
        if raw_hashtags is not None:
            hashtags = [ht["text"] for ht in raw_hashtags]

        if recursive:
            # Also collect the hashtags from the retweet and quote
            if self.is_retweet:
                hashtags.extend(self.retweet_object.get_hashtags())
            if self.is_quote:
                hashtags.extend(self.quote_object.get_hashtags())

        return hashtags

    def get_media(self, recursive=False):
        """
        Get all media from the tweet.
        They can be found in the "extended_entities" field.

        Parameters:
            - recursive (bool, default True): If True, the function will also
                extract media from any embedded quoted_status or retweeted_status
                object; if False, the function will ignore these objects

        Returns:
            - media (list of dicts) : A list of media objects that take the following form:
                {
                    'media_url' : <url_str>,
                    'media_type' : <type_str> # E.g., 'photo', 'video', 'gif'
                }
        """

        # Sometimes the media in the original tweet is included in the retweet or quoting tweet.
        # Keep a set of known_media to avoid adding duplicates.
        media = []
        # Entities can be found in multiple places
        # See an example: https://twitter.com/i/web/status/1577811416794513408
        if self.is_extended:  # Prioritize values from "extended_tweet" if exists.
            media_list = self.extended_object.get_value(["extended_entities", "media"])
        else:
            media_list = self.get_value(["extended_entities", "media"])
        if media_list is not None:
            for item in media_list:
                media.append(
                    {"media_url": item["media_url"], "media_type": item["type"]}
                )

        if recursive:
            # Also collect the media from the retweet and quote
            if self.is_retweet:
                for temp_media in self.retweet_object.get_media():
                    media.append(temp_media)

            if self.is_quote:
                for temp_media in self.quote_object.get_media():
                    media.append(temp_media)

        return media

    def __repr__(self):
        """
        Define the representation of the object.
        """
        return "".join(
            [
                f"<{self.__class__.__name__}() object> from @{self.get_user_sreenname()}\n",
                f"Link: {self.get_link_to_post()}",
            ]
        )
