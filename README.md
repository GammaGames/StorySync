# StorySync
Sync reddit stories to a personal sub

## Usage

1. Clone the repo to your computer
2. Copy the `.env.example` file to `.env` and add your own credentials and secrets
3. Copy the `config.yaml.example` file to `config.yaml` and add your own username, subreddits, and such
4. Create an empty sqlite database with `touch app/db.sqlite`
5. Start the container whenever you want to sync your stories with `docker-compose up`

## Configuration

I use a yaml config file to set up where to pull stories to and from:

```yaml
GammaGames:  # Take stories from /u/GammaGames
  count:
    posts: 16  # Only pull the latest 16 posts
    comments: 64  # Only pull the latest 64 comments
  from:  # A list of subreddits to allow past the filter
    WritingPrompts:
      comments:  # Sync comment stories
      - delay:  # Only sync them after a delay. This can be in hours, days, weeks, etc.
          days: 2
      - require-title  # Require a title? I almost always have one
    shortstories:
      posts:  # Sync post stories from r/ss
      - delay:
          days: 2
      comments:  # Sync comment stories, similar as above
      - delay:
          days: 2
      - require-title
  to:  # Post the stories to r/GammeWrites
    GammaWrites
```

Additional notes:

1. It says to pull the latest 64 comments, meaning the newest 64 comments your account has made. If you are very active, it will likely find a much smaller number to sync.
2. I filter out any stories that aren't immediate children of the post. Because of this, Prompt Me responses are not collected
3. If there is a delay and the comment goes past the count before the delay is over, the story will not be synced
4. I filter out stickied comments, because those are usually mod actions
5. I try to pull out titles and sub-titles (for serials)
