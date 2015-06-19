import threading
import time
import gps
import csv


class GpsPoller(threading.Thread):
    __log_file_name = None
    __log_file = None
    __csv_writer = None
    __current_value = None
    __start_time = None
    __debug = None
    running = False

    def __init__(self, a_log_file_name='./gps.csv', a_debug=False):
        self.__log_file_name = a_log_file_name
        self.__log_file = open(self.__log_file_name, 'wb')
        self.__csv_writer = csv.writer(self.__log_file, delimiter=',',
                                       quotechar='|',
                                       quoting=csv.QUOTE_MINIMAL)
        self.__start_time = time.clock()
        self.__debug = a_debug
        threading.Thread.__init__(self)
        self.gpsd = gps.gps(mode=gps.WATCH_ENABLE)
        self.running = True

    def run(self):
        while self.running:
            if self.gpsd.next() != -1:
                delta_time = time.clock() - self.__start_time
                csv_row = list()
                delta_time = '%.3f' % delta_time
                csv_row.append(delta_time)
                utc_time = self.gpsd.utc
                csv_row.append(utc_time)
                latitude = '%.5f' % self.gpsd.fix.latitude
                csv_row.append(latitude)
                longitude = '%.5f' % self.gpsd.fix.longitude
                csv_row.append(longitude)
                speed_ms = '%.2f' % self.gpsd.fix.speed
                csv_row.append(speed_ms)
                if self.__debug:
                    print(csv_row)
                self.__csv_writer.writerow(csv_row)
            elif self.gpsd.next() == 1:
                print('got -1')

"""
gps_thread = GpsPoller('./gps.csv', True)
try:
    gps_thread.start()
    while True:
        time.sleep(1)

except (KeyboardInterrupt):
    gps_thread.running = False
    gps_thread.join()
"""
