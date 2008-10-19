import appswitch, time,keypress
from key_codes import *
print "Waiting..."
time.sleep(5)
print "Clicking..."
keypress.simulate_key(EKeyLeftSoftkey,EKeyLeftSoftkey)
#time.sleep(1)
#keypress.simulate_key(EKeyRightSoftkey,EKeyRightSoftkey)
print "End."


