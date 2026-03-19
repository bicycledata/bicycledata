# Installation Guide

## 1. Install Raspberry Pi OS Lite (64-bit)

We recommand the Raspberry Pi Imager to configure and install the OS.

### System Configuration

* **Hostname:**
  The hostname must be unique.
  We use the format `radaridevX`, where `X` is incremented for each device (e.g., `radaridev10`).
  For community-owned devices, use a similar naming scheme but with a different prefix.

* **Username and Password:**
  Set a username and password to allow SSH access.

Example configuration:

```
hostname: radaridev10   # <- Use a unique hostname!
username: <user>
password: *****

WiFi SSID: bicycledata   # <- important!
WiFi password: bicycledata  # <- important!
Country: SE

Locale settings:
Region: Stockholm
Timezone: Europe/Stockholm

Enable SSH with password authentication
```

## 2. Initial System Setup

Update the system and install required packages:

```zsh
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y git jq curl btop
```


## 3. Setup bicycleinit

Clone the repository and create a virtual environment:

```zsh
git clone https://github.com/bicycledata/bicycleinit.git ~/bicycleinit
cd ~/bicycleinit

python3 -m venv .env --system-site-packages
source .env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```


## 4. Configure the Systemd Service

Create the systemd service file:

```zsh
sudo nano /etc/systemd/system/bicycleinit.service
```

Copy the following content and replace `<user>` with the username you selected earlier:

```ini
[Unit]
Description=bicycleinit service
After=network.target

[Service]
User=<user>
Group=<user>
WorkingDirectory=/home/<user>/bicycleinit
ExecStart=/home/<user>/bicycleinit/.env/bin/python3 bicycleinit.py

Restart=always
RestartSec=5
StartLimitInterval=0
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
```

Save and exit.


## 5. Enable and start the Service

```zsh
sudo systemctl daemon-reload
sudo systemctl enable bicycleinit
sudo systemctl start bicycleinit
```

To verify that the service is running:

```zsh
sudo systemctl status bicycleinit
```

Your system should now be fully configured and running the bicycleinit service automatically at startup. After the first handshake, the administrator needs to map the device to your user account. This step is currently performed manually and cannot be completed by a community user. (this might change in the future)
