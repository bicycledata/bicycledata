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
    * 1x microSD card (32GB) [price: 149kr(https://www.electrokit.com/minneskort-microsd-a2-class-32gb-raspberry-pi)
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
    * 12× M4×10 bolts + lock nuts (for the enclosure / *lock*) [link: https://www.amazon.se/Cylinderhuvudskruvar-Zinkpl%C3%A4terad-Fasteners-Cylindrical-Certified/dp/B09446MZL1/ref=sr_1_3?crid=2YMGE7AE67AT&dib=eyJ2IjoiMSJ9.elDdXwmNjtOsCUoqT0DnAT1FkysZOxggMbxHYPMo64oqTNi6N4xkq6KkJZyZrpgyGzLy6vMwyF__uHmvk0rz9G5S9hxxMaoErbv4socIZucftnMkdhfBdIzJ0mtsIndXvBGom1QPUMuUGzE-9Pt4yEcEFrdSgLLy9s1PIWAqsRCMgM-1nRvNHGphLJwkxffvF7amRyPBP8T4M37bfNdIT0I6OpfJ1JS_rXIKXsIc-h8eSl5XvTJ7bjFyBKW35ywttgO9XBZkOYVXCQfw6Stbn5K7LJHnSAsWd2Wo_FWvGbY.yVHheR_4ZdCm-XGuWqlWZP7afv_R3SczEzjlB81FeU4&dib_tag=se&keywords=M4x10%2Bhex&qid=1768824131&sprefix=m4x10%2Bhex%2Caps%2C122&sr=8-3&th=1]
    * 1× Garmin SEAT RAIL MOUNT KIT [price: 459kr] [link: https://www.garmin.com/sv-SE/p/874032/]

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
    * PIN 14: Ground
    * PIN 16: GPIO 23

3. Button Power-off:
    * PIN 30: Ground
    * PIN 32: GPIO 12

4. LEDs
    * PIN 34: Ground
    * PIN 36: GPIO 16
    * PIN 38: GPIO 20
    * PIN 40: GPIO 21
