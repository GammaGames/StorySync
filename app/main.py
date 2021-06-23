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

        comments = filter_comments(client.redditor(username).comments.new(limit=64), settings)

        for post in posts:
            print("Post:", post.subreddit.display_name, ":", post.name)

        for comment in comments:
            print("Comment", comment.subreddit.display_name, ":", comment.body.split("\n")[0])
            print(parse_comment_title(comment.body, True))

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


def filter_comments(comments, config):
    return [
        c for c in comments
        if c.parent_id.startswith("t3_")  # Only first-child comments
        and c.subreddit.display_name in config["from"]  # Subreddit has to be in settings
        and "comments" in config["from"][c.subreddit.display_name]  # Comments has to be in subreddit settings
        and (  # If the comments require a title
            ("require-title" in config["from"][c.subreddit.display_name]["comments"] and c.body.startswith("#"))
            or True
        )
    ]


if __name__ == "__main__":
    main()
