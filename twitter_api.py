import tweepy
import json
from time import sleep
import sys, os
from random import randint
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pickle

def get_config(filename,username):
        j = json.load(open(filename))
        return j[username]

class TweetBot:
    def __init__(self, screen_name, config_filename='config.json'):

        config = get_config(config_filename, screen_name)
        oauth = self.OAuth(config)
        self.api = tweepy.API(oauth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.screen_name = screen_name

    def OAuth(self, config):
        try:
            auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
            auth.set_access_token(config['access_token'], config['access_secret'])
            return auth
        except:
            return None

    # config = get_config('config.json','shitty_princess')
    # oauth = OAuth(config)

    # api = tweepy.API(oauth)

    def print_err(self, err):
        print(str(err) + " on line " + str(sys.exc_info()[2].tb_lineno))

    def follow_user(self, username):
        try:
            self.api.create_friendship(username)
        except Exception as ex:
            self.print_err(ex)

    def like(self, id):
        try:
            self.api.create_favorite(id)
        except Exception as ex:
            self.print_err(ex)

    def retweet(self,id):
        try:
            self.api.retweet(id)
        except Exception as ex:
            self.print_err(ex)

    def search_follow_trains(self):
        for tweet in tweepy.Cursor(self.api.search,q="ifb",result_type="recent", include_entities=True, geocode="5.5557,-0.1963,200km").items(5):
            print("tweet: ", tweet.text, " by: ", tweet.user.screen_name)
            
            print("=========================================================================")
            id = tweet._json["id"]
            like_or_follow = randint(0,10)
            
            user = tweet.user

            if like_or_follow > 5:

                print("following this lucky user")
                self.follow_user(user.screen_name)
                sleep(30*like_or_follow)
            else:
                print("liking tweet")
                self.like(tweet.id)
                sleep(30*like_or_follow)
           
            
    def reply_status(self, tweet_id, message):
        try:
            self.api.update_status(message,in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        except Exception as e:
            self.print_err(e)

    def reconcile_followers(self):
        page = tweepy.Cursor(self.api.followers, result_type="recent").items(20)
        # screen_names.extend([i._json["screen_name"] for i in page])
        # print("LENGTH OF IDS ARRAY: ", len(screen_names))
        # sleep(10)
        for user in page:
            print("================================ USER FOLLOWING ME=====================================")
            print("USER: ",user.screen_name)
            if not user.following:
                print("NOT FOLLOWING BACK")
                user.follow()
                sleep(60*5)
            else:
                print("FOLLOWING BACK ALREADY...")

    def reconcile_following(self):
        print("starting reconciliation...")
        user_ids = [user.id for user in tweepy.Cursor(self.api.friends).items(100)]
        print("gotten user ids")
        for relationship in self.api._lookup_friendships(user_ids):
            print("user follows back. Skipping...")
            if not relationship.is_followed_by:
                print(f'Unfollowing @{relationship.screen_name} ({relationship.id})')
                try:
                    self.api.destroy_friendship(relationship.id)
                  
                except tweepy.error.TweepError:
                    print('Error unfollowing.')
            print(f"Done with @{relationship.screen_name}...")
            sleep(5)


    def cleanup_follows(self, screen_name):
        filename = screen_name + '_follows.pckl'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        user_obj = self.api.get_user(screen_name)
        following_size = user_obj.friends_count

        cursor_position = 0

        for friends_ids in tweepy.Cursor(self.api.friends_ids, screen_name=screen_name, count_size=200).pages():
            for id in friends_ids:
                #check if last tweet is more than three months old
                
                status = self.api.user_timeline(id, count=1)
                if not status:
                    print("User ID: ", id)
                    print("No status: ", status)
                continue

                print("=================>>>>>>")
                print("User: ", user.screen_name)
                three_months_ago = datetime.today() - relativedelta(months=+6)
                if status.created_at <= three_months_ago:
                    print("Last tweet date: is more than three months ==> ", status.created_at)
                    user.unfollow
                    print("unfollowed")
                

                #check if following back

                #check if bio has keyword
                sleep(60)
            
        
if __name__=="__main__":
  
    t_bot = TweetBot("kwesi_dadson")
    # t_bot.search_follow_trains()
    # t_bot.reply_status("1267189208600457217", "Then take this seriously! Delete this tweet!!")
    # t_bot.search_follow_trains()

    t_bot.cleanup_follows("kwesi_dadson")
