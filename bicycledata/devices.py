import json
import os
from datetime import datetime, UTC

def check_v2_ident(ident: str) -> bool:
  return ident.isalnum()

def check_v2_device_path(ident: str) -> bool:
  if not check_v2_ident(ident):
    return False
  return os.path.exists(os.path.join('data', 'v2', 'devices', ident))

def load_devices():
  devices = []
  directory = os.path.join('data', 'devices')

  if os.path.exists(directory):
    for ident in os.listdir(directory):
      ident_path = os.path.join(directory, ident)
      if os.path.isdir(ident_path):  # Ensure it's a directory
        info = read_device_info(ident)
        if info:
          devices.append(info)

  # Sort devices by info['ping'] in ascending order
  devices.sort(key=lambda device: device['ping'], reverse=True)

  return devices

def load_v2_devices():
  devices = []
  directory = os.path.join('data', 'v2', 'devices')

  if os.path.exists(directory):
    for ident in os.listdir(directory):
      if not check_v2_ident(ident):
        continue
      ident_path = os.path.join(directory, ident)
      if not os.path.isdir(ident_path):
        continue
      info = read_v2_device_info(ident)
      if info:
        devices.append(info)

  # Sort devices by info['ping'] in ascending order
  devices.sort(key=lambda device: device['ping'], reverse=True)

  return devices

def read_v2_config_file(ident, file_path=None):
  if file_path is None:
    file_path = os.path.join('data', 'v2', 'devices', ident, 'bicycleinit.json')

  try:
    with open(file_path) as f:
      config = f.read()
      return config
  except (FileNotFoundError, json.JSONDecodeError) as e:
    return None

def read_v2_device_info(ident, file_path=None):
  if file_path is None:
    file_path = os.path.join('data', 'v2', 'devices', ident, 'bicycleinit.json')

  try:
    with open(file_path) as f:
      info = json.load(f)

    info['name'] = f"{info['username']}@{info['hostname']}" if 'name' not in info else info['name']
    info['image'] = '/static/images/devices/default.jpg'
    info['ping'], info['online'] = read_last_ping_v2(ident)

    return info

  except (FileNotFoundError, json.JSONDecodeError) as e:
    return None

def read_v2_sessions(ident, all=False):
  directory = os.path.join('data', 'v2', 'devices', ident, 'sessions')
  sessions = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
  if not all:
    sessions = [s for s in sessions if os.path.exists(os.path.join(directory, s, 'bicyclegps'))]
  sessions.sort(reverse=True)
  return sessions

def read_device_info(ident):
  directory = os.path.join('data', 'devices', ident)
  filename = 'config.json'
  file_path = os.path.join(directory, filename)

  try:
    with open(file_path) as f:
      info = json.load(f)

    info['hash'] = ident

    if not 'model' in info:
      info['model'] = 'unknown'
      info['image'] = '/static/images/devices/default.jpg'
    else:
      match info['model']:
        case x if x.lower().startswith('radaride'):
          info['image'] = '/static/images/devices/radaride-v5.png'
        case x if x.lower().startswith('cardilidar'):
          info['image'] = '/static/images/devices/CardiLidar.jpg'
        case _:
          info['image'] = '/static/images/devices/default.jpg'

    if not 'project' in info:
      info['project'] = 'none'

    info['ping'], info['online'] = read_last_ping(ident)

    return info

  except (FileNotFoundError, json.JSONDecodeError) as e:
    return None

def read_config_file(ident):
  directory = os.path.join('data', 'devices', ident)
  filename = 'config.json'
  file_path = os.path.join(directory, filename)

  try:
    with open(file_path) as f:
      config = f.read()
      return config
  except (FileNotFoundError, json.JSONDecodeError) as e:
    return None

def write_config_file(ident, config):
  directory = os.path.join('data', 'devices', ident)
  filename = 'config.json'
  file_path = os.path.join(directory, filename)

  with open(file_path, 'w') as file:
    json.dump(config, file, indent=2)

def write_v2_config_file(ident, config):
  old_config = read_v2_device_info(ident)

  for key in ['ident', 'registration', 'username', 'hostname']:
    if key not in config:
      raise ValueError(f"Missing required key '{key}' in the config.")

    if old_config[key] != config[key]:
      raise ValueError(f"Invalid config file: {key} cannot be changed.")

  with open(os.path.join('data', 'v2', 'devices', ident, 'bicycleinit.json'), 'w') as file:
    json.dump(config, file, indent=2)

def read_last_ping(ident, buffer_size=1024):
  file_path = os.path.join('data', 'devices', ident, 'ping.log')
  try:
    with open(file_path, 'rb') as f:
      # Move the pointer to the end of the file
      f.seek(0, os.SEEK_END)
      file_size = f.tell()
      buffer = b''

      # Read the file in reverse in chunks of buffer_size
      while file_size > 0:
        # Determine how much to read (buffer_size or remaining file size)
        read_size = min(buffer_size, file_size)

        # Move the pointer back by the read size
        f.seek(-read_size, os.SEEK_CUR)

        # Read the chunk and prepend it to the buffer
        buffer = f.read(read_size) + buffer

        # Move the pointer back by the read size again
        f.seek(-read_size, os.SEEK_CUR)

        # Check if we've found a new line character in the buffer
        if b'\n' in buffer:
          # Split the buffer into lines
          lines = buffer.split(b'\n')

          # The last full line will be the last element of the list
          last_line = lines[-2] if len(lines) > 1 else lines[-1]

          # Decode the last line and strip any extra whitespace
          last_line = last_line.decode('utf-8').strip()

          # Extract the timestamp from the last line
          timestamp_str = last_line.split(",")[0]

          # Convert the timestamp string to a datetime object
          last_ping_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

          # Get the current time
          current_time = datetime.now()

          # Calculate the time difference in seconds
          time_difference = (current_time - last_ping_time).total_seconds()

          return timestamp_str, time_difference < 300

      return '0', False

  except Exception as e:
    return '0', False

def read_last_ping_v2(ident, buffer_size=1024):
  file_path = os.path.join('data', 'v2', 'devices', ident, 'ping.log')
  try:
    with open(file_path, 'rb') as f:
      # Move the pointer to the end of the file
      f.seek(0, os.SEEK_END)
      file_size = f.tell()
      buffer = b''

      # Read the file in reverse in chunks of buffer_size
      while file_size > 0:
        # Determine how much to read (buffer_size or remaining file size)
        read_size = min(buffer_size, file_size)

        # Move the pointer back by the read size
        f.seek(-read_size, os.SEEK_CUR)

        # Read the chunk and prepend it to the buffer
        buffer = f.read(read_size) + buffer

        # Move the pointer back by the read size again
        f.seek(-read_size, os.SEEK_CUR)

        # Check if we've found a new line character in the buffer
        if b'\n' in buffer:
          # Split the buffer into lines
          lines = buffer.split(b'\n')

          # The last full line will be the last element of the list
          last_line = lines[-2] if len(lines) > 1 else lines[-1]

          # Decode the last line and strip any extra whitespace
          last_line = last_line.decode('utf-8').strip()

          # Extract the timestamp from the last line
          timestamp_str = last_line.split(",")[0]

          # Convert the timestamp string to a datetime object
          last_ping_time = datetime.fromisoformat(timestamp_str)

          # Get the current time
          current_time = datetime.now(UTC)

          # Calculate the time difference in seconds
          time_difference = (current_time - last_ping_time).total_seconds()

          return timestamp_str, time_difference < 300

      return '0', False

  except Exception as e:
    return '0', False
