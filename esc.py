import os
import time


import pigpio

os.system("sudo pigpiod")  # Launching GPIO library


ESC = 17 
pi =pigpio.pi()

time.sleep(2)
print("podau signal")

for speed in range(1000,2000):
    pi.set_servo_pulsewidth(ESC, speed)
    time.sleep(2)

