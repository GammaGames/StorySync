import yaml
import praw
import os
import re


def main():
    client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        client_secret=os.getenv("REDDIT_SECRET", ""),
        username=os.getenv("REDDIT_USERNAME", ""),
        password=os.getenv("REDDIT_PASSWORD", ""),
        user_agent="Personal story sync",
    )
    config = yaml.safe_load(open("/opt/config.yaml"))

    for username, settings in config.items():
        print("User:", username, "comments" in settings["from"]["WritingPrompts"])
        posts = [
            p for p in client.redditor(username).submissions.new(limit=8)
            if p.subreddit.display_name in settings["from"]  # Subreddit has to be in settings
            and "posts" in settings["from"][p.subreddit.display_name]  # Posts has to be in subreddit settings
        ]

        comments = [
            c for c in client.redditor(username).comments.new(limit=32)
            if c.parent_id.startswith("t3_")  # Only first-child comments
                and c.subreddit.display_name in settings["from"]  # Subreddit has to be in settings
                and "comments" in settings["from"][c.subreddit.display_name]  # Comments has to be in subreddit settings
        ]

        for post in posts:
            print("Post:", post.subreddit.display_name, ":", post.name)

        for comment in comments:
            print("Comment:", comment.subreddit.display_name, ":", comment.parent_id)

        # TODO check if posts and stuff are already stored
        # TODO If they are stored, check if they need to be updated
        # TODO If they aren't, make them

if __name__ == "__main__":
    main()
