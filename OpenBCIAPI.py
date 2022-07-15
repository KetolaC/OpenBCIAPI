# Imports
from cyton import OpenBCICyton
import serial
import serial.tools.list_ports

class OpenBCIAPI:

    def __init__(self, num_ch=8, debug=False, daisy=False):
        self.num_ch = num_ch
        self.debug = debug
        self.daisy = daisy
        self.baud = 115200  # Default baud rate
        self.com_port = None
        self.serial = None

        # TODO
        # connect to UART using the connect method

    def connect(self):
        if self.com_port is None:                                   # If no COM port is specified
            ports = serial.tools.list_ports.comports()              # Get all open COM ports

            for p in ports:                                         # Parse through open COM ports
                s = serial.Serial(port=p[0], baudrate=self.baud,
                                  timeout=10)                       # Open serial connection to COM port
                s.write(b'v')                                       # Request message from OpenBCI board
                message = s.readline()                              # Read incoming message

                if b'OpenBCI' in message:                           # Check if OpenBCI board is detected
                    print('OpenBCI connection established.')        # Notify user if connection established
                    self.com_port = p[0]                            # Save the COM port
                    self.serial = s                                 # Save the serial connection
                    if self.debug:
                        print("OpenBCI port: %s" %(self.com_port))
                    break                                           # Exit the loop

            if self.com_port is None:                               # If no port detected
                print('No OpenBCI board detected.')                  # Notify user
                s.close()                                           # Close loose connection

    def disconnect(self):
        pass

    def live_plot(self):
        pass

    def stop_live_plot(self):
        pass

    def record(self):
        pass

    def stop_record(self):
        pass

    def deactivate_channels(self, channels):
        pass

    def activate_channels(self, channels):
        pass

    def set_gain(self, gain):
        pass

    def timestamp(self, active):
        pass

    def set_baud(self, baud):
        self.baud = baud

    def set_com_port(self, com):
        if 'COM' not in com:
            raise ValueError("Port names must be in the format of 'COMi', where i is an integer.")
        self.com_port = com


if __name__ == '__main__':

    test = OpenBCIAPI()
    print(test.com_port)
    # test.set_com_port('COM4')
    test.connect()
    print(test.com_port)
