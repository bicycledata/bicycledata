import json
import os
import secrets
from datetime import datetime

import flask_login
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import flash, redirect, render_template, request, url_for

from bicycledata import app, config, dir, login_manager
from bicycledata.email import send_email
from bicycledata.ntfy import SendMessage


class User(flask_login.UserMixin):
  def __init__(self, user):
    self.id = user['id']
    self.name = user['name']
    self.email = user['email']
    self.role = user['role']    # inactive, public, private, admin
    self.hash = user['hash']
    self.last_login = user['last_login']
    self.num_logins = user['num_logins']
    self.sessions = user['sessions']

  def save(self):
    user = {
             'id': self.id,
             'name': self.name,
             'email': self.email,
             'role': self.role,
             'hash': self.hash,
             'last_login': self.last_login,
             'num_logins': self.num_logins,
             'sessions': self.sessions
           }
    save_user(user)

  @property
  def is_admin(self):
    """Convenience property for templates to check admin role."""
    return self.role == 'admin'

  @property
  def is_private(self):
    """Convenience property for templates to check private role."""
    return self.role in ('admin', 'private')

def save_user(user):
  DIR = os.path.join('data', 'login')
  dir.createDirIfNeeded(DIR)
  path = os.path.join(DIR, f"{user['id']}.json")
  with open(path, 'w') as f:
    json.dump({
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'hash': user['hash'],
                'last_login': user['last_login'],
                'num_logins': user['num_logins'],
                'sessions': user['sessions']
              }, f, indent=2)


def load_users():
  DIR = os.path.join('data', 'login')

  # load users from all .json files in DIR
  users = []
  if os.path.isdir(DIR):
    for fname in os.listdir(DIR):
      if not fname.endswith('.json'):
        continue
      with open(os.path.join(DIR, fname), 'r') as f:
        user = json.load(f)
      users.append(user)

  return users

def load_user_by_id(user_id):
  users = load_users()

  for user in users:
    if user['id'] == user_id and user['role'] != 'inactive':
      return user

  return None

def add_new_user(name, email):
  DIR = os.path.join('data', 'login')

  users = load_users()

  # check if any user already has this email
  if any(u['email'] == email for u in users):
    return False

  # create a new user
  ph = PasswordHasher()
  password = secrets.token_hex(16)

  user = {
          'id': secrets.token_hex(3),
          'name': name,
          'email': email,
          'role': 'public',
          'hash': ph.hash(password),
          'last_login': "n/a",
          'num_logins': 0,
          'sessions': []
        }

  # ensure unique user ID
  while any(u['id'] == user['id'] for u in users):
    user['id'] += secrets.token_hex(1)

  save_user(user)

  subject = "BicycleData account created"
  body = f'email: {email}\npassword: {password}\n\nPlease keep this information safe. You will need the password to log in to your account.'
  send_email(email, subject, body, config)

  return True

@login_manager.user_loader
def get_user_by_id(user_id):
  user = load_user_by_id(user_id)

  if user:
    return User(user)

  return None

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
  ph = PasswordHasher()
  users = load_users()
  for user in users:
    try:
      ph.verify(user['hash'], token)
    except VerifyMismatchError:
      continue

    if user['role'] == 'inactive':
      flash('User is not yet activated')
      return redirect(url_for('login'))

    user['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user['num_logins'] = user.get('num_logins', 0) + 1
    save_user(user)

    login_user = User(user)
    flask_login.login_user(login_user)

    SendMessage(f'*login* {user["name"]}')

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
    flash('There is unusually high traffic at the moment. Please try to signup later again.')
    return redirect(url_for('index'))

  if not add_new_user(name, email):
    flash('User with this email already exists.')
    return redirect(url_for('login'))

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
  sessions = []
  for s in flask_login.current_user.sessions:
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
  for user in load_users():
    users.append({'email': user['email'], 'name': user['name'], 'id': user['id'], 'role': user['role'], 'last_login': user["last_login"], 'num_login': user["num_logins"]})
  return render_template('admin.html', users=users)
