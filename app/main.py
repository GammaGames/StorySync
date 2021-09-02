import yaml
import praw
import os
import re
from datetime import datetime, timedelta
from models import Story
from pony.orm import db_session

from config import load_config, filter_comments, filter_posts


@db_session
def main():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID", ""),
        client_secret=os.getenv("REDDIT_SECRET", ""),
        username=os.getenv("REDDIT_USERNAME", ""),
        password=os.getenv("REDDIT_PASSWORD", ""),
        user_agent="Personal story sync",
    )
    config = load_config()

    def post_story(model):
        # Post story
        subreddit = reddit.subreddit(settings["to"])
        story = subreddit.submit(
            model.title,
            f"{model.body}\n\n[Story From r/{model.subreddit}]({model.source_permalink})"
        )
        # Set permalink for updating
        model.target_permalink = story.permalink

    def edit_story(model):
        story = reddit.submission(url=f"https://reddit.com{model.target_permalink}")
        story.edit(f"{model.body}\n\n[Story From r/{model.subreddit}]({model.source_permalink})")


    for username, settings in config.items():
        print(f"Collecting stories for {username}...")
        posts = filter_posts(reddit.redditor(username).submissions.new(limit=settings["count"]["posts"]), settings)
        comments = filter_comments(reddit.redditor(username).comments.new(limit=settings["count"]["comments"]), settings)

        for post in posts:
            print(post.title)

        for comment in comments:
            model = Story[comment.id, "comment"] if Story.exists(id=comment.id, type="comment") else Story(id=comment.id, type="comment")
            # If we're extracting title, try to extract it. Also optionally get subtitle
            if "extract-title" in settings["from"][comment.subreddit.display_name]["comments"]:
                model.title = parse_comment_title(
                    comment.body,
                    "extract-subtitle" in settings["from"][comment.subreddit.display_name]["comments"]
                )
            else:
                model.title = comment.submission.title

            if model.target_permalink is None:
                model.source_permalink = comment.permalink
                model.subreddit = comment.subreddit.display_name
                model.source_permalink = comment.permalink
                model.body = comment.body

                print(f"Creating {model.id}: {model.title}")
                # post_story(model)

            elif comment.edited and comment.body != model.body:
                model.body = comment.body

                print(f"Updating {model.id}: {model.title}")
                # edit_story(model)

            else:
                print(f"Skipping {model.id}: {model.title}")


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
