# Introduction #
By mean of SMSs received by a phone running LC-CarTrack, you can track that phone over a map. Currently there is no program available which can display on a map the received point, but it should be possible to write an additional program which, upon receiving the SMS, creates a POI file which is then loaded by a GPS mapping program
Such a program could perhaps be [J2meMap](http://j2memap.landspurg.net/) or [MGMaps](http://www.mgmaps.com/) or [Tracker.py](http://code.google.com/p/tracker-py/).

# GoogleEarth #
Realtime tracking in GoogleEarth is already working.
You must edit the source to [the webserver](specify.md) where to [upload](upload.md) data to, then you must [configure](configure.md) GoogleEarth to receive data from the program.


# [J2meMap](http://j2memap.landspurg.net/) #
Not yet tested




# [MGMaps](http://www.mgmaps.com/) #
If the additional program creates a proper .KML file, than this file can be IMPORTED from SERVICES menu, thus resulting in displaying on the map the position received by SMS.
On version 1.41.03, you'll use:
menu - 3.services - 6.viewKML -> Open File
Process must be manually repeated any time you want the position to be updated, but it should be possible to programmatically simulate needed keys (once the KML path has been set):
left-soft-key, 3, 6, OK, DOWN, OK, left-soft-key, OK, DOWN, OK, LEFT, LEFT




# [Tracker.py](http://code.google.com/p/tracker-py/) #
Not yet tested