#!/usr/bin/env python

import time
import subprocess
import RPi.GPIO as GPIO
from datetime import datetime
from threads import KDSThread, GpsThread, LedBlink

# Pin config
LED_GREEN = 20
LED_RED = 21
BUTTON = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Thread objects
kds_thread = False
gps_thread = False
blink_thread = False

GPIO.output(LED_RED, GPIO.LOW)
GPIO.output(LED_GREEN, GPIO.HIGH)
time.sleep(2)


def start_recording():
   global kds_thread, gps_thread
   GPIO.output(LED_GREEN, GPIO.LOW)
   blink_thread = LedBlink(3, "BlinkThread", LED_RED)
   blink_thread.start()

   proc = subprocess.Popen("/picam/start.sh", shell=True)
   time.sleep(5)

   start_datetime = datetime.now()
   outfile = open("/datos/%s.log" % start_datetime, 'a')
   outfile.write("Datetime, Elapsed Time, Latitude, Longitude, "
                 "Speed, GPS Speed, Lean, GForce, RPMs\n")

   kds_thread = KDSThread(1, "KDSThread")
   gps_thread = GpsThread(2, "GPSThread")
   kds_thread.start()
   gps_thread.start()

   proc = subprocess.Popen(
      "echo 'dir=/datos\nfilename=%s.ts' > /picam/hooks/start_record" % start_datetime,
      shell=True)

   blink_thread.running = False
   blink_thread.join()
   GPIO.output(LED_RED, GPIO.HIGH)
   while True:
      input_state = GPIO.input(BUTTON)
      if input_state == False:
         outfile.close()
         stop_recording()
         break

      now = datetime.now()
      outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
         now, (now - start_datetime),
         gps_thread.latitude, gps_thread.longitude, kds_thread.kph, gps_thread.speed,
         kds_thread.lean, kds_thread.gforce, kds_thread.rpm))

      time.sleep(0.2)


def stop_recording():
   global kds_thread, gps_thread

   blink_thread = LedBlink(3, "BlinkThread", LED_RED)
   blink_thread.start()
   proc = subprocess.Popen("touch /picam/hooks/stop_record", shell=True)
   time.sleep(3)

   kds_thread.running = False
   kds_thread.join()

   gps_thread.running = False
   gps_thread.join()

   proc = subprocess.Popen("find /picam/ -name '*.ts' -exec rm -f '{}' \;", shell=True)
   proc = subprocess.Popen("killall picam", shell=True)
   blink_thread.running = False
   blink_thread.join()
   GPIO.output(LED_GREEN, GPIO.HIGH)


try:
   while True:
      input_state = GPIO.input(BUTTON)
      if input_state == False:
         start_recording()

      time.sleep(0.2)

except (KeyboardInterrupt, SystemExit):
   kds_thread.running = False
   gps_thread.running = False
   print "Exiting!"

