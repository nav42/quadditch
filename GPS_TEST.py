from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % args.connect
vehicle = connect(args.connect, baud=57600, wait_ready=True)

# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

  while not vehicle.is_armable:
    time.sleep(1)

  print "Arming motors"
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True



  print "Taking off!"
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    altitude = vehicle.location.global_relative_frame.alt
    print " Altitude: ", altitude 
    #Break and return from function just below target altitude.        
    if altitude >= aTargetAltitude - 1: 
      print "Reached target altitude"
      break
    time.sleep(1)

#----------------MAIN PROGRAM---------------
# Initialize the takeoff sequence to 20m
arm_and_takeoff(10)

print("Take off complete")


# Hover for 10 seconds
time.sleep(10)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")
time.sleep(20)

# Close vehicle object
vehicle.close()
