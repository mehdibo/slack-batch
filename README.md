# Slack batch
As Slack no longer provides an API to invite people, this is a Selenium Python script to do so.
If you still have a legacy token check [my other repo instead](https://github.com/mehdibo/SlackBatch).

# Installation
## Docker (Recommended)
1. Just run `docker pull mehdibo/slack-batch`

## Directly on machine
1. Make sure you have Python 3.9 installed
2. [Install Geckodriver](https://github.com/mozilla/geckodriver/releases/download)
3. Make sure you have Firefox installed too
4. Run `pip install -r requirements.txt` and `mkdir ./screenshots` to create a screenshots folder

# Usage
## Via Docker (Recommended)

Run:
```sh
docker run --rm \
    -v /tmp:/tmp/files \
    mehdibo/slack-batch emails.txt --workspace https://test.slack.com --email YOUR_EMAIL --passwd YOUR_PASSWORD
```

Replace `/tmp` with the path where your `emails.txt` file exists

If you want to use the `--screenshot` flag

## Directly on machine

```
usage: ./main.py [-h] --workspace WORKSPACE --email EMAIL --passwd PASSWD
                   [--verbose] [--screenshot]
                   emails

Send slack invitations

positional arguments:
  emails                A file that contains one email per line

optional arguments:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        A url to your Slack workspace
  --email EMAIL         Your Slack workspace email
  --passwd PASSWD       Your Slack workspace password
  --verbose             Verbose mode
  --screenshot          Screenshot after every invite
```