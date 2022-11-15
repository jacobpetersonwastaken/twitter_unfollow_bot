from os import getenv
import tweepy
from dotenv import load_dotenv
from requests import post, delete, put, get, request, Response
from requests_oauthlib import OAuth1
from json import dump, load
from time import sleep, time
from PlayVideo import PlayVideo
import pyuser_agent
client = tweepy.Client
pagination_token = "token"


def get_follower_list():
    """Getting all the followers from twitters api"""
    load_dotenv('.env')
    my_id = getenv('TWITTER_ID')
    twitter_bearer_token = getenv('BEARER_TOKEN')
    headers = {"Authorization": f"Bearer {twitter_bearer_token}"}

    parameters = {
        'max_results': 1000,
        'pagination_token': "token"
    }
    endpoint = f"https://api.twitter.com/2/users/{my_id}/following"
    r = get(url=endpoint, params=parameters, headers=headers)
    response = r.json()
    print(r.headers)

    with open("following1.json", "w+") as data:
        dump(response, data)




def raw_folowers_to_data():
    """Getting the user ids to unfollow from the json data"""
    raw_data = ["following.json", "following1.json"]

    following_ids = []
    for i in raw_data:
        with open(i, "r") as following:
            data = load(following)
            for id in data["data"]:
                following_ids.append(id["id"])
    with open("following_ids.json", "w+") as file:
        dump(following_ids, file)

def unfollow(user_id_to_unfollow):
    """Unfollow bot"""
    load_dotenv('.env')
    your_twitter_id = getenv("TWITTER_ID")
    consumer_key = getenv("API_KEY")
    consumer_secret = getenv("API_KEY_SECRET")
    access_token = getenv("ACCESS_TOKEN")
    access_token_secret = getenv("ACCESS_TOKEN_SECRET")
    ua = pyuser_agent.UA()
    headers = {
        "User-Agent": ua.random
    }
    endpoint = f"https://api.twitter.com/2/users/{your_twitter_id}/following/{user_id_to_unfollow}"
    auth = OAuth1(client_key=consumer_key, client_secret=consumer_secret, resource_owner_key=access_token,
                  resource_owner_secret=access_token_secret, decoding=None)
    r = delete(url=endpoint, auth=auth, headers=headers)
    reset_rate_limit = int(r.headers["x-rate-limit-remaining"])
    print("requests left this session", reset_rate_limit)
    if reset_rate_limit == 0:
        print("Sleeping for 15 minutes")
        sleep(960)
        return True
    if 200 <= r.status_code < 300:
        return True
    else:
        print("Status code:", r.status_code)
        print(r.headers)
        return False

def unfollow_timer(time_between_requests):
    """Workes with twitters api limits and waits for those to make sure we dont get banned"""
    video = PlayVideo()
    with open("following_ids.json", "r") as data:
        ids = load(data)
    for i, id in enumerate(ids):
        index = i + 1
        if unfollow(id):
            print(f"Unfollowing user {id}")
        else:
            video.play_video(r"brokenTabel.mp4", 6)
            print(f"Error on Id: {id}")
            input("\nwaiting for human")
        sleep(time_between_requests)



unfollow_timer(10)
