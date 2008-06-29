##########################################
### LcCarTrack - satellite car antitheft 
###     Written by Luca Cassioli 2008
##########################################
## Version 1.0.0

### This program is FREEWARE.
### Commercial use is forbidden without author's permission.


### Keep the phone and a GPS receiver hidden into your car,
### continuously charging and running this python script.
### If your car gets stolen (or if you don't remember where
### you parked it...), just send an SMS to it containing:
### SEND - to receive a single SMS with latitude and longitude;
### TRACK ON - to start receiving one SMS every INTERVAL second;
### TRACK OFF - to stop tracking.

### ****** WARNNG:Using this program to track others than yourself, or things
### ****** you don't own, is forbidden in most countries and legally 
### ****** persecuted (privacy law).

import inbox
import e32
import socket
import appuifw
import messaging
import os

Recipient_number="000000"
FOLDER='e:/LcCarTrack'
FILEPATH='e:/LcCarTrack/settings.txt'

TRACKING = 0 # Disabled by default.
INTERVAL = 20 # seconds between tracking messages

def Connect():
  #return "debug"
  sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
  address,service=socket.bt_discover()    # cerca ricevitore.
  target=(address,service.values()[0]) # si collega
  sock.connect(target)# al ricevitore.
  return sock
  
def ReadPos():
      valid = 0 
      while (valid==0): # If unknown line is read from GPS, device output must be read again.
          rawdata = readline(sock) 
          if rawdata:
              msg= '(stringa non prevista)'
              data = rawdata.strip()
              talker = data[1:3]
              sentence_id = data[3:6]
              sentence_data = data[7:]             
              #Extract location data:
              location = {}
              if sentence_id == 'GGA':
                location = get_gga_location(sentence_data) 
                msg = 'LAT:' + location['lat'] + ',LON:' + location['long']
                valid = 1
              if sentence_id == 'GLL':
                location = get_gll_location(sentence_data)
                msg = 'LAT:' + location['lat'] + ',LON:' + location['long']
                valid = 1
              if sentence_id == 'RMC':
                location = get_rmc_location(sentence_data)
                msg = 'LAT:' + location['lat'] + ',LON:' + location['long']
                valid = 1                     
          else:
              print "****** dati non validi*****"
              msg= 'couldnt receive GPS data'        
      return msg
      
      
def SendMess(n,m):
  #print "Invio messaggio " + m + " a " + n
  messaging.sms_send(n,m) # DEBUG

def read_sms(id): #DEBUG
#def read_sms():
    global Recipient_number
    global TRACKING
    ##############################à
    #sms_text="TRACK ON" # DEBUG*********
    ##############################à
    e32.ao_sleep(0.1)
    i=inbox.Inbox() #DEBUG
    sms_text=i.content(id) #DEBUG
    appuifw.note(u"Messaggio da elaborare: " + sms_text, "info")

    # Execute different actions depending on SMS contents:
    if sms_text[0:8] == 'TRACK ON':
      i.delete(id) # Delete just received message
      SendMess(Recipient_number,'TRACKING ACTIVATED!')
      TRACKING = 1
      while (TRACKING == 1):
        e32.ao_sleep(INTERVAL)
        msg=ReadPos()
        SendMess(Recipient_number,'TRACKING: '+msg)  
        print 'Tracker message sent.'
    if sms_text[0:9] == 'TRACK OFF':
      i.delete(id) # Delete just received message
      TRACKING = 0
      SendMess(Recipient_number, "tracking DEactivated!")
    if sms_text[0:4] == 'SEND':
      i.delete(id) # Delete just received message
      print 'Reading position....'      
      msg=ReadPos()
      print 'Sending position ' + msg + ' to ' + Recipient_number 
      SendMess(Recipient_number, msg) # Send SMS.
      print 'Position sent.'


def ReadSettings():
    global Recipient_number
    global FILEPATH
    try:
        f=open(FILEPATH,'rt')  # Open for reading
        print "file aperto"
        try:
            content = f.read()
            print "contenuto letto"
            parameters=eval(content) # Store values
            print "valori presi"
            f.close()
            Recipient_number = parameters.get('recipient','')  # read values
            #print Recipient_number
        except:
            print 'Couldnt read file - err 001'
    except:
        print 'Couldnt open file - err 002'
        
def write():
    global Recipient_number
    global FOLDER
    # Setup configuration file:
    FILEPATH=os.path.join(FOLDER,'settings.txt')
    # Create if does not exist:
    if not os.path.isdir(FOLDER):
        os.makedirs(FOLDER)
        FOLDER=os.path.join(FOLDER,'settings.txt')        
    # Store values into a dictionary:
    parameters={}
    parameters['recipient']= Recipient_number
    # Save:
    f=open(FILEPATH,'wt')
    f.write(repr(parameters))
    f.close()
    
# Format a NMEA timestamp into something friendly
def format_time(time):
	hh = time[0:2]
	mm = time[2:4]
	ss = time[4:]
	return "%s:%s:%s UTC" % (hh,mm,ss)
 
# Format a NMEA date into something friendly
def format_date(date):
	months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
	dd = date[0:2]
	mm = date[2:4]
	yy = date[4:6]
	yyyy = int(yy) + 2000
	return "%s %s %d" % (dd, months[(int(mm)-1)], yyyy)
  
# Get the location from a GGA sentence
def get_gga_location(data):
	d = data.split(',')
	ret = {}
	ret['type'] = 'GGA'
	ret['lat'] = "%s%s" % (d[1],d[2])
	ret['long'] = "%s%s" % (d[3],d[4])
	ret['time'] = format_time(d[0])
	return ret
 
# Get the location from a GLL sentence
def get_gll_location(data):
	d = data.split(',')
	ret = {}
	ret['type'] = 'GLL'
	ret['lat'] = "%s%s" % (d[0],d[1])
	ret['long'] = "%s%s" % (d[2],d[3])
	ret['time'] = format_time(d[4])
	return ret
 
# Get the location from a RMC sentence
def get_rmc_location(data):
	d = data.split(',')
	ret = {}
	ret['type'] = 'RMC'
	ret['lat'] = "%s%s" % (d[2],d[3])
	ret['long'] = "%s%s" % (d[4],d[5])
	ret['time'] = format_time(d[0])
	return ret
  
def readline(sock):
	"""Read one single line from the socket"""
	line = ""
	while 1:
		char = sock.recv(1)
		if not char: break
		line += char
		if char == "\n": break
	return line
          
ReadSettings()
sock=Connect()

print Recipient_number
print sock

print 'connecting to inbox...'
i=inbox.Inbox()  #DEBUG
# Connect messages receiving to program:   
i.bind(read_sms) #DEBUG
print 'Connected. Waiting for incoming messages...'

#print "DEBUG MODE"
#read_sms()

