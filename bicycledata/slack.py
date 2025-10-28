import slack

from bicycledata import config


def SendSlackMessage(message):
  try:
    client = slack.WebClient(token=config['slack-token'])
    client.chat_postMessage(channel='#bicycledata', text=message)
  except Exception:
    pass
