import serial


class Arduino: 
    def __init__(self, port, baudrate=9600, timeout=None, coding='utf-8'):
        self.serial_connected = False
        self.serial = serial.Serial(port, baudrate=baudrate, timeout=timeout, write_timeout=1)

        #self.serial.flush()
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

        self.serial_connected = True
        self.coding = coding

    def send_data(self, data):  
        #print('Sent to Arduino:', data)
       
        try:
            self.serial.write(data.encode(self.coding))
        except serial.SerialTimeoutException:
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()

    def read_data(self):
        line = self.serial.readline().decode(self.coding).strip()
        return line

    def set_speed(self, speed):
        msg = 'e'+str(speed)
        self.send_data(msg)

    def set_angle(self, angle):
        msg = 's'+str(angle)
        self.send_data(msg)

   # def dist(self, speed, turn):
      #  msg = 'DIST'+str(speed):{turn}'
       # self.send_data(msg)

    def stop(self):
        msg = 'STOP'
        self.send_data(msg)

    def drop(self):
        msg = 'DROP'
        self.send_data(msg)

    def __del__(self):
        if self.serial_connected:
            self.serial.close()
