import os
import shutil
import subprocess
import dir
from datetime import datetime
import time


def file_sanity_check(filename):
  return os.path.isfile(filename) and os.path.getsize(filename) > 0


def log(file_path, message):
  with open(file_path, 'a', encoding='utf-8') as f:
    f.write(message +'\n')


def post_process():
  log_device_discovered_ctr = 0
  log_sessions_discovered_ctr = 0
  log_sessions_processed_ctr = 0
  log_sessions_skipped_ctr = 0
  log_sessions_failed_ctr = 0
  log_session_action = 'unprocessed'
  try:
    log_path = os.path.join('..', 'data', 'log', 'postprocess')
    log_file = os.path.join(log_path, datetime.now().strftime("%Y%m%d-%H%M%S") + '.log')
    dir.createDirIfNeeded(log_path)
    log(log_file, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | postprocess start")

    devices_dir = os.path.join('..', 'data', 'v2', 'devices')
    for device in os.listdir(devices_dir):
      log_device_discovered_ctr += 1
      
      sessions_dir = os.path.join(devices_dir, device, 'sessions')
      for session in os.listdir(sessions_dir):
        log_session_start = time.time()
        log_sessions_discovered_ctr += 1
        bicyclebutton_file = os.path.join(sessions_dir, session, 'bicyclebutton')
        bicyclegps_file = os.path.join(sessions_dir, session, 'bicyclegps')
        bicyclelidar_file = os.path.join(sessions_dir, session, 'bicyclelidar')
        postprocess_dir = os.path.join(sessions_dir, session, 'postprocess')

        if os.path.isdir(postprocess_dir):
          log_sessions_skipped_ctr += 1
          log_session_action = 'skipped'
          print("postprocess already done for session: ", session)
          log(log_file, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Device ID " + str(device) + " | Session ID " + str(session) + " | Action " + log_session_action + " | Execution time[s]: " + str(time.time()-log_session_start))
          continue
        if not (file_sanity_check(bicyclebutton_file) and file_sanity_check(bicyclegps_file) and file_sanity_check(bicyclelidar_file)):
          log_sessions_skipped_ctr += 1
          log_session_action = 'skipped because incomplete'
          print("data incomplete for session: ", session)
          log(log_file, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Device ID " + str(device) + " | Session ID " + str(session) + " | Action " + log_session_action + " | Execution time[s]: " + str(time.time()-log_session_start))
          continue
        
        dir.createDirIfNeeded(postprocess_dir)
        result = subprocess.run(['.venv/bin/python3', 'bicycledigest.py', '-b', bicyclebutton_file, '-g', bicyclegps_file, '-l', bicyclelidar_file, '-o', postprocess_dir], cwd='../bicycledigest', capture_output=True, text=True)
        
        if result.returncode != 0:
          shutil.rmtree(postprocess_dir)
          log_sessions_failed_ctr += 1
          log_session_action = 'failed'
          print("postprocess data failed for session: ", session)
          log(log_file, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Device ID " + str(device) + " | Session ID " + str(session) + " | Action " + log_session_action + " | Execution time[s]: " + str(time.time()-log_session_start))
          continue
        
        dir.createFileIfNeeded(postprocess_dir, 'postprocess.txt')
        with open(os.path.join(sessions_dir, session, 'postprocess', 'postprocess.txt'), "w") as f:
          f.write(result.stdout)
          log_sessions_processed_ctr += 1
          log_session_action = 'processed'
          print("postprocess data written for session: ", session)
          log(log_file, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | Device ID " + str(device) + " | Session ID " + str(session) + " | Action " + log_session_action + " | Execution time[s]: " + str(time.time()-log_session_start))

  except Exception as e:
    log(log_file, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | postprocess exception: " + str(e)))
  log(log_file, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | postprocess end results" + " | sessions discovered: " + str(log_sessions_discovered_ctr) + " | sessions processed: " + str(log_sessions_processed_ctr) + " | sessions skipped: " + str(log_sessions_skipped_ctr)))


if __name__ == '__main__':
  post_process()

