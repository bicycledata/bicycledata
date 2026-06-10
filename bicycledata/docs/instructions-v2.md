<!--

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
-->

<h1 id="getting-started">Getting started</h1>

  <p>
    These instructions are intended for participants in the so-called
    "Citizen Scientist" data collection in the
    <a href="https://www.vti.se/en/archives/projects/ComCy">ComCy</a>-project.
    If you are interested in participating, you can find out more
    <a href="https://www.vti.se/en/archives/projects/ComCy/comcy/contribute-as-test-participant">here</a>.
  </p>

  <p>
    If you use the old version of the logger, please follow the
    <a href="/docs/instructions">legacy instructions</a>.
  </p>

  <p>
    <a href="#quick-guide-logging">Jump to Quick Guide</a>
  </p>



<h2 id="toc">Table of Contents</h2>
<table>
  <tr>
    <th align="left">Getting Started</th>
    <th align="left">Data</th>
  </tr>

  <tr>
    <td valign="top">
      <ul>
        <li><a href="#registration">Registration</a></li>
        <li><a href="#unboxing">Unboxing</a></li>
        <li><a href="#how-do-i-mount-the-logger">Mounting Logger on Bike</a></li>
        <li><a href="#how-do-i-configure-my-hotspot">Hotspot Configuration</a></li>
        <li><a href="#how-do-i-operate-the-logger">Operation of Logger</a></li>
        <li><a href="#how-do-i-charge">Charging the equipment</a></li>
      </ul>
    </td>

    <td valign="top">

      <ul>
        <li><a href="#after-each-ride">After Each Ride</a></li>
        <li><a href="#how-do-i-access-my-data">Data Access</a></li>
        <li><a href="#download-data">Data Download</a></li>
        <li><a href="#who-can-access-my-data">Data Privacy</a></li>
      </ul>
    </td>
  </tr>
</table>


<h2 id="registration">Registration</h2>

![Close-up of login information](/static/images/devices/login.jpg) 

<p>
  You can <a href="https://bicycledata.vti.se/login">register</a> via our homepage (<a href="https://bicycledata.vti.se/">https://bicycledata.vti.se/</a>), , where you'll find all relevant information.
</p>

<p>
  Sign up with your name and a valid email address. You use the same address to log in to your dashboard and to view, annotate and download your data. We handle registrations manually, so it may take a while before you receive a response.
</p>

<h2 id="unboxing">Unboxing</h2>

What you'll get from us:

<h3 id="holder">Holder</h3>

A holder for Garmin and GoPro devices to attach the logger to your seat
rails with an Allen key.

<img
  src="/static/images/devices/KatjaKircher_VTITrafficLogger-050.jpg"
  alt="Garmin seat rail mount with screws"
  width="250"
/>

<h3 id="trafficlogger">TrafficLogger</h3>

<p>
  A logging device measuring the lateral distance to passing traffic. The device you get
  can have a different colour and look slightly different, but you will find the
  buttons, sensors and LEDs that are described here.
</p>

<p>
  <b>Content</b>
</p>

<ul>
  <li>Raspberry Pi core unit</li>
  <li>Lidar sensor</li>
  <li>GPS sensor</li>
</ul>


 <table>
  <tr>
    <td align="center">
      <img src="/static/images/devices/box1_0021.jpg" style="width: 250px; max-width: 100%;" alt="Left side of device"><br>
      <strong>Left side</strong><br>
      Lidar sensor, upload button and USB-C-port to power the device on.
    </td>
    <td align="center">
      <img src="/static/images/devices/box1_0022.jpg" style="width: 250px; max-width: 100%;" alt="Front side of device"><br>
      <strong>Front</strong><br>
      USB-C port for the event button.
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="/static/images/devices/box1_0026.jpg" style="width: 250px; max-width: 100%;" alt="Rear side of device"><br>
      <strong>Rear</strong><br>
      Radar attachment point, opening for power bank.
    </td>
    <td align="center">
      <img src="/static/images/devices/box1_0020.jpg" style="width: 250px; max-width: 100%;" alt="Top side of device"><br>
      <strong>Top side</strong><br>
      Top of device with status LEDs.
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="/static/images/devices/box1_0029.jpg" style="width: 250px; max-width: 100%;" alt="Power on"><br>
      <strong>USB-C-cable from power bank plugged in</strong><br>
      The cable from the power bank is plugged into the device to power the device.
    </td>
    <td align="center">
      <img src="/static/images/devices/box1_0030.jpg" style="width: 250px; max-width: 100%;" alt="Box with event button"><br>
      <strong>Box with event button</strong><br>
      The logger with event button attached.
    </td>
  </tr>

</table>

<h3 id="garmin-varia">Garmin Varia radar</h3>

<p>
  You can use Garmin Varia devices in the 3-, 5- or 7-series. You'll get a Varia 315 from us. If you want to use your own Garmin Varia, please let us know.
</p>

<p>
  The radar is attached to the rear of the logger. It connects to the TrafficLogger via Bluetooth and it registers vehicles
  approaching from behind, logging their distance and relative speed from
  a range of about 140 m.
</p>

<table>
  <tr>
    <td align="center">
      <img src="/static/images/devices/KatjaKircherVTI_TrafficLogger-045.jpg" style="width: 250px; max-width: 100%;" alt="Garmin Varia 716"><br>
      <strong>Garmin Varia 716</strong><br>
      Press the big button on the side for 2 s to turn the device on or off.
      Charge with a USB-C cable (included).
    </td>
    <td align="center">
      <img src="/static/images/devices/KatjaKircher_Box_v10_05.jpg" style="width: 250px; max-width: 100%;" alt="Garmin Varia 315"><br>
      <strong>Garmin Varia 315</strong><br>
      Press the button on top for 2 s to turn the device on or off.
      Charge with a micro-USB cable (included).
    </td>
  </tr>
</table>



<h3 id="button">Button</h3>

<p>
  The button is placed on the handlebars and attached to the front side of the logger via USB-C. You mark passing events by pressing the button, for instructions see <a href="/docs/mark-overtaking-events">here</a>.
</p>

<table>
  <tr>
    <td align="center">
      <img src="/static/images/devices/KatjaKircherVTI_TrafficLogger-043.jpg" style="width: 250px; max-width: 100%;" alt="Event button with cable"><br>
      <strong>The button to mark passing events</strong><br>
      You attach the button to the handlebars with the velcro-strip and connect it to the logger via USB-C.
    </td>
    <td align="center">
      <img src="/static/images/devices/KatjaKircherVTI_TrafficLogger-044.jpg" style="width: 250px; max-width: 100%;" alt="Close-up of event button"><br>
      <strong>Close-up of button</strong><br>
      Close-up of the event button you use to mark overtakes.
    </td>
  </tr>
</table>



<h2 id="how-do-i-mount-the-logger"> How do I mount the logger?</h2>

<ol>
  <li>Mount the clamp to the seat rails using an Allen key. You may want to place some protection underneath to avoid scratching the rails. It may take some creativity to get a good placement, for example, some saddles are designed such that it works better to mount the clamp upside down.</li>
  <li>Mount the logger to the clamp. Do not overtighten. Make sure the logger is not in the way for your legs.</li>
  <li>Attach the event button to the handlebars in a location that is easy to reach, but where you won't press it accidentally.</li>
  <li>Route the cable along the frame. Make sure that you can still turn the handlebars.</li>
  <li>Connect the USB cable to the front USB-port of the logger.</li>
  <li>Attach the Garmin Varia radar to the logger.</li>
</ol>


<table>
  <tr>
    <td align="center">
      <img src="/static/images/devices/box1_0002.jpg" style="width: 250px; max-width: 100%;" alt="Device attached to seat rails"><br>
      <strong>Mount on seat rails</strong><br>
      Mount the logger on the seat rails choosing a hole that does not interfere with your legs and keeps the logger as balanced as possible.
    </td>
    <td align="center">
      <img src="/static/images/devices/KatjaKircher_VTITrafficLogger_010.jpg" style="width: 250px; max-width: 100%;" alt="Hands operate event button"><br>
      <strong>Attach event button</strong><br>
      Make sure to have the button within easy reach, but "out of the way" for accidental presses.
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="/static/images/devices/box1_0007.jpg" style="width: 250px; max-width: 100%;" alt="LED status indicators"><br>
      <strong>LEDs for status indication</strong><br>
      Status indicators for radar (RA) - lit when connected, flashing when searching;<br> WiFi (WF) - lit when connected;<br> and GPS fix (GP) - position fix when lit, flashing when searching.
    </td>
    <td align="center">
      <img src="/static/images/devices/box1_0017.jpg" style="width: 250px; max-width: 100%;" alt="Power bank holder"><br>
      <strong>Power bank holder</strong><br>
      If you want to take out the power bank, carefully remove the splint holding it in place and apply pressure from the front side. Do not pull on the cable.
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="/static/images/devices/box1_0005.jpg" style="width: 250px; max-width: 100%;" alt="Event button attachment point"><br>
      <strong>USB-contact for event button</strong><br>
      Attach the button to the logger via USB-C. Make sure to use the USB-contact on the front side of the logger.
    </td>
    <td align="center">
      <img src="/static/images/devices/box4_0003.jpg" style="width: 250px; max-width: 100%;" alt="Box with USB-C-cable in charging port"><br>
      <strong>Charge the logger</strong><br>
      Charge the box by inserting the USB-C-contact of the power bank into a USB wall charger, alternatively, remove the power bank and insert a USB-C-charger into the contact on the side. When fully charged, the logger will work for around 8h. After around 5h of charging, the power bank is fully charged. [correct picture to come]
    </td>
  </tr>
</table>


<h2 id="how-do-i-configure-my-hotspot">How do I configure my hotspot?</h2>


<table>
  <tr>
    <td align="center" style="width: 170px; vertical-align: top;">
      <img
        src="/static/images/devices/MobileHotspot.jpg"
        style="width: 200px; max-width: 100%;"
        alt="Android phone screenshot with hotspot settings"
      >
    </td>

    <td style="vertical-align: top; max-width: 420px;">
      <b>Android:</b> On your phone, configure your hotspot such that it is called <code>bicycledata</code><br>
      Also the password should be set to <code>bicycledata</code><br>
      Use 2.4&nbsp;GHz.<br><br>

      <b>iPhone:</b> Rename your phone to <code>bicycledata</code> via Settings > General > About > Name; tap <code>x</code> then enter the new name.<br>
      In Swedish: Inställningar > Allmänt > Om > Namn<br><br>
      Under "hotspot"/"internetdelning" set the password to <code>bicycledata</code><br>
      Under "hotspot"/"internetdelning" set "allow others to connect" to yes.<br>
      For more detailed instructions for iPhone check <a href="/docs/iphone-hotspot">here</a>.<br>
    </td>
  </tr>
</table>



<h2 id="how-do-i-operate-the-logger">How do I operate the logger?</h2>

<p>
  <div class="note">
    <b>Important:</b> Turn the devices on and off in the specified order.
  </div>
</p>

<h3 id="startup">Start</h3>

<ol>
  <li>Activate your hotspot (<code>bicycledata</code>).</li>

  <li>
    Start the Garmin Varia (press the ON/OFF button for 2 seconds).
    <ul>
      <li>Varia 315: The LED will flash blue.</li>
      <li>Varia 716: The LED will turn green, then red. 
      <br><em>(This can differ between devices.)</em></li>
    </ul>
  </li>

  <li>
    Start the logger by inserting the USB-cable into the port on the left side of the device. It takes one or two minutes to start up. You will see the LEDs flash after a while.
    <ul>
      <li><strong>WiFi:</strong> <code>WF</code> LED indicates connection to hotspot.</li>
      <li><strong>WiFi:</strong> When <code>WF</code> LED turns off, the hotspot can be shut off.</li>
      <li><strong>Radar:</strong> <code>RA</code> LED indicates connection to Garmin Varia.</li>
      <li><strong>GPS:</strong> <code>GP</code> LED indicates a GPS fix (this can take a while, 4–7 minutes is not unusual).</li>
    </ul>
  </li>
</ol>

<p>
  Now you're ready to go riding. Please read <a href="/docs/mark-overtaking-events">here</a> how to mark passing events with the button.
</p>

<h3 id="data-upload">Data upload and shutting down</h3>

<ol>
  <li>Activate your hotspot again (<code>bicycledata</code>).</li>
  <li>Press the upload button for 5 seconds (until the LEDs start flashing).
    <ul style="margin-bottom: 0;">
      <li>WiFi-LED lit: Connection established (data upload starts).</li>
      <li>LEDS are flashing (data are being uploaded).</li>
      <li>Wait until LEDs turn off.</li>
    </ul>
  </li>
  <li>Turn off the Garmin Varia (press the button for 2 seconds)</li>
  <li>Turn off the logger by carefully removing the power bank cable from the port.</li>
  <li>If necessary, charge the logger. If you leave the cable plugged into the logger, the battery will drain.</li>
</ol>

<p>
  <b>Note:</b> Sometimes the ride does not upload fully. You can either start the equipment again and then press the upload button (with the hotspot on throughout, no need to start the radar), or you can wait until you ride the next time. The data will only be deleted from the logger once uploaded to the server.
</p>

<h2 id="how-do-i-charge">How do I charge the equipment?</h2>


<h3 id="charge-logger">Logger</h3>

<ul>
  <li>One charge lasts for around 8-9 hours of riding.</li>
  <li>Charge the logger via USB-C.</li>
  <li>The power bank has a display indicating the charging level. To see it, the power bank has to be removed from the logger.</li>
</ul>

You can charge the power bank of the logger in two ways:
<ol>
  <li>Plug the cable that you use to start the logger into a USB-C-charger.</li>
  <li>Plug a USB-C-cable into the side of the power bank (you'll have to take the power bank out).</li>
</ol>

<p>
  For the first solution, you'll either have to get the bike close to a USB-C-charger or you'll have to remove the logger from the bike. If you do the latter, it is easiest do detach the button from the logger, leaving the button on the bike, and then unscrew the middle screw in the holder instead of removing the holder from the seat rails or removing the logger from the holder (see picture).
</p>

<img
  src="/static/images/devices/KatjaKircher_Box_v10_04.jpg"
  alt="Garmin Varia 716"
  width="250"
/>

<p>
  For the second solution, carefully remove the red splint. Apply pressure through the hole in the front to press out the power bank. There can be a piece of rubber keeping the power bank in place, such that this may require some effort.
</p>

<p>
  To re-insert, make sure that the cable comes through the hole in the front. Do <b>not</b> pull on the cable. Apply pressure from the rear instead.
</p>

<h3 id="charge-garmin-varia">Garmin Varia</h3>

<ul>
  <li>One charge lasts for up to 6 hours.</li>
  <li>You take off the Varia by turning it counter-clockwise.</li>
  <li>Charge the Garmin Varia with the enclosed micro-USB cable.</li>
  <li>While charging, a LED flashes green. When fully charged, the LED remains on.</li>
</ul>

<h1 id="my-data">My data</h1>

After uploading the logged data as described above, you can annotate and download your data via the dashboard.

<h2 id="after-each-ride">After each ride</h2>

<p><strong>Log in on your dashboard after each ride to:</strong></p>

<ul>
  <li>
    Mark whether the data originate from a real ride or if you only tested the
    logger and “played” with it (in this case click <code>hide</code>).
  </li>

  <li>
    Mark whether you rode on your own (write <code>0</code>) or in the company
    of others (indicate how many people you rode with).
  </li>

  <li>
    Indicate whether you marked overtakes or also oncoming traffic by checking the appropriate boxes.
  </li>

  <li>
    Comment on certain events or other things we should know 
    (traffic situations, weather, logger issues, or
    anything else you find relevant).
  </li>
</ul>

<p>
  You do not have to fill in the battery fields.
</p>

<h2 id="how-do-i-access-my-data">How do I access my data?</h2>

<p>
  Under "Sessions" all occasions when you turned the logger on are listed. You can hide occasions that were not a proper ride. Click on a ride to see its contents.
</p>

<img
  src="/static/images/graphics/Dashboard_Sessions_English.jpg"
  alt="A screenshot of the dashboard as of January 2026"
  width="500"
/>

<p>
  Here you can see some meta-information about your ride and have the possibility to make annotations (image slightly outdated).
</p>

<img
  src="/static/images/graphics/Dashboard_SingleRide_English.jpg"
  alt="A screenshot of the dashboard as of January 2026"
  width="400"
/>

<h2 id="download-data">Download data</h2>

<p>
  You can download raw data files. In the future, you will be able to also download processed events.
</p>

<!--
<p>
  Each sensor generates a file that contains data from your entire ride (raw data). This information forms the basis of our analyses. In addition, there is a data file containing the overtake events found in the material. For each event it contains the location, the lateral distance, the vehicle speed when overtaking and other information. If you also marked oncoming vehicles, you will find an additional file for those passes, but they do not contain vehicle speed.
</p>
-->

<h2 id="who-can-access-my-data">Who can access my data?</h2>

<p>
  Only you, via your dashboard, and the researchers at VTI who participate in the project can access your raw data. The processed events can eventually be published on openly accessible maps and in other publications, like scientific articles, research reports and on social media. They will be shared with other researchers within the <a href="https://www.vti.se/en/archives/projects/ComCy">ComCy-project</a>. Processed means that single overtakes and oncoming passes are identifiable via their location and time, but without cyclist ID.
</p>

<p>
  The data could for example be displayed as in the excerpt of the map below, where a mouseover shows the speed and lateral clearance of the overtaking vehicle.
</p>

<img
  src="/static/images/graphics/otMap.png"
  alt="A screenshot of a map with overtaking events marked by colour (latera clearance) and size (vehicle speed)"
  width="400"
/>


<h2 id="what-happens-later">What happens when I’m done with the data collection?</h2>

<p>
  Also after returning the logger, you’ll be able to log in, see and download your data as long as the server is running and we have the possibility to maintain it. We cannot give any guarantees about the timeframe, however.
</p>

<h1 id="quick-guide-logging">Quick Guide - Logging</h1>

<ol>
  <li>Make sure event button is attached</li>
  <li>Activate hotspot</li>
  <li>Turn radar on</li>
  <li>Turn logger on (plug in cable from power bank)</li>
  <li>Wait for radar and GPS LED to turn on</li>
  <li>Optional: Deactivate hotspot</li>
</ol>
<p>
  Ride and mark passing events
</p>
<ol>
  <li>Activate hotspot</li>
  <li>Press upload button until all LEDs flash</li>
  <li>Turn off radar</li>
  <li>When LEDs are off, detach power bank cable from logger</li>
  <li>Charge equipment if necessary</li>
</ol>


