import json
import os
import secrets
from datetime import UTC, datetime

import flask_login
import slack
from discord import SyncWebhook
from flask import (Response, abort, flash, jsonify, make_response, redirect,
                   render_template, request, send_from_directory, url_for)

from bicycledata import app, config, dir, login_manager
from bicycledata.devices import (check_v2_device_path, load_devices,
                                 load_v2_devices, read_config_file,
                                 read_device_info, read_v2_config_file,
                                 read_v2_device_info, read_v2_sessions,
                                 write_config_file, write_v2_config_file)
from bicycledata.user import User, add_new_user, load_users


def SendDiscordMessage(message):
  try:
    webhook = SyncWebhook.from_url(config['discord-webhook'])
    webhook.send(message)
  except Exception:
    pass

def SendSlackMessage(message):
  try:
    client = slack.WebClient(token=config['slack-token'])
    client.chat_postMessage(channel='#bicycledata', text=message)
  except Exception:
    pass

@app.after_request
def after_request(response):
  # Log all requests except for successful ones (200) and not modified (304)
  if response.status_code in (200, 304):
    return response

  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  DIR = os.path.join('data', 'log')
  filename = 'requests.md'

  dir.createDirIfNeeded(DIR)

  with open(os.path.join(DIR, filename), 'a') as file:
    file.write('{} | {} | {} | {} | {} | {}\n'.format(timestamp, request.remote_addr, request.scheme, request.method, request.full_path, response.status))

  return response

@app.route('/')
def index():
  return render_template('index.html')

###
###
### NEW API endpoints (v2)
### START
###
###

@app.route('/api/v2/time', methods=['GET', 'POST'])
def api_v2_time():
  try:
    if request.method == 'GET':
      return jsonify({"server_time": datetime.now(UTC).isoformat()})

    server_time = datetime.now(UTC).isoformat()
    client_time = datetime.fromisoformat(request.json.get('client_time'))
    diff = datetime.fromisoformat(server_time) - client_time
    return jsonify({"server_time": server_time, "diff": diff.total_seconds()})
  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/v2/register', methods=['POST'])
def api_v2_register():
  # Generate a unique hash
  ident = secrets.token_hex()
  device_path = os.path.join('data', 'v2', 'devices', ident)
  sessions_path = os.path.join(device_path, 'sessions')

  # Make sure that the device doesn't already exist
  if check_v2_device_path(ident):
    return jsonify({"error": "Please try again."}), 404

  try:
    data = request.get_json()

    if not isinstance(data, dict):
      return jsonify({"error": "Invalid data format, expected a JSON object"}), 400

    # Add the registration timestamp
    data['registration'] = datetime.now(UTC).isoformat()

    # Add device ident
    data['ident'] = ident

    # Add a default sensor
    data['sensors'] = [ {'name': 'sensor_template', 'git_url': 'https://github.com/bicycledata/sensor_template.git', 'git_branch': 'api-v2', 'entry_point': 'sensor:main', 'restart': False, 'args': {'upload_interval': 5}} ]

    os.makedirs(device_path, exist_ok=True)
    os.makedirs(sessions_path, exist_ok=True)

    file_path = os.path.join(device_path, 'bicycleinit.json')
    with open(file_path, 'w') as file:
      json.dump(data, file, indent=2)

    SendDiscordMessage(f'[v2] *register* {data["username"]}@{data["hostname"]} ({ident})')
    with open(os.path.join(device_path, 'ping.log'), 'a') as f:
      f.write(datetime.now(UTC).isoformat() + ", /api/v2/register\n")

    return jsonify(data), 201  # 201 Created status

  except json.JSONDecodeError:
    return jsonify({"error": "Invalid JSON format"}), 400

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/v2/config', methods=['POST'])
def api_v2_config():
  payload = request.get_json()

  # Make sure that payload is dictionary and contains required fields: ident
  if not isinstance(payload, dict) or 'ident' not in payload:
    return jsonify({"error": "Invalid data format, expected a JSON object with valid 'ident'"}), 400

  ident = payload['ident']
  device_path = os.path.join('data', 'v2', 'devices', ident)

  # Make sure that the device doesn't already exist
  if not check_v2_device_path(ident):
    return jsonify({"error": "Device not found"}), 404

  file_path = os.path.join(device_path, 'bicycleinit.json')

  try:
    with open(file_path, 'r') as file:
      data = json.load(file)

    SendDiscordMessage(f'[v2] *config* {data["username"]}@{data["hostname"]} ({ident})')
    with open(os.path.join(device_path, 'ping.log'), 'a') as f:
      f.write(datetime.now(UTC).isoformat() + ", /api/config\n")

    return jsonify(data)

  except json.JSONDecodeError:
    return jsonify({"error": "Invalid JSON format"}), 400

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/v2/session/upload', methods=['POST'])
def api_v2_session_upload_chunk():
  try:
    payload = request.get_json()

    # Make sure that payload is dictionary and contains required fields: ident, session, log
    if not isinstance(payload, dict) or 'ident' not in payload or 'session' not in payload or 'filename' not in payload or 'data' not in payload:
      return jsonify({"error": "Invalid data format, expected a JSON object with 'ident', 'session', 'filename' and 'data' fields"}), 400

    ident = payload['ident']
    session = payload['session']
    filename = payload['filename']
    data = payload['data']

    # Check ident
    if check_v2_device_path(ident) is False:
      return jsonify({"error": "Device not found"}), 400

    # Check session format
    try:
      datetime.strptime(session, '%Y%m%d-%H%M%S')
    except ValueError:
      return jsonify({"error": "Invalid session format"}), 400

    # Create data/devices/<ident>/sessions/<session> directory if it does not exist
    file_path = os.path.join('data', 'v2', 'devices', ident, 'sessions', session)
    os.makedirs(file_path, exist_ok=True)

    # Append log to data/devices/<ident>/sessions/<session>/bicycleinit.log
    log_path = os.path.join(file_path, filename)
    with open(log_path, 'a') as file:
      file.write(data)
    return jsonify({"status": "ok"}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route('/v2/devices')
@flask_login.login_required
def v2_devices():
  devices = load_v2_devices()
  return render_template('devices_v2.html', devices=devices)


@app.route('/v2/devices/<ident>', methods=['GET', 'POST'])
@flask_login.login_required
def v2_devices_ident(ident):
  if request.method == 'GET':
    all_sessions = request.args.get('all', '0') == '1'
    device = read_v2_device_info(ident)
    config = read_v2_config_file(ident)
    sessions = read_v2_sessions(ident, all_sessions)
    if device:
      return render_template('devices_v2_ident.html', device=device, config=config, sessions=sessions)
    return render_template('404.html'), 404

  # POST
  config = request.form['config']
  try:
    config = json.loads(config)
    write_v2_config_file(ident, config)
    SendDiscordMessage(f'[v2] *config updated* {ident}')
  except (FileNotFoundError, json.JSONDecodeError) as e:
    flash("Failed to update config.json. Please verify that the file has correct JSON syntax and try again.")
  except ValueError as e:
    flash(f"Failed to update config.json: {e}")

  return redirect(url_for('v2_devices_ident', ident=ident))


@app.route('/v2/devices/<ident>/sessions/<session>')
@flask_login.login_required
def v2_devices_ident_session(ident, session):
  try:
    session_dir = os.path.join('data', 'v2', 'devices', ident, 'sessions', session)
    device = read_v2_device_info(ident, file_path=os.path.join(session_dir, 'bicycleinit.json'))
    config = read_v2_config_file(ident, file_path=os.path.join(session_dir, 'bicycleinit.json'))
    try:
      log = open(os.path.join(session_dir, 'bicycleinit.log')).read()
    except Exception:
      log = None
    sensors = [name for name in os.listdir(session_dir) if os.path.isfile(os.path.join(session_dir, name)) and name != 'bicycleinit.log' and name != 'bicycleinit.json']
    sensors.sort()

    session_info = {'name': session,
                    'start': '---',
                    'end': '---',
                    'duration': '---'
                    }

    # GPS track extraction
    gps_track = []
    gps_file = os.path.join(app.root_path, '..', session_dir, 'bicyclegps')
    if os.path.isfile(gps_file):
      import csv
      with open(gps_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
          try:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            gps_track.append([lat, lon])
            if session_info['start'] == '---':
              session_info['start']  = datetime.fromisoformat(row['time']).astimezone().strftime('%Y-%m-%d %H:%M')
              start_time = datetime.fromisoformat(row['time'])
            session_info['end'] = datetime.fromisoformat(row['time']).astimezone().strftime('%Y-%m-%d %H:%M')
            duration = datetime.fromisoformat(row['time']) - start_time
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            session_info['duration'] = f"{hours}h {minutes}min"
          except Exception:
            continue

    return render_template(
      'devices_v2_ident_session.html',
      device=device,
      config=config,
      session=session_info,
      log=log,
      sensors=sensors,
      gps_track=gps_track
    )
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route('/v2/devices/<ident>/sessions/<session>/sensors/<sensor>')
@flask_login.login_required
def v2_devices_ident_sessions_session_sensors_sensor(ident, session, sensor):
  if not check_v2_device_path(ident):
    return jsonify({"error": "Device not found"}), 404

  try:
    directory = os.path.join(app.root_path, '..', 'data', 'v2', 'devices', ident, 'sessions', session)
    return send_from_directory(directory, sensor, mimetype='text/plain', as_attachment=True)
  except Exception as e:
    return jsonify({"error": str(e)}), 500

###
###
### END
### NEW API endpoints (v2)
###
###




###
###
### OLD API endpoints (v1)
### START
###
###

@app.route('/api/time')
def api_time():
  return jsonify({"time": datetime.utcnow().isoformat() + 'Z'})

@app.route('/api/register', methods=['POST'])
def api_register():
  # Generate a unique hash
  hash_value = secrets.token_hex()
  dir_path = f'data/devices/{hash_value}'

  if os.path.exists(dir_path):
    return jsonify({"error": "Please try again."}), 404

  try:
    data = request.get_json()

    if not isinstance(data, dict):
      return jsonify({"error": "Invalid data format, expected a JSON object"}), 400

    # Add the registration timestamp
    data['registration'] = datetime.utcnow().isoformat() + 'Z'  # ISO 8601 format with 'Z' for UTC
    data['sensors'] = [ {'name': 'sensor_template', 'git_url': 'https://github.com/bicycledata/sensor_template.git', 'git_version': 'main', 'entry_point': 'sensor.py', 'args': ['--upload-interval', '5']} ]
    if 'project' not in data:
      data['project'] = 'dev'
    if 'model' not in data:
      data['model'] = 'unknown'

    dir.createDirIfNeeded(dir_path)

    file_path = os.path.join(dir_path, 'config.json')
    with open(file_path, 'w') as file:
      json.dump(data, file, indent=2)

    SendDiscordMessage(f'*register* {data["username"]}@{data["hostname"]} ({hash_value})')
    with open(os.path.join(dir_path, 'ping.log'), 'a') as f:
      f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", /api/register\n")

    return jsonify({'hash': hash_value}), 201  # 201 Created status

  except json.JSONDecodeError:
    return jsonify({"error": "Invalid JSON format"}), 400

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/config')
def api_config():
  hash_value = request.args.get('hash')
  dir_path = f'data/devices/{hash_value}'

  file_path = os.path.join(dir_path, 'config.json')

  if not os.path.exists(dir_path):
    return jsonify({"error": "Device not found"}), 404

  try:
    with open(file_path, 'r') as file:
      data = json.load(file)

    SendDiscordMessage(f'*config* {data["username"]}@{data["hostname"]} ({hash_value})')
    with open(os.path.join(dir_path, 'ping.log'), 'a') as f:
      f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", /api/config\n")

    return jsonify(data)

  except json.JSONDecodeError:
    return jsonify({"error": "Invalid JSON format"}), 400

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@app.route('/api/sensor/update', methods=['POST'])
def api_sensor_update():
  data = request.get_json()

  hash = data.get('hash')
  sensor = data.get('sensor')

  dir_path = f'data/devices/{hash}'

  if not os.path.exists(dir_path):
    return jsonify({"error": "Device not found"}), 404

  dir.createDirIfNeeded(dir_path + '/sensors/')

  with open(dir_path + '/sensors/' + sensor + '.latest', 'w') as file:
    file.writelines(data['csv_data'])

  with open(dir_path + '/sensors/' + sensor, 'a') as file:
    file.writelines(data['csv_data'])

  with open(os.path.join(dir_path, 'ping.log'), 'a') as f:
    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", /api/sensor/update\n")

  return 'Ok'

@app.route('/api/<hash>/sensor/<name>')
def api_hash_sensor_name(hash, name):
    if not hash.isalnum():
        return jsonify({"error": "Invalid input"}), 400

    sensor_path = os.path.join('data', 'devices', hash, 'sensors', name)

    if not os.path.exists(sensor_path):
        return jsonify({"error": "Device or sensor not found"}), 404

    try:
        with open(sensor_path, 'r') as file:
            data = file.readlines()

        data = [x.rstrip() for x in data]

        return jsonify({'sensor': name, "data": data})

    except IOError as e:
        return jsonify({"error": "Error reading the file", "details": str(e)}), 500

@app.route('/generic')
@flask_login.login_required
def generic():
  return render_template('generic.html')

@app.route('/elements')
@flask_login.login_required
def elements():
  return render_template('elements.html')

@app.route('/devices')
@flask_login.login_required
def devices():
  devices = load_devices()
  return render_template('devices.html', devices=devices)

@app.route('/devices/<ident>', methods=['GET', 'POST'])
def devices_ident(ident):
  if request.method == 'GET':
    device = read_device_info(ident)
    config = read_config_file(ident)
    if device:
      return render_template('devices_ident.html', device=device, config=config)
    return render_template('404.html'), 404

  # POST
  config = request.form['config']
  try:
    config = json.loads(config)
    write_config_file(ident, config)
    SendDiscordMessage(f'*config updated* {ident}')
  except (FileNotFoundError, json.JSONDecodeError) as e:
    flash("Failed to update config.json. Please verify that the file has correct JSON syntax and try again.")

  return redirect(url_for('devices_ident', ident=ident))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

  token = request.form['password']
  return redirect(url_for('login_with_token', token=token))

@app.route('/login/<token>')
def login_with_token(token):
  users = load_users()
  for user in users.values():
    if user['password'] == token:
      if user['role'] == 'inactive':
        flash('User is not yet activated')
        return redirect(url_for('login'))

      login_user = User(user)
      flask_login.login_user(login_user)

      SendSlackMessage(f'*login* {user["name"]}')

      with open(os.path.join('data', 'login', token), 'a') as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

      return redirect(url_for('index'))

  flash('Bad login')
  return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
def signup():
  if not request.method == 'POST':
    return redirect(url_for('login'))

  name = request.form['name']
  email = request.form['email']

  if not name or not email:
    flash('Registration failed: both name and email are required')
    return redirect(url_for('login'))

  users = load_users()
  if len(users) > 100:
    flash('There is unusually high traffic at the moment. Please try to send your message later again.')
    return redirect(url_for('index'))

  if not email in users:
    add_new_user(name, email)

  flash('All accounts get activated manually. You will get an email as soon as your request is processed.')
  SendSlackMessage(f'*signup* New user requests access: {name}, {email}')
  return redirect(url_for('index'))

@app.route('/logout')
@flask_login.login_required
def logout():
  flask_login.logout_user()
  return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  DIR = 'data/contact/'

  if not request.method == 'POST':
    comments = []
    users = []

    if not flask_login.current_user.is_anonymous and flask_login.current_user.role == "admin":
      for email, user in load_users().items():
        login_info = "0"
        try:
          with open(os.path.join('data/login/', user['password']), 'r') as f:
            lines = f.readlines()
            login_info = f'{len(lines)} {lines[-1]}'
        except Exception:
          pass
        users.append({'email': email, 'name': user['name'], 'role': user['role'], 'token': user['password'], 'login_info': login_info})
    return render_template('contact.html', comments=comments, users=users)

  dir.createDirIfNeeded(DIR)

  num_comments = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
  if num_comments >= 100:
    flash('There is unusually high traffic at the moment, which forced us to stop receiving messages. Please try to send your message later again.')
    filename = 'last.md'
  else:
    filename = f'{num_comments+1}.md'

  date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  name = request.form['name']
  email = request.form['email']
  message = request.form['message']

  SendSlackMessage(f'*message* new message received from {name}, {email}')

  with open(os.path.join(DIR, filename), 'w') as file:
    file.write('---\n')
    file.write(f'"date":  "{date}",\n')
    file.write(f'"name":  "{name}",\n')
    file.write(f'"email": "{email}"\n')
    file.write('---\n')
    file.write(message)
    return redirect(url_for('index'))

@app.route('/devices/<hash>/sensors/<sensor>/latest')
@flask_login.login_required
def devices_sensor_tail(hash, sensor):
  directory = os.path.join(app.root_path, '..', 'data', 'devices', hash, 'sensors')
  return send_from_directory(directory, sensor + '.latest', mimetype='text/plain', as_attachment=False)

@app.route('/devices/<hash>/sensors/<sensor>')
@flask_login.login_required
def devices_sensor(hash, sensor):
  directory = os.path.join(app.root_path, '..', 'data', 'devices', hash, 'sensors')
  return send_from_directory(directory, sensor, mimetype='text/plain', as_attachment=True)

###
###
### END
### OLD API endpoints (v1)
###
###

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(app.static_folder, 'favicon/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
  return send_from_directory(app.static_folder, 'favicon/apple-touch-icon.png', mimetype='image/png')

@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon_precomposed():
  return send_from_directory(app.static_folder, 'favicon/apple-touch-icon.png', mimetype='image/png')

@app.route('/robots.txt')
def robots():
  return send_from_directory(app.static_folder, 'robots.txt')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404
