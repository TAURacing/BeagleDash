import os
import gps
import time
import time
import threading

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps.gps(mode=WATCH_ENABLE)
        self.current_value = None # ???
        self.running = True

    def run(self):
        while self.running:
            if self.gpsd.next() != -1:
                print('got data')
                print('lat: ' + str(self.gpsd.fix.latitude))
            elif: self.gpsd.next() == 1:
                print('got -1')

gps_thread = GpsPoller() # create the thread
try:
    gps_thread.start() # start it up
    while True:
        #It may take a second or two to get good data
        #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

        #os.system('clear')
#
        #print
        #print ' GPS reading'
        #print '----------------------------------------'
        #print 'latitude    ' , gpsd.fix.latitude
        #print 'longitude   ' , gpsd.fix.longitude
        #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        #print 'altitude (m)' , gpsd.fix.altitude
        #print 'eps         ' , gpsd.fix.eps
        #print 'epx         ' , gpsd.fix.epx
        #print 'epv         ' , gpsd.fix.epv
        #print 'ept         ' , gpsd.fix.ept
        #print 'speed (m/s) ' , gpsd.fix.speed
        #print 'climb       ' , gpsd.fix.climb
        #print 'track       ' , gpsd.fix.track
        #print 'mode        ' , gpsd.fix.mode
        #print
        #print 'sats        ' , gpsd.satellites

        time.sleep(5) #set to whatever

except (KeyboardInterrupt, SystemExit):
    print "\nKilling Thread..."
    gps_thread.running = False
    gps_thread.join()
print "Done.\nExiting."
