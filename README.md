# Is this a pigeon?

Twitter bot for generating "Is this a pigeon?" memes when you mention its
handle

## Hosted on [Glitch.com](https://glitch.com)

1. Import the GitHub repository into Glitch

2. Add the environment variables to `.env`

```sh
TWITTER_CONSUMER_KEY=<insert-consumer-key>
TWITTER_CONSUMER_SECRET=<insert-consumer-secret>
TWITTER_ACCESS_TOKEN=<insert-access-token>
TWITTER_ACCESS_TOKEN_SECRET=<insert-access-token-secret>
```

3. Wait for Glitch to install dependencies and start the bot

4. Set up an uptime monitoring service, such as
   [UptimeRobot](https://uptimerobot.com/) to prevent the project from going to
   sleep due to inactivity

## Self-hosted

### Installation

1. Install [PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html)

2. Install Python dependencies

```sh
pip3 install -U -r requirements.txt
```

### Usage

1. Set up the environment variables

```sh
export TWITTER_CONSUMER_KEY="<insert-consumer-key>"
export TWITTER_CONSUMER_SECRET="<insert-consumer-secret>"
export TWITTER_ACCESS_TOKEN="<insert-access-token>"
export TWITTER_ACCESS_TOKEN_SECRET="<insert-access-token-secret>"
```

2. Start the bot

```sh
./main.py
```
