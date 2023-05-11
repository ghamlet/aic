import os
import time


import pigpio

os.system("sudo pigpiod")  # Launching GPIO library


ESC = 17 
pi =pigpio.pi()

time.sleep(2)
print("podau signal")


    
pi.set_servo_pulsewidth(ESC, 1000)
time.sleep(2)

pi.set_servo_pulsewidth(ESC, 1200)
time.sleep(2)

