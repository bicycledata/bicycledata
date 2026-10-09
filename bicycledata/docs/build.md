# Build Instructions

## Bill of Materials (BOM)
1. Print parts of plate 1 in PETG, plate 2&3 in TPU (336.08g incl. support) (112.02kr) [Bicycledata v4.3mf](/static/files/Bicycledata v4.3mf)
    * Box Body
    * Box Battery Stop
    * Box Top
    * Box Batteryholder
    * USB Slot Sealing
    * Lid Sealing
    * Mount Joint

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
    * Data cable + connectors (e.g. Molex or a 2x20 GPIO Female Pin header)

4. User Interface Components
    * 1x push button
    * 3x led
    * 1x push button (for OT)

5. Mechanical & Mounting Hardware
    * 4× M2.5×6 screws (for mounting the Raspberry Pi)
    * 1× 40×70×1 mm metal plate (metallplåt)
    * 4× M5×25 bolt + lock nut (rear mount and mount joint)
    * 6× M4×10 bolts + lock nuts (for the enclosure / *lock*) [link](https://www.amazon.se/Cylinderhuvudskruvar-Zinkpl%C3%A4terad-Fasteners-Cylindrical-Certified/dp/B09446MZL1/ref=sr_1_3?crid=2YMGE7AE67AT&dib=eyJ2IjoiMSJ9.elDdXwmNjtOsCUoqT0DnAT1FkysZOxggMbxHYPMo64oqTNi6N4xkq6KkJZyZrpgyGzLy6vMwyF__uHmvk0rz9G5S9hxxMaoErbv4socIZucftnMkdhfBdIzJ0mtsIndXvBGom1QPUMuUGzE-9Pt4yEcEFrdSgLLy9s1PIWAqsRCMgM-1nRvNHGphLJwkxffvF7amRyPBP8T4M37bfNdIT0I6OpfJ1JS_rXIKXsIc-h8eSl5XvTJ7bjFyBKW35ywttgO9XBZkOYVXCQfw6Stbn5K7LJHnSAsWd2Wo_FWvGbY.yVHheR_4ZdCm-XGuWqlWZP7afv_R3SczEzjlB81FeU4&dib_tag=se&keywords=M4x10%2Bhex&qid=1768824131&sprefix=m4x10%2Bhex%2Caps%2C122&sr=8-3&th=1)
    * 2× M4×12 bolts + lock nuts (for the gps metal plate) [link](https://www.amazon.se/Cylinderhuvudskruvar-Zinkpl%C3%A4terad-Fasteners-Cylindrical-Certified/dp/B09445JWSC?crid=2YMGE7AE67AT&dib=eyJ2IjoiMSJ9.elDdXwmNjtOsCUoqT0DnAT1FkysZOxggMbxHYPMo64oqTNi6N4xkq6KkJZyZrpgyGzLy6vMwyF__uHmvk0rz9G5S9hxxMaoErbv4socIZucftnMkdhfBdIzJ0mtsIndXvBGom1QPUMuUGzE-9Pt4yEcEFrdSgLLy9s1PIWAqsRCMgM-1nRvNHGphLJwkxffvF7amRyPBP8T4M37bfNdIT0I6OpfJ1JS_rXIKXsIc-h8eSl5XvTJ7bjFyBKW35ywttgO9XBZkOYVXCQfw6Stbn5K7LJHnSAsWd2Wo_FWvGbY.yVHheR_4ZdCm-XGuWqlWZP7afv_R3SczEzjlB81FeU4&dib_tag=se&keywords=M4x10%2Bhex&qid=1768824131&sprefix=m4x10%2Bhex%2Caps%2C122&sr=8-3&th=1)
    * 1× Garmin SEAT RAIL MOUNT KIT [price: 459kr](https://www.garmin.com/sv-SE/p/874032/)

## Pin Schema

1. LiDAR
    * PIN 04: 5v
    * PIN 06: Ground
    * PIN 08: GPIO 14: UART0 TX
    * PIN 10: GPIO 15: UART0 RX

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

## Build Steps

1. Print [Bicycledata v4.3mf](/static/files/Bicycledata v4.3mf)
2. Remove the supports from the printed models.
3. Insert the lock nuts into the inside of the top cover. You may use superglue on the sides of the lock nuts to keep them in place when assembling and disassembling the box, but be careful so that the threads do not get covered in glue.
4. Mount the Raspberry Pi to the Pi tray using 4 M2.5x6 mm screws.
5. Place the power bank in the battery holder and insert the battery stop into the battery holder. The battery should be placed so that its cable end stick through the opening on the opposite side of where the battery stop is.
6. Prepare the buttons, USB-C connectors, and LEDs with Molex connectors. Follow the Pin schema so that it fits the raspberry Pi 5 GPIO.
    6.1 Alternatively solder the electronics onto a GPIO female header instead of using molex [link](https://www.amazon.se/2-54mm-Female-Headers-Connector-Raspberry/dp/B07YSFPSL6?crid=4PDVDUGKJIVT&dib=eyJ2IjoiMSJ9.p4CV8gmrRLtouhwmQgBcEWB_DLpzcc5gOMHTBi57b6E67nrWTgE1s3nK5IRoXVEcZ5qx4sVuqWHLw0J1KAfWWbx-hKU7HbsZTZz1mBUkZ0fvf2o1m57phoDAw4Oj9IsPbn9ehgqaOBjTJTAPgmhl2PJaLiMRv4IKh9dwUl5O8Hx6VFf_DBu05CSOd7XVSchWGtYF7vIYPKyqfchSuHSXDWC21X6aWFYQKJuyPn7ZaQihPElrjtpc51es0yjpOaBh7O4a8Wq8_TvjzL6X1CpfkW92I8fQrwKfzuj14SYksuk.lfOak1xaEKzV70lH42ZTFUVKOyZO-7svO0TVyybxGYs&dib_tag=se&keywords=raspberry+pi+5+gpio+female+header&qid=1791537397&sprefix=raspberry+pi+5+gpio+female+header%2Caps%2C115&sr=8-5)
7. Attach the electronics to the different box parts where they fit. The USB for the power bank is designed to be on the same face of the box body as the power on-of button and lidar.
8. Assemble, in order, the top cover, lid sealing, body and battery holder. Insert 6 M4 lock nuts into the body and top cover.
9. Attach the mount joint to the top cover and then the seat rail mount kit for the seat and Varia.

### Power Supply

The box is powered by a USB-C power bank. The power bank can be recharged through the same cable which is used to power the box.

Connecting the power bank to the box activates the box.

Press the Power-off button to deactivate the box. This initiates an upload procedure on the box so that the latest data is uploaded. The LEDs will blink during this procedure. Once the LEDs on the box are turned off, the power bank may be disconnected.

# Installation Guide

* [Installation Guide](/docs/installation)
