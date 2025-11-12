import json
import os
import secrets
from datetime import datetime

import flask_login
from flask import flash, redirect, render_template, request, url_for

from bicycledata import app, dir, login_manager
from bicycledata.ntfy import SendMessage


class User(flask_login.UserMixin):
  def __init__(self, user):
    self.name = user['name']
    self.id = user['email']
    self.role = user['role']

  @property
  def is_admin(self):
    """Convenience property for templates to check admin role."""
    return getattr(self, 'role', None) == 'admin'

  @property
  def is_private(self):
    """Convenience property for templates to check private role."""
    role = getattr(self, 'role', None)
    return role in ('admin', 'private')

def load_users():
  """Load users from `data/login/login.json`.

  Supports two formats for compatibility:
  - JSON array of objects with keys 'role','name','email','token' (preferred)
  - legacy semicolon-separated lines (role;name;email;token)
  Returns a dict mapping email -> user dict containing keys 'role','name','email','password'
  where 'password' stores the token used by other parts of the app.
  """
  DIR = os.path.join('data', 'login')

  users = {}
  try:
    path = os.path.join(DIR, 'login.json')
    with open(path, 'r', encoding='utf-8') as fh:
      content = fh.read().strip()
      if not content:
        data = []
      else:
        data = json.loads(content)

    # Expecting a list of user objects
    if isinstance(data, list):
      for item in data:
        role = item.get('role')
        name = item.get('name')
        email = item.get('email')
        token = item.get('token') or item.get('password')
        if not email:
          continue
        users[email] = {'role': role, 'name': name, 'email': email, 'password': token}
    else:
      # Unexpected JSON root; fall back to empty
      return {}
  except FileNotFoundError:
    # Fallback: older semicolon format in a file named login.md
    try:
      path = os.path.join(DIR, 'login.md')
      with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
          fields = line.rstrip().split(';')
          if len(fields) != 4:
            continue
          email = fields[2]
          users[email] = {'role': fields[0], 'name': fields[1], 'email': fields[2], 'password': fields[3]}
    except Exception:
      return {}

  return users

def add_new_user(name, email):
  """Add a new user to `data/login/login.json` and return True if added, False if user exists."""
  DIR = os.path.join('data', 'login')
  filename = 'login.json'

  users = load_users()
  if email not in users:
    token = secrets.token_hex()
    users[email] = {'role': 'inactive', 'name': name, 'email': email, 'password': token}
    dir.createFileIfNeeded(DIR, filename)
    path = os.path.join(DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
      json.dump(list(users.values()), f, indent=2, ensure_ascii=False)
    return True
  return False

def read_user_data(email):
  users = load_users()

  if email not in users:
    raise ValueError("Unknown user email")

  data = {}
  try:
    with open(os.path.join('data/login/', users[email]["password"]), 'r') as f:
      data = json.load(f)
  except Exception:
    pass

  return data

def write_user_data(email, data):
  users = load_users()

  if email not in users:
    raise ValueError("Unknown user email")

  try:
    with open(os.path.join('data/login/', users[email]["password"]), 'w') as f:
      json.dump(data, f, indent=2, ensure_ascii=False)
  except Exception:
    pass

@login_manager.user_loader
def get_user_by_email(email):
  users = load_users()

  if email not in users:
    return None

  user = users[email]

  if user['role'] == 'inactive':
    return None

  login_user = User(user)
  return login_user

@login_manager.unauthorized_handler
def unauthorized_handler():
  return redirect(url_for('login'))

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

      SendMessage(f'*login* {user["name"]}')

      udata = read_user_data(user['email'])
      udata['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      udata['num_logins'] = udata.get('num_logins', 0) + 1
      write_user_data(user['email'], udata)

      return redirect(url_for('user_sessions'))

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

  if not add_new_user(name, email):
    flash('User with this email already exists.')
    return redirect(url_for('login'))

  flash('All accounts get activated manually. You will get an email as soon as your request is processed.')
  SendMessage(f'*signup* New user requests access: {name}, {email}')
  return redirect(url_for('index'))

@app.route('/logout')
@flask_login.login_required
def logout():
  flask_login.logout_user()
  return redirect(url_for('index'))

@app.route('/sessions')
@flask_login.login_required
def user_sessions():
  udata = read_user_data(flask_login.current_user.id)
  sessions = []
  for s in udata.get('sessions', []):
    device, date = s.split('/', 1)
    sessions.append({'device': device, 'date': date})
  sessions.sort(key=lambda x: x['date'], reverse=True)
  return render_template('user_sessions.html', sessions=sessions)

@app.route('/admin', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
  if not flask_login.current_user.is_admin:
    flash('Access denied')
    return redirect(url_for('index'))

  users = []
  for email, user in load_users().items():
    udata = read_user_data(email)
    users.append({'email': email, 'name': user['name'], 'role': user['role'], 'token': user['password'], 'last_login': udata.get("last_login", "n/a"), 'num_login': udata.get("num_logins", 0)})
  return render_template('admin.html', users=users)
