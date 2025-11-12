import requests

from bicycledata import config


def SendMessage(message):
  url = config.get('ntfy-url')
  token = config.get('ntfy-token')
  if not url or not token:
    return

  try:
    requests.post(url, data=message, headers={"Authorization": f"Bearer {token}"}, timeout=2)
  except Exception:
    pass
