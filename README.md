# Slack batch
As Slack no longer provides an API to invite people, this is a Selenium Python script to do so.
If you still have a legacy token check [my other repo instead](https://github.com/mehdibo/SlackBatch).

# Installation
## Docker (Recommended)
1. Make sure you have docker installed and running
2. `git clone` the repository and `cd` into it
3. Run `docker build -t slack-back .`

## Directly on machine
1. Make sure you have Python 3.9 installed
2. [Install Geckodriver](https://github.com/mozilla/geckodriver/releases/download)
3. Make sure you have Firefox installed too
4. Run `pip install -r requirements.txt` and `mkdir ./screenshots` to create a screenshots folder

# Usage
## Via Docker (Recommended)

Run:
```shell script
docker run --rm \
    -v /tmp:/tmp/files \
    slack-batch emails.txt --workspace https://test.slack.com --email YOUR_EMAIL --passwd YOUR_PASSWORD
```

Change `/tmp` with the path where your `emails.txt` file exists

If you want to use the `--screenshot` flag