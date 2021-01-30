from twitter_api import TweetBot, get_config
import threading

if __name__=="__main__":
    allowed = get_config('config.json',"allowed")

    print("starting...")
    for config in allowed:
        print("USER:",config)
        t_bot = TweetBot(config)
        t = threading.Thread(target=t_bot.search_follow_trains)
        t.start()
        print("THREAD RUNNING...")
        print("==========================================================")