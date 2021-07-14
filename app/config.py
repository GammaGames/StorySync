import yaml


def load_config():
    data = yaml.safe_load(open("/opt/config.yaml"))

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
    return [
        c for c in comments
        if c.parent_id.startswith("t3_")  # Only first-child comments
        and c.subreddit.display_name in config["from"]  # Subreddit has to be in settings
        and "comments" in config["from"][c.subreddit.display_name]  # Comments has to be in subreddit settings
        and (  # If the comments require a title
            ("require-title" in config["from"][c.subreddit.display_name]["comments"] and c.body.startswith("#"))
            or True
        )
        and (  # If there is a delay
            True
        )
    ]


def filter_posts(posts, config):
    pass
