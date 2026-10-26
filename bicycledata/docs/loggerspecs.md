<h1 id="SpecAndUse">TrafficLogger - Specs and use cases</h1>

<h2 id="Spec">Specifications</h2>
<ul>
  <li><a href="#logger">The logger</a></li>
  <li><a href="#techspecs">Technical specifications</a></li>
  <li><a href="#button">The event button</a></li>
  <li><a href="#data">Data</a></li>
  <li><a href="#modularity">Modularity and adaptability</a></li>
  <li><a href="#usecases">Use cases</a></li>
</ul>

<h2 id="Materials">Available equipment</h2>
<ul>
  <li><a href="equip">Loggers etc.</li>
</ul>

<h2 id="projects">Use in projects</h2>
<ul>
  <li><a href="#commission">Commission a project</a></li>
  <li><a href="#collaborate">Collaborate</a></li>
  <li><a href="#rental">Rental of logger(s)</a></li>
</ul>

<h2 id="Spec">Specifications</h2>

<h3 id="logger">The logger</h3>

<p>
    The logger is attached to the seat rails of a bicycle (or similar, see below). Via pressing an event button, the user marks events to help locating them in the time series data. One such use case are overtaking and oncoming passes (see the ComCy project). A range of other use cases is thinkable (see below).
</p>

<img src="/static/images/devices/box1_0002.jpg" style="width: 450px; max-width: 100%;" alt="Device attached to seat rails"><br>
<strong>A logger mounted on the seat rails of a bike</strong><br>

<p>
  The logger is compatible with most bikes. A detailed description of the current sensors and functionality can be found <a href="/docs/instructions-v2.md">here</a>.
</p>

<h3 id="techspecs">Technical specifications</h3>

<ul>
  <li>Width: 9.5 cm</li>
  <li>Length: 18 cm including the Garmin Varia 315</li>
  <li>Height: 10 cm (including battery pack), 7.5 cm (excluding battery pack); always excluding the mount</li>
  <li>Weight: 820 g in total (logger with holder: 550 g; battery pack: 220 g; Garmin Varia 315: 50 g)
</ul>

<p>
  The battery pack lasts for ca. 9 h of operation (the Garmin Varia 315 lasts 5-6 h).
</p>

<h3 id="button">The event button</h3>

<p>
  We deploy an event button for the detection of overtaking and oncoming passes, as we assess this to be the most reliable method to obtain clean data. We operate the logger without camera, partially for GDPR reasons and partially as this would inflate the amount of data enormously. Also, video review does not scale well. Overall, we would say that the button solution works very well with trained users and reasonably well with untrained users.
</p>
<p>
  For a detailed description of how the event button should be used to mark overtaking and oncoming passes such that they are detectable by our algorithm, check <a href="/docs/mark-overtaking-events">here</a>.
</p>

<h3 id="data">Data</h3>

<p>
  Data are logged either event-based or as time series, generating one file per sensor per session with a common timestamp. Currently we log:
</p>

<ul>
  <li><strong>button:</strong> event button presses, event-based (timestamp and duration)</li>
  <li><strong>lidar:</strong> distance to nearest object, max ca. 12 m; ca. 35 Hz (adjustable)</li>
  <li><strong>radar:</strong> distance to vehicles approaching from behind and their relative speed, max ca. 140 m; 8 Hz (fixed)</li>
  <li><strong>GPS:</strong> geoposition and derivatives; 1 Hz (fixed)</li>
</ul>

<p>
By default, the data are uploaded to a server at VTI via a WiFi connection (e. g. hotspot). This can be adjusted if required.
</p>

<p>
By default, VTI researchers (currently three people) have full access to the data. Each user has full access to their data. Currently, a logger is manually assigned to a user. Other people cannot access the data.
</p>

<h3 id="modularity">Modularity and adaptability</h3>

<p>
  The loggers are built and programmed in a modular way, such that sensors easily can be added or removed. Adaptations can also be made to the case and the mount, such that the logger can be used on other transport modes or in completely different settings.
</p>


<h3 id="usecases">Use cases</h3>

<p>
  The use case for which the logger was built originally is overtaking of cyclists with motor vehicles (see e.g. the <a href="https://www.vti.se/en/archives/projects/ComCy">ComCy</a>-project). Other use cases are thinkable. They may require physical modifications or additional sensors. Below is a non-exhaustive list of examples, with additional sensors in parentheses.
</p>

<ul>
  <li>glare from cars or other sources (camera, proof-of-concept tested)</li>
  <li>rider comfort depending on surface or other features (accelerometer, proof-of-concept tested)</li>
  <li>ambient noise (not tested)</li>
  <li>air quality (not tested)</li>
</ul>

<h2 id="Materials">Available equipment</h2>

<h3 id="equip">Loggers etc.</h3>

<p>
  Currently we have the following equipment which can be deployed by us or rented out:
</p>

<p>
  7 loggers including
</p>
<ul>
  <li>Garmin Varia 315 radar</li>
  <li>lidar</li>
  <li>GPS</li>
  <li>event button</li>
</ul>

<p>
  One simple accelerometer is mounted in one logger.
</p>


<h2 id="projects">Use in projects</h2>

<p>
  The loggers can be operated by trained test leaders or sent out to "Citizen Scientists", that is, interested lay people with some technical understanding. Both approaches have been tested with satisfying results.
</p>

<h3 id="commission">Commission a project</h3>

<p>
  We perform a complete study based on your research question.
</p>

<h3 id="collaborate">Collaborate</h3>

<p>
  Collaborative projects where we perform any part of the following either alone or in collaboration:
</p>

<ul>
  <li>further logger development</li>
  <li>study planning and testing</li>
  <li>data collection</li>
  <li>data processing</li>
  <li>data analysis</li>
  <li>reporting</li>
</ul>

<h3 id="rental">Rental of logger(s)</h3>

<p>
  You can rent loggers from us and perform your own study. We would support as needed. Please get in touch.
</p>

