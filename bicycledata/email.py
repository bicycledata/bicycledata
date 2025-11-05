import smtplib
from email.message import EmailMessage


def send_email(to, subject, body, config):
  smtp_host = config.get('smtp-host')
  smtp_port = config.get('smtp-port')
  smtp_from = config.get('smtp-from')

  # Build message
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = smtp_from
  msg['To'] = to
  msg.set_content(body)

  server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
  status = {'success': False, 'error': None}
  try:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.send_message(msg)
    status['success'] = True
  except Exception as e:
    status['error'] = str(e)
  finally:
    server.quit()

  return status
