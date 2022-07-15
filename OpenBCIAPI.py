# Imports
from cyton import OpenBCICyton
import serial
import serial.tools.list_ports as st

class OpenBCIAPI:

    def __init__(self, num_ch=8, debug=False, daisy=False):
        self.num_ch = num_ch                                        # The number of channels in use
        self.debug = debug                                          # Debug script enabled status
        self.daisy = daisy                                          # Determines if the Daisy is attached
        self.baud = 115200                                          # Default baud rate
        self.com_port = None                                        # The COM port for UART
        self.serial = None                                          # Serial connection to board

    def connect(self):
        if self.com_port is None:                                   # If no COM port is specified
            ports = st.comports()                                   # Get all open COM ports

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
                        print("OpenBCI port: %s" % self.com_port)
                    break                                           # Exit the loop

            if self.com_port is None:                               # If no board detected
                print('No OpenBCI board detected.')                 # Notify user
                s.close()                                           # Close loose connection

        else:
            self.serial = serial.Serial(port=self.com_port,
                                        baudrate=self.baud,
                                        timeout=10)                 # Open serial connection to COM port
            self.serial.write(b'v')                                 # Request message from OpenBCI board
            message = self.serial.readline()                        # Read incoming message

            if b'OpenBCI' in message:                               # Check if OpenBCI board is detected
                print('OpenBCI connection established.')            # Notify user if connection established
            else:                                                   # If no board detected
                print('No OpenBCI board detected.')                 # Notify user
                self.serial.close()                                 # Close loose connection

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

        if 'COM' not in com:                                        # Check if COM port given
            raise ValueError("Port names must be in the format "
                             "of 'COMi', where i is an integer.")   # Give feedback on correct data format

        open_ports = [p[0] for p in st.comports()]                  # Get open ports

        if com not in open_ports:                                   # Check that given port is open
            raise ValueError("Selected COM port is not open.")      # Raise error for closed ports

        self.com_port = com                                         # Set port to user's input


if __name__ == '__main__':

    test = OpenBCIAPI()
    print(test.com_port)
    test.set_com_port('COM3')
    print(test.com_port)
    test.connect()
    print(test.com_port)
