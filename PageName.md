# Introduction #

LC Car Track allows any gsm cellphone supporting Python (e.g. Nokia [Series60](http://www.forum.nokia.com/devices/matrix_s60_1.html) with Pys60) to send, upon SMS request, SMSs containing position read from external bluetooth GPS receiver.


# Details #
Upon receiving an SMS, the program checks it for keywords; if it finds one of them, it replies with one single SMS or starts sending SMSs at defined time intervals until a "STOP" SMS is received: this is known as "tracking mode", and allows realtime tracking of the phone, or of a stolen car when the phone is hidden in.
It has been chosen not to use GPRS network to send data as on some phone user authorization is required to start connection, thus preventing program from being used as a standalone antitheft; SMS can instead be sent without asking for any permission.
This causes costs to be greater than adopting a GPRS communication method, but in consideration of money this program should allow to save (cost of a phone with built-in gps, or cost of a car), it shouldn't be an issue.

# Possible improvements #
As pys60 does allow simulating keystrokes sent to other applications, maybe it could be possibile to start a GPRS connection by simulating the user pressing the YES key; but this should also require to be able to detect if such a connection is already active, to be able to know if the confirmation dialog is being shown.

A further improvement could be "parking mode": if you have to park your car for a long time, you set up the program to continuously check for the parking location GPS position: as soon as the car position changes w.r.t. stored position, a theft is detected and an SMS is sent (or tracking mode is activated)

A strongly needed improvement is an additional program to be used on **another** phone which allows tracking stolen phone position without the need for a portable computer. To accomplish this, a map visualization algorithm must be implemented.

# Porting to other platforms #

Although this program is designed to work with external GPS sets, it should be possible to make it work on cellphones equipped with built-in GPS module such as Nokia [N95](N95.md) or Apple [iPhone](iPhone.md).

To port program to N95 an additional python module is required, named LocationRequestor:

https://www.iyouit.eu/portal/software.aspx

Please see dedicated page for porting to [N95](N95.md).

To port program to iPhone you'll need to "hack" it in such a way it can be programmed in Python:

http://www.saurik.com/id/5

Please see dedicated page for porting to [iPhone](iPhone.md).