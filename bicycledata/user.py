import os
import secrets
from datetime import datetime

import flask_login
from flask import flash, redirect, render_template, request, url_for

from bicycledata import app, dir, login_manager
from bicycledata.slack import SendSlackMessage


class User(flask_login.UserMixin):
  def __init__(self, user):
    self.name = user['name']
    self.id = user['email']
    self.role = user['role']

  @property
  def is_admin(self):
    """Convenience property for templates to check admin role."""
    return getattr(self, 'role', None) == 'admin'

def load_users():
  DIR = os.path.join('data', 'login')
  filename = 'login.md'

  dir.createFileIfNeeded(DIR, filename)

  users = {}
  with open(os.path.join(DIR, filename)) as file:
    for line in file:
      fields = line.rstrip().split(';')
      if len(fields) != 4:
        continue
      email = fields[2]
      users[email] = {'role': fields[0], 'name': fields[1], 'email': fields[2], 'password': fields[3]}
  return users

def add_new_user(name, email):
  DIR = os.path.join('data', 'login')
  filename = 'login.md'

  dir.createFileIfNeeded(DIR, filename)

  password = secrets.token_hex()
  with open(os.path.join(DIR, filename), 'a') as file:
    file.write(f'inactive;{name};{email};{password}\n')

@login_manager.user_loader
def user_loader(email):
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

      SendSlackMessage(f'*login* {user["name"]}')

      with open(os.path.join('data', 'login', token), 'a') as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

      return redirect(url_for('v2_devices'))

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

@app.route('/admin', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
  if not flask_login.current_user.is_admin:
    flash('Access denied')
    return redirect(url_for('index'))

  users = []
  for email, user in load_users().items():
    login_info = "0"
    try:
      with open(os.path.join('data/login/', user['password']), 'r') as f:
        lines = f.readlines()
        login_info = f'{len(lines)} {lines[-1]}'
    except Exception:
      pass
    users.append({'email': email, 'name': user['name'], 'role': user['role'], 'token': user['password'], 'login_info': login_info})
  return render_template('admin.html', users=users)
