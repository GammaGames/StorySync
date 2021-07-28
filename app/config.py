import yaml
from datetime import datetime, timedelta


def load_config():
    data = yaml.safe_load(open("/config.yaml"))

    for username, settings in data.items():
        for subreddit, content_types in settings["from"].items():
            for content_type, settings in content_types.items():
                config = {}
                for s in settings:
                    if isinstance(s, dict):
                        config[list(s.keys())[0]] = list(s.values())[0]
                    else:
                        config[s] = True

                data[username]["from"][subreddit][content_type] = config

    return data


def filter_comments(comments, config):
    result = []
    for comment in comments:
        if filter_comment(comment, config):
            result.append(comment)

            if "collect-chain" in config["from"][comment.subreddit.display_name]["comments"]:
                pass
                # TODO chain comments

    return result


def filter_comment(comment, config):
    return (
        comment.parent_id.startswith("t3_") # Only first-child comments
        and not comment.stickied  # Mostly for mods lol
        and comment.subreddit.display_name in config["from"]  # Subreddit has to be in settings
        and "comments" in config["from"][comment.subreddit.display_name]  # Comments has to be in subreddit settings
        # TODO title-regex: "#\s*<?(\s*(?:\w\s*)+)>?"
        and (  # If the comments require a title
            ("require-title" in config["from"][comment.subreddit.display_name]["comments"] and comment.body.startswith("#"))
            or "require-title" not in config["from"][comment.subreddit.display_name]["comments"]
        )
        and (  # If there is a delay
            (
                "delay" in config["from"][comment.subreddit.display_name]["comments"]
                and datetime.fromtimestamp(comment.created_utc) < (datetime.now() - timedelta(**config["from"][comment.subreddit.display_name]["comments"]["delay"]))
            )
            or "delay" not in config["from"][comment.subreddit.display_name]["comments"]
        )
    )


def filter_posts(posts, config):
    return [
        p for p in posts
        if p.subreddit.display_name in config["from"]  # Subreddit has to be in settings
        and "posts" in config["from"][p.subreddit.display_name]  # Posts has to be in subreddit settings
    ]
