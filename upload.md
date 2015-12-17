LCCarTrack sends data to a [webserver](webserver.md) by means of an HTTP request to a PHP page.
The PHP pages reads the data in the URL and it stores them into a KML file which can be read by [GoogleEarth](GoogleEarth.md) or compatible programs to show current position.

Upload is performed by means of urllip.urlopen().

The URl for PHP page is as follows (subject to change as program evolves):
http://jumpjack.altervista.org/lccartrack/upload.php?pos=41.997748,12.616809&name=Car&speed=10&time=2008-10-22_10:20:00

pos: LONGITUDE followed by LATITUDE
name: main string appearing in GoogleEarth map
speed: added to the name displayed by GoogleEarth, followed by "Km/h"
time: timestamp of the upload

The timestamps of the upload time and of GPS-receiving time are added to the DESCRIPTION of the "waypoint".