# Overview #
This program allows turning any GSM phone supporting python and bluetooth into a GPS car antitheft. Upon receiving properly formatted SMS, phone replies with an SMS containing its GPS position and/or uploading position to a web server. Program can work in "one reply" and "tracking" mode; in the second case, upon receving the triggering SMS is starts sending location-SMSs (or uploading data)at user-defined time intervals, to allow real time tracking.

No subscription to online service required, just a cellphone subscription is required.
Variant with SMS sending can be useful in case no PHP-supporting server is available.

Written in Pys60, tested on Nokia 6600/6680.

# Details #

## Alternatives ##
There are several programs around capable of tracking a phone via GPS, but looks like all of them require "free subscription" to some services, or they only allow tracking through GoogleMaps, or just export KML files to be manually loaded into GoogleEarth.
Boring.

I have a better idea: I publish the source of a PHP script which anyone can store on any server he likes, possibly a free hosting service (which must support PHP, such as http://www.altervista.org ).


## How it works ##
This script receives position data from a program installed on your phone, which can be:
[LCCarTrack](http://code.google.com/p/lc-cartrack/source/browse/trunk/lc-cartrack/LcCarTrack.py) or [Trakkcor](http://www.trakkcor.ch/development.html)

The first is written by me, in python, and it's currently under development. First version sent position by SMS directly to the phone. New version (currently UNstable) sends data over GPRS; being it a matter of a few hundreds of byte, each upload should cost much less than 1 cent (with my plan I pay 6 euro/MB, i.e. 0.000006 euro/byte , or 0.0006 euro per upload!).
The biggest issue with my program is that pys60 does not support socket timeout, so in case of missing network the program locks up!

The second program is an opensource j2me midlet: just like my program it allows sending data to any webserver (in my program you have to manually edit the source, in Trakkcor you just edit an option). The main advantage is that (I guess) java is more robust in case of missing network, so it shouldn’t lock up.

I think my final choice will be to "couple" trakkcor to LCCartrack, getting it called by LCCarTrack every time an upload is needed.

In the meantime, you can use Trakkcor alone to track your mobile: once you authorize it to connect to gprs, it does not ask anymore, so you can start autoupload ("Live tracker") and put the phone on the car (or whatelse) you want to track.

## Try it: See your current position on a web page or in GoogleEarth! ##

You can try it with these parameters:

URL: http://jumpjack.altervista.org/lccartrack/upload_trakkcor.php

NMEA message type: $GPGGA

HTTP method: GET



Your upload will be stored into two files:

http://jumpjack.altervista.org/lccartrack/trakkcor.txt  (history)

http://jumpjack.altervista.org/lccartrack/trakkcor.kml (current position)



You can add the second address to GoogleEarth (menu ADD->Network Link) and set your favourite refresh: this will result in your position being continuously updated as you move. :)

Don't have a GPS receiver right now? Manually send a fake position and chek it on GoogleEarth, just by opening this url (specify your own coordinates, LAT and LON):
http://jumpjack.altervista.org/lccartrack/upload.php?pos=42.0,12.0

Then check your position on http://jumpjack.altervista.org/lccartrack/lccartrack.txt and (in GoogleEarth) http://jumpjack.altervista.org/lccartrack/lccartrack.kml

## GoogleEarth on phone? ##
But not all people has a notebook PC, so here it is another idea: use [MGMaps](http://www.mgmaps.com)to track the phone on another phone; this program allows displaying position on a map without downloading maps from network, but rather using cached maps, which you can for example produce using Microsoft MapCrunch, to obtain maps even from scanned images!
After installing MGMaps, open Application Manager of phone, select MGMaps, and grant permission to allow file system reading: this will prevent MGMaps from asking you for permission every time it loads map from phone.
Then, launch MGMaps, and choose Services->View KML : insert the above address for KML file. This will result in MGMaps loading position from network and displaying it on a map on the screen. Unfortunately there is no auto-update option (AFAIK) at this moment, so you have to manually refresh the waypoint. But fortunately an SDK for MGMaps exists (http://www.nutiteq.com/ ), which should allow writing own midlets which just show position on a map (without all other MGMaps options) and implements autorefresh.
