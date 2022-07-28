# Imports
# from cyton import OpenBCICyton
import serial
import serial.tools.list_ports as st
import time
from threading import Thread
import datetime as dt


class OpenBCIAPI:

    def __init__(self, num_ch=8, debug=False, daisy=False):
        """
        An OpenBCIAPI object can be used to interface between a python script and Cyton board\n
        :param num_ch: The number of channels being used
        :param debug: Determines if debug messages are enabled
        :param daisy: Set to True if Daisy module is being used
        """
        self.num_ch = num_ch                                        # The number of channels in use
        self.debug = debug                                          # Debug script enabled status
        self.daisy = daisy                                          # Determines if the Daisy is attached
        # TODO
        # Activate daisy on a firmware level when needed
        if self.daisy:
            self.sampling_rate = 125                                # Sampling rate at 125 Hz with Daisy Module
        else:
            self.sampling_rate = 250                                # Sampling rate at 250 Hz with Daisy Module
        self.baud = 115200                                          # Default baud rate
        self.com_port = None                                        # The COM port for UART
        self.serial = None                                          # Serial connection to board
        self.sample = None                                          # The data received from the board
        self.sample_num = None                                      # The number of samples received
        self._streaming = None

    def stream(self):
        self.serial.write(b'b')                                     # Send begin stream command
        self._streaming = True

        if self.debug:
            print("Streaming started.")

        while self._streaming:

            # self.serial.flushInput()

            header = self.serial.read(1)    # Read the first byte

            print(header)

            if header == b'\xa0':
                line = self.serial.read(32)
                line = header + line
                # print(line)
                # print("Header: {}".format(hex(line[0])))
                # print("Sample Number: " + str(line[1]))
                # print("Channel 1: {}".format(line[2:5]))
                # print("Channel 2: {}".format(line[5:8]))
                # print("Channel 3: {}".format(line[8:11]))
                # print("Channel 4: {}".format(line[11:14]))
                # print("Channel 5: {}".format(line[14:17]))
                # print("Channel 6: {}".format(line[17:20]))
                # print("Channel 7: {}".format(line[20:23]))
                # print("Channel 8: {}".format(line[23:26]))
                # print("Acc X1: {}".format(hex(line[26])))
                # print("Acc X0: {}".format(hex(line[27])))
                # print("Acc Y1: {}".format(hex(line[28])))
                # print("Acc Y0: {}".format(hex(line[29])))
                # print("Acc Z1: {}".format(hex(line[30])))
                # print("Acc Z0: {}".format(hex(line[31])))
                # print("Footer: {}".format(hex(line[32])))
                # print(len(line))


    def stop_stream(self):

        if self.debug:
            print("Stream stopped.")
        self.serial.write(b's')                                     # Request board to stop streaming
        self._streaming = False                                     # End streaming loop

    # """
    #   PARSER:
    #   Parses incoming data packet into OpenBCISample.
    #   Incoming Packet Structure:
    #   Start Byte(1)|Sample ID(1)|Channel Data(24)|Aux Data(6)|End Byte(1)
    #   0xA0|0-255|8, 3-byte signed ints|3 2-byte signed ints|0xC0
    #
    # """

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
                    while b'$$$' not in message:
                        message = self.serial.readline()  # Go through rest of restart message
                    if self.debug:
                        print("OpenBCI port: %s" % self.com_port)   # Show port in debug
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
                if self.debug:
                    print("OpenBCI port: %s" % self.com_port)       # Show port in debug
                while b'$$$' not in message:
                    message = self.serial.readline()                # Go through rest of restart message
            else:                                                   # If no board detected
                print('No OpenBCI board detected.')                 # Notify user
                self.serial.close()                                 # Close loose connection

    def disconnect(self):
        self.serial.close()                                         # Close the port connection

    def live_plot(self):
        pass

    def stop_live_plot(self):
        pass

    def record(self, filename=None):
        if filename is None:
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

    test = OpenBCIAPI(debug=True)
    print(test.com_port)
    test.set_com_port('COM3')
    print(test.com_port)
    test.connect()
    print(test.com_port)
    test.stream()
