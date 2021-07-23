import yaml
import praw
import os
import re
from datetime import datetime, timedelta

from config import load_config, filter_comments, filter_posts


def main():
    client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        client_secret=os.getenv("REDDIT_SECRET", ""),
        username=os.getenv("REDDIT_USERNAME", ""),
        password=os.getenv("REDDIT_PASSWORD", ""),
        user_agent="Personal story sync",
    )
    config = load_config()

    for username, settings in config.items():
        posts = filter_posts( client.redditor(username).submissions.new(limit=settings["count"]["posts"]), settings)
        comments = filter_comments(client.redditor(username).comments.new(limit=settings["count"]["comments"]), settings)

        for post in posts:
            print("Post:", post.subreddit.display_name, ":", post.name)

        for comment in comments:
            print("Comment", comment.subreddit.display_name, ":", parse_comment_title(comment.body, True))
            # print(
            #     parse_comment_title(comment.body, True),
            #     datetime.fromtimestamp(comment.created_utc),
            #     datetime.now() - timedelta(**settings["from"][comment.subreddit.display_name]["comments"]["delay"]),
            #     datetime.fromtimestamp(comment.created_utc) < datetime.now() - timedelta(**settings["from"][comment.subreddit.display_name]["comments"]["delay"])
            # )

        # TODO check if posts and stuff are already stored
        # TODO If they are stored, check if they need to be updated
        # TODO If they aren't, make them


def parse_comment_title(comment, subtitle=False):
    pass
    lines = list(filter(None, [s.strip() for s in comment.split("\n")]))
    title_match = re.search(r"^(?:#\s*)?\<?(?P<title>[^\>]*)\>?", lines[0])
    title = title_match.group("title") if title_match is not None else ""
    if subtitle and len(lines) > 1 and lines[1].startswith("#"):
        subtitle_match = re.search(r"^(?:#+\s*)?(?P<subtitle>.*)", lines[1])
        title += f" - {subtitle_match.group('subtitle')}" if subtitle_match is not None else ""

    return title


if __name__ == "__main__":
    main()
