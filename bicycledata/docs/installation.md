# Installation Guide

[bicycledata_36ed03d.img](/static/files/bicycledata_36ed03d.img)

## 1. Install Raspberry Pi OS Lite (64-bit)

We recommand the Raspberry Pi Imager to configure and install the OS.

### System Configuration

* **Hostname:**
  Set hostname to "bicycledata"

* **Username and Password:**
  Set a username and password to allow SSH access.

Example configuration:

```
hostname: bicycledata
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

sudo raspi-config
-> Interface Options
-> Serial Port
-> select no (login shell)
-> select yes (enable serial port)
-> finish
-> reboot

```
sudo nano /boot/firmware/config.txt
```
add these two lines under [all]
```
enable_uart=1
dtparam=uart0=on
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

Create vti-nopasswd file:
```
sudo nano /etc/sudoers.d/vti-nopasswd
```

add following line to the vti-nopasswd
```
vti ALL=(ALL) NOPASSWD: /usr/sbin/shutdown, /usr/bin/nmcli, /usr/bin/hciconfig
```

ctrl+x to exit, select yes when asked to save.

enter following line:
```
sudo chmod 440 /etc/sudoers.d/vti-nopasswd
```

Your system should now be fully configured and running the bicycleinit service automatically at startup. After the first handshake, the administrator needs to map the device to your user account. This step is currently performed manually and cannot be completed by a community user. (this might change in the future)
