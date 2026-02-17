# Build Instructions

## Bill of Materials (BOM)
1. Print all parts in PETG (345,06g incl. support) (116kr) [Bicycledata v2.3mf](/static/files/Bicycledata v2.3mf)
    * Box Body
    * Box Bottom
    * Pi Tray
    * Top Rail
    * Rear Mount
    * USB Mount (part A)
    * USB Mount (part B)
    * Switch Mount
    * Box Top

2. Core Electronics (4383kr)
    * 1x Raspberry Pi 5 (4GB RAM) [price: 829kr](https://www.electrokit.com/raspberry-pi-5-4gb)
    * 1x microSD card (32GB) [price: 149kr](https://www.electrokit.com/minneskort-microsd-a2-class-32gb-raspberry-pi)
    * 1x USB GPS module [price: 249kr](https://www.electrokit.com/gps-mottagare-usb-dfrobot-tel0137)
    * 1x LiDAR sensor TFMini-S [price: 769kr](https://www.electrokit.com/avstandsgivare-lidar-0.1-12m-tf-mini-s)
    * 1x Garmin Varia RVR315 [price: 1599kr](https://www.garmin.com/sv-SE/p/669024/pn/010-02253-00/)
    * 1x Powerbank Anker Nano [price: 699kr](https://www.amazon.se/Anker-Powerbank-powerbank-USB-C-kabel-kompatibel/dp/B0C9CJKCH3/ref=asc_df_B0C9CJKCH3?mcid=44fa350b25113a49a44dd1843a368505&tag=shpngadsglede-21&linkCode=df0&hvadid=719621620464&hvpos=&hvnetw=g&hvrand=10941814230683062894&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062421&hvtargid=pla-2197490552831&language=sv_SE&gad_source=1&th=1)
    * 1x RTC-batteri för Raspberry Pi 5 [price: 89kr](https://www.electrokit.com/rtc-batteri-for-raspberry-pi-5)

3. USB & Power Components
    * 1× USB-C female connector
    * 1× USB-C female connector with CC support
    * 1× USB-C male connector with CC support
    * Data cable + connectors (e.g. Molex)

4. User Interface Components
    * 1x 4-pin on-off switch
    * 1x push button
    * 3x led
    * 1x push button (for OT)

5. Mechanical & Mounting Hardware
    * 4× M2.5×6 screws (for mounting the Raspberry Pi)
    * 1× 60×80×1 mm metal plate (metallplåt)
    * 1× M5×20 bolt + lock nut (rear mount)
    * 12× M4×10 bolts + lock nuts (for the enclosure / *lock*) [link](https://www.amazon.se/Cylinderhuvudskruvar-Zinkpl%C3%A4terad-Fasteners-Cylindrical-Certified/dp/B09446MZL1/ref=sr_1_3?crid=2YMGE7AE67AT&dib=eyJ2IjoiMSJ9.elDdXwmNjtOsCUoqT0DnAT1FkysZOxggMbxHYPMo64oqTNi6N4xkq6KkJZyZrpgyGzLy6vMwyF__uHmvk0rz9G5S9hxxMaoErbv4socIZucftnMkdhfBdIzJ0mtsIndXvBGom1QPUMuUGzE-9Pt4yEcEFrdSgLLy9s1PIWAqsRCMgM-1nRvNHGphLJwkxffvF7amRyPBP8T4M37bfNdIT0I6OpfJ1JS_rXIKXsIc-h8eSl5XvTJ7bjFyBKW35ywttgO9XBZkOYVXCQfw6Stbn5K7LJHnSAsWd2Wo_FWvGbY.yVHheR_4ZdCm-XGuWqlWZP7afv_R3SczEzjlB81FeU4&dib_tag=se&keywords=M4x10%2Bhex&qid=1768824131&sprefix=m4x10%2Bhex%2Caps%2C122&sr=8-3&th=1)
    * 1× Garmin SEAT RAIL MOUNT KIT [price: 459kr](https://www.garmin.com/sv-SE/p/874032/)

6. Enclosure & Display Parts
    * 1x 24x35x2mm plastic glass (plexiglas / plastglas)


## Pin Schema

1. LiDAR
    * PIN 04: 5v
    * PIN 06: Ground
    * PIN 08: GPIO 14: UART0 TX
    * PIN 10: GPIO 15: UART0 RX

    From the back, connector on the top: Ground, 5V. TX, RX

2. Button OT
    * D+ -> PIN 14: Ground
    * D- -> PIN 16: GPIO 23

3. Button Power-off:
    * PIN 30: Ground
    * PIN 32: GPIO 12

4. LEDs
    * PIN 34: Ground
    * PIN 36: GPIO 16 (wifi)
    * PIN 38: GPIO 20 (gps)
    * PIN 40: GPIO 21 (radar)

5. USB-C (for power supply)
    * V
    * G
    * CC1: A5
    * CC2: B5

## Build Steps

1. Print [Bicycledata v2.3mf](/static/files/Bicycledata v2.3mf)
2. Remove the supports and insert 12 M4 lock nuts into the bottom and top covers.
3. Mount the Raspberry Pi to the Pi tray using 4 M2.5x6 mm screws.
4. Insert the plastic window into the bottom cover (e.g., secure it with CA glue).
5. Place the power bank with the screen facing up on top of the plastic window inside the bottom cover.
6. Prepare the buttons, USB-C connectors, and LEDs with Molex connectors (TODO: add more detailed instructions).
7. ...

### Power Supply

The box is powered by a USB-C power bank. To allow recharging without opening the enclosure, a USB-C receptacle is mounted to the housing.

An ON–OFF–ON switch is used to select between charging mode and operating mode. This ensures that only one active power connection is present at a time — or none when the switch is in the neutral (center) position.

#### Wiring

Each USB-C power connection requires four wires: V, G, CC1 (A5), and CC2 (B5). The switch must connect V to V, G to G, CC1 to CC1, and CC2 to CC2.

The common (middle) terminal of the switch is connected to a usb-c receptacle which is connected to the USB-C output/input  cable of the power bank. (important: not the output/input port)

The two ON positions are wired as follows:

**Charging mode**
Connects the power bank to the external USB-C receptacle on the housing (for charging the power bank).

**Operating mode**
Connects the power bank to the USB-C connector connected to the Raspberry Pi (to power the system).

In the center (OFF) position, the power bank is disconnected from both circuits.

**Note**

This wiring solution is functional but not ideal from an electrical design perspective. Improvements such as power-path management, proper load sharing, or protection circuitry may increase safety and reliability. Suggestions for enhancement are welcome.


**Switch schema**
```
###
# ON ---> usb-c receptacle -> charging
# OFF --> usb-c receptacle -> power bank's cable
# ON ---> usb-c connector -> raspberry pi
###
```

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
