##########################################
### LcCarTrack - satellite car antitheft 
###     Written by Luca Cassioli 2008
##########################################
## Version 1.1.4

# 1.1.4 - *GGA and *GLL strings no more used (contain old data?)
#         Implemented GSM_position
# 1.1.3 - Added dozens of try-catch to increase robustness...
# 1.1.2 - Added degree/minutes/seconds separators
# 1.1.1 - Fixed bug of sample FormatMessage() calls
#         overriding MSG_FORMAT settings.
#       - Added customizable decimals number.  
# 1.1.0 - Started SVN/GoogleCode configuration management
#         Customizable message formatting added. 

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

import keycapture
from appuifw import *
import inbox
import e32
import socket
import appuifw
import messaging
import os
from e32 import ao_sleep,Ao_lock
import phone_ext

import keypress
from key_codes import *

import appswitch
import urllib

import location

locationAPI=location
abort = 0


Recipient_number="000000"
FOLDER='e:/LcCarTrack'
FILEPATH='e:/LcCarTrack/settings.txt'

# Available message formats:
FMT_YOUPOSITION = 1 # Lat$Lon  , for site http://www.youposition.it 
FMT_DECIMAL = 2 # LAT=dd.dddddd, LON=dd.dddddd
FMT_60 = 3 # LAT = dd mm ss.ssss , LON = dd mm ss.ssss
FMT_CUSTOM1 = 4 # Free slot: add your conversion algorithm in FomratMessage(lat,lon,type) function
FMT_CUSTOM2 = 5 # Free slot: add your conversion algorithm in FomratMessage(lat,lon,type) function

##################################
####  Selected message format ####
MSG_FORMAT = FMT_DECIMAL      ####
MAX_DECIMALS = 6              ####
##################################
  
  
TRACKING = 0 # Disabled by default.
INTERVAL = 20 # seconds between tracking messages
MAXATTEMPTS = 1 # Max attempts in case of GPS error
MAXSTRINGATTEMPTS = 40 # Max attempts in case of not suitable string incoming from GPS
GPS_CONNECT_ERROR = "Error connecting to GPS"
GPS_RECONNECT_ERROR = "Failed attempting reconnecting to GPS"

GPS_address = '' # temporary
GlobalErr = 0


def UploadPosition():
  p = ReadPos()
  data = "<?xml version=%221.0%22 encoding=%22UTF-8%22?><kml xmlns=%22http://www.opengis.net/kml/2.2%22><Placemark><name>Prova</name><description>Descrizione</description><Point><coordinates>" + p  + ",0</coordinates></Point></Placemark></kml>"
  data=urllib.urlencode({'data':data})
  print "Starting authorizer in background..."
  e32.start_server("c:\\system\\apps\\python\\my\\authorize.py")
  print "Uploading data ..."
  try:
    response = urllib.urlopen("http://jumpjack.altervista.org/prove/testphp.php?data=" + data).read()
    print "Result: "+ response
  except Exception,e:
    print "Error uploading data! " + str(e)


def PrintOptions():
  print
  print "###########################"
  print "1 - Show position"
  print "2 - Send position"
  print "3 - Search new GPS device"  
  print "4 - Upload position"  
  print "5 - Break loop"  
  print
  print "0 - SHOW THIS MENU"
  print "###########################"

def quit():
    app.exit_key_handler = None
    script_lock.signal()
    capturer.stop()
    print "PROGRAMMA TERMINATO."
    print
    
def cb_capture(key):
    global abort
    if key==keycapture.EKey0:
      PrintOptions();
    if key==keycapture.EKey1:
      print "Current position:", ReadPos()
    if key==keycapture.EKey2:
      print "Sending message..."
      SendMess(Recipient_number, ReadPos())
    if key==keycapture.EKey3:
      try:
        sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
        address,service=socket.bt_discover()   
        print "Address:", address
      except Exception, e:
        print "Error formatting message: " + str(e)
    if key==keycapture.EKey4:
      print "Uploading position..."
      UploadPosition()
    if key==keycapture.EKey5:
      print "STOP!"
      abort = 1

        
        
def FormatMessage(lat,lon,fmt):
  global GlobalErr
  #print "converto lat:",lat, " , lon:", lon, " in formato ", fmt
  try:
    GlobalErr = 0
    LatComma=lat.find(".")
    LonComma = lon.find(".")
    la = float(lat)
    lo = float(lon)
    #print lat ,la
    #print lon, lo
    msg = "[conversion error]"
    if fmt == FMT_YOUPOSITION: # dd.dddddd$ddd.dddddd
      msg = lat[0:lat.find(".")+MAX_DECIMALS+1] +"$" + lon[0:lon.find(".")+MAX_DECIMALS+1]         
    if fmt == FMT_DECIMAL: # LAT:dd.dddddd,LON:ddd.dddddd (with MAX_DECIMALS decimals)
      msg = "LAT:" + lat[0:lat.find(".")+MAX_DECIMALS+1] + ", LON:" + lon[0:lon.find(".")+MAX_DECIMALS+1]    
    if fmt == FMT_60:
      la_deg = la
      la_min = (la-int(la))*60
      la_sec = (la_min-int(la_min))*60
      
      lo_deg = lo
      lo_min = (lo-int(lo))*60
      lo_sec = (lo_min-int(lo_min))*60
      
      StrLat = str(int(la_deg))+ "^ " + str(int(la_min)) + "' " + str((la_sec))
      StrLat = StrLat[0:StrLat.find(".")+MAX_DECIMALS+1] + "''"
      
      StrLon = str(int(lo_deg))+ "^ " + str(int(lo_min)) + "' " + str((lo_sec))
      StrLon = StrLon[0:StrLon.find(".")+MAX_DECIMALS+1] + "''"
      
      msg = "LAT:" + StrLat + ", LON:" + StrLon
    if fmt == FMT_CUSTOM1:
      pass
    if fmt == FMT_CUSTOM2:
      pass
  except Exception, e:
    print "Error formatting message: " + str(e)
    GlobalErr = e
#  finally:
  return msg
  
  
def Connect():
  global GPS_CONNECT_ERROR,GPS_address,GlobalErr
  try:
    GlobalErr = 0
    #return "debug"
    sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    print "Looking for devices..."
    address,service=socket.bt_discover(GPS_address)    # cerca ricevitore.
    print "Connecting..."
    target=(address,service.values()[0]) # si collega
    sock.connect(target)# al ricevitore.
    print "Connected to ",target,address
  except Exception, e:
    GlobalErr = e
    sock=GPS_CONNECT_ERROR
    print "Error connecting to BT device: "+ str(e)
  #finally:
  return sock
  
def ReadPos():
      global sock,MSG_FORMAT, MAXATTEMPTS,GPS_CONNECT_ERROR,GPS_RECONNECT_ERROR,GlobalErr
      print "   DEBUG - controllo SOCK..."
      if (sock==GPS_CONNECT_ERROR) or (GlobalErr<>0):
        print "   DEBUG - errore, riconnetto..."
        attempts = 0
        while (GlobalErr<>0) and (attempts<=MAXATTEMPTS):
          sock=Connect()
          attempts = attempts + 1
        if sock==GPS_CONNECT_ERROR:
          print "   DEBUG -  impossibile riconnettersi"
          return GPS_RECONNECT_ERROR
      print "   DEBUG - tutto ok, procedo..."
      msg="[empty]"
      GlobalErr = 0
      try:
        valid = 0 
        attempts = 0
        GlobalErr = 0
        while (valid==0) and (attempts<=MAXSTRINGATTEMPTS): # If unknown line is read from GPS, device output must be read again.
            #print "   DEBUG - inizio ciclo lettura"
            attempts = attempts + 1
            rawdata="[ToBeRead]"
            rawdata = readline(sock) 
            print "raw=",rawdata
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
                  valid = 0 # No useful data?
                if sentence_id == 'GLL':
                  location = get_gll_location(sentence_data)
                  valid = 0 # No useful data?
                if sentence_id == 'RMC':
                  location = get_rmc_location(sentence_data)
                  valid = 1     
                if valid == 1:                
                  temp = 'LAT:' + location['lat'] + ',LON:' + location['long']
                  la = str(int(temp[4:6])+float(temp[6:13])/60)
                  lo = str(int(temp[19:22])+float(temp[22:29])/60)
                  msg = FormatMessage(la,lo,MSG_FORMAT) 
                else:
                  msg = "Invalid data, can't format"
            else:
                print "****** invalid data *****"
                msg= 'ERROR: couldnt receive GPS data'   
      except Exception,e:
        GlobalErr = e
        print "Error in readpos(): " + str(e)
        
      #mcc, mnc, lac, cellid = locationAPI.gsm_location()         
      if valid==0:
        msg=msg+ str(GlobalErr)
      if GlobalErr == "":
        GlobalErr = "Couldn't receive data from GPS"    
      # Add GSM position (You can use www.opencellid.org to determine position:  http://www.opencellid.org/cell/get?mnc=1&mcc=2&lac=200&cellid=234 "
      #msg = msg + " - GSM: mcc=" +  str(mcc) + ", mnc=" +  str(mnc) + ", lac=" + str(lac) + ", cellid=" +  str(cellid)    
      return msg
      
      
def SendMess(n,m):
  global GlobalErr
  #print "Invio messaggio " + m + " a " + n
  try:
    GlobalErr = 0
    messaging.sms_send(n,m) # DEBUG
  except Exception,e:
    GlobalErr = e
    print "Error sending SMS: " + str(e)

def read_sms(id): #DEBUG
#def read_sms():
    global GlobalErr,Recipient_number,sock
    global TRACKING
    ##############################à
    #sms_text="TRACK ON" # DEBUG*********
    ##############################à
    try:
      GlobalErr = 0
      e32.ao_sleep(0.1)
      try:
        i=inbox.Inbox() #DEBUG
      except:
        print "ERROR connecting to inbox"
      try:
        sms_text=i.content(id) #DEBUG
        print "SMS ricevuto: ", sms_text
      except:
        print "Error retrieving message body"
      # Execute different actions depending on SMS contents:
      if sms_text[0:8].upper() == 'TRACK ON':
        i.delete(id) # Delete just received message
        print "riconosciuto TRACK ON"
        SendMess(Recipient_number,'TRACKING ACTIVATED!')
        TRACKING = 1
        while (TRACKING == 1):
          e32.ao_sleep(INTERVAL)
          UploadPosition()
          #msg=ReadPos()
          #SendMess(Recipient_number,'TRACKING: '+msg)  
          print 'Tracker message uploaded.'
      if sms_text[0:9].upper() == 'TRACK OFF':
        print "riconosciuto TRACK OFF"
        i.delete(id) # Delete just received message
        TRACKING = 0
        SendMess(Recipient_number, "tracking DEactivated!")
      if sms_text[0:4].upper() == 'SEND':
        print "riconosciuto SEND"
        i.delete(id) # Delete just received message
        #print 'Reading position....'      
        #msg=ReadPos()
        #print 'Sending position ' + msg + ' to ' + Recipient_number 
        UploadPosition()
        #SendMess(Recipient_number, msg) # Send SMS.
        print 'Position uploaded.'
      if sms_text[0:6].upper() == 'STATUS':
        print "riconosciuto STATUS"      
        i.delete(id) # Delete just received message
        SendMess(Recipient_number, "Status: GlobalErr="+repr(GlobalErr)+", msg=" + msg) # Send SMS.
    except Exception, e:
      GlobalErr = e
      print "Error processing message >>" + sms_text + "<< :"+ str(e) 


def ReadSettings():
    global Recipient_number,GPS_address
    global FILEPATH
    global GlobalErr
    try:
        GlobalErr = 0
        f=open(FILEPATH,'rt')  # Open for reading
        print "file impostazioni aperto..."
        try:
            GlobalErr = 0        
            content = f.read()
            content=content[0:len(content)-2]
            print "contenuto letto..."
            parameters=eval(content) # Store values
            print "valori estratti."
            f.close()
            Recipient_number = parameters.get('recipient','')  # read values
            GPS_address = parameters.get('GPS','')
            print "Numero destinazione:" , Recipient_number
            print "GPS:", GPS_address
        except Exception, e: 
            GlobalErr = e
            print 'Couldnt read settings file - err 001'
            print 'System message: ' + str(e)
    except Exception, e: 
        GlobalErr = e
        print 'Couldnt read settings file - err 002'
        print 'System message: ' + str(e)
           
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
  global GlobalErr
  try:
    GlobalErr = 0
    d = data.split(',')
    ret = {}
    ret['type'] = 'GGA'
    ret['lat'] = "%s%s" % (d[1],d[2])
    ret['long'] = "%s%s" % (d[3],d[4])
    ret['time'] = format_time(d[0])
  except Exception, e:
    GlobalErr = e
    print "Error getting location from GGA sentence: " + str(e)
  #finally:
  return ret
 
# Get the location from a GLL sentence
def get_gll_location(data):
  global GlobalErr
  try:
    GlobalErr = 0
    d = data.split(',')
    ret = {}
    ret['type'] = 'GLL'
    ret['lat'] = "%s%s" % (d[0],d[1])
    ret['long'] = "%s%s" % (d[2],d[3])
    ret['time'] = format_time(d[4])
  except Exception, e:
    GlobalErr = e
    print "Error getting location from GLL sentence: " + str(e)
  #finally:
  return ret
 
# Get the location from a RMC sentence
def get_rmc_location(data):
  global GlobalErr
  try:
    GlobalErr = 0
    d = data.split(',')
    ret = {}
    ret['type'] = 'RMC'
    ret['lat'] = "%s%s" % (d[2],d[3])
    ret['long'] = "%s%s" % (d[4],d[5])
    ret['time'] = format_time(d[0])
  except Exception, e:
    GlobalErr = e
    print "Error getting location from RMC sentence: " + str(e)
  #finally:
  return ret
  
def readline(sock):
  """Read one single line from the socket"""
  global GlobalErr
  line = ""
  try:
    GlobalErr = 0
    print "Retrieving data from GPS..."
    while 1:
      char = sock.recv(1)
      if not char: break
      line += char
      if char == "\n": break
  except Exception, e:
    print "Error readline(sock)"
    GlobalErr = e
  #finally:
  print "Done."
  return line

ReadSettings()

sock=Connect() # Connect to bluetooth GPS; sock=GPS_CONNECT_ERROR in case of error.
print "SOCK=",sock
StoreSettings = MSG_FORMAT

############# Usage example:
### WARNING: These example will override setting for MSG_FORMAT variable at
### the beginning of the source!!!
#
#MSG_FORMAT = FMT_YOUPOSITION
#print ReadPos() # DEBUG

#e32.ao_sleep(3)
#MSG_FORMAT = FMT_DECIMAL
#print ReadPos() # DEBUG

#e32.ao_sleep(3)
#MSG_FORMAT = FMT_60
print "Current position:",  ReadPos() # DEBUG
############################

MSG_FORMAT = StoreSettings

print 'connecting to inbox...'
try:
  GlobalErr = 0
  i=inbox.Inbox()  #DEBUG
except Exception, e:
  GlobalErr = e
  print "Error connecting to inbox: " + str(e)
  
# Connect messages receiving to program:   
try:
  GlobalErr = 0
  i.bind(read_sms) #DEBUG
  print 'Connected. Waiting for incoming messages...'
except Exception, e:
  GlobalErr = e
  print "Error binding inbox to function: " + str(e)

script_lock = Ao_lock()

app.exit_key_handler = quit
capturer=keycapture.KeyCapturer(cb_capture)
capturer.forwarding=0
capturer.keys=(keycapture.EKey0,keycapture.EKey1,keycapture.EKey2,keycapture.EKey3,keycapture.EKey4)
PrintOptions()
capturer.start()

# while abort==0: #endless loop to monitor for incoming calls
#   if phone_ext.CallStatus() == 5:
#     phone_ext.HangUp()
#     e32.ao_sleep(5)  
#     phone_no = str(phone_ext.LastCall())
#     UploadPosition()  
#     print "Position uploaded."
    
script_lock.wait()



