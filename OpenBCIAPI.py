# Imports
import os
import serial
import serial.tools.list_ports as st
import time
from threading import Event, Thread
import datetime as dt


class OpenBCIAPI:

    def __init__(self, num_ch=8, debug=False, daisy=False):
        """
        An OpenBCIAPI object can be used to interface between a python script and Cyton board\n
        :param num_ch: The number of channels being used
        :param debug: Determines if debug messages are enabled
        :param daisy: Set to True if Daisy module is being used
        """
        self.num_ch = num_ch  # The number of channels in use
        self.debug = debug  # Debug script enabled status
        self.daisy = daisy  # Determines if the Daisy is attached
        self.sampling_rate = 256  # Sampling rate at 250 Hz with Daisy Module
        self.baud = 115200  # Default baud rate
        self.com_port = None  # The COM port for UART
        self.serial = None  # Serial connection to board
        self._buffer = ''
        self._streaming = Event()  # Control the streaming thread
        self._data_ready = Event()  # Determine when a new sample is collected
        self._recording = Event()  # Keep track of recording status

    def _get_sample(self):

        while True:
            if not self._streaming.is_set():
                break

            header = self.serial.read(1)  # Read a single byte from buffer

            while header != b'\xa0':
                header = self.serial.read(1)  # Read a single byte from buffer
                if self.debug:
                    print("Finding next header")

            if self.debug:
                print("Data package located")  # Send debug message

            line = self.serial.read(32)  # Retrieve the remainder of the package data
            line = header + line  # Concatenate whole package

            if len(line) == 33:

                sample_num = line[1]  # Save sample number

                if self.debug:
                    print("Sample number: %i" % sample_num)

                eeg_data = [line[2:5], line[5:8], line[8:11],
                            line[11:14], line[14:17], line[17:20],
                            line[20:23], line[23:26]]  # Save the EEG data

                for i in range(len(eeg_data)):
                    temp = ''
                    for j in eeg_data[i]:
                        temp = temp + format(j, '08b')
                    if temp != '':
                        eeg_data[i] = int(temp, 2)
                    else:
                        if self.debug:
                            print("bad eeg data: ")
                            print(eeg_data[i])
                            print(len(line))

                accel_data = [line[26], line[27], line[28],
                              line[29], line[30], line[31]]  # Save the accelerometer data

                self._buffer = self._buffer \
                               + str(sample_num) \
                               + str(eeg_data) \
                               + str(accel_data) + "\n"

            if self.debug:
                print("Size of buffer: %i" % len(self._buffer))

            if sample_num == 255:
                if self.debug:
                    print("buffer full")
                    return

    def _stream(self):
        self.serial.write(b'b')  # Send begin stream command
        self._streaming.set()  # Set streaming condition

        if self.debug:
            print("Streaming started.")  # Debug message

        while self._streaming.is_set():  # Repeat loop until stop stream event
            self._get_sample()  # Call the sampling method

        if self.debug:
            print("Stream terminated internally")  # Debug message when stream stopped

    def _stop_stream(self):

        if self.debug:
            print("Stream stopped.")  # Debug message for stopping stream
        self.serial.write(b's')  # Request board to stop streaming
        self._streaming.clear()  # End streaming loop

    def _write_sample(self, file):

        if self.debug:
            print("Saving to file")

        s = str(self._buffer)
        file.write(s)
        self._buffer = ''

    def connect(self):
        if self.com_port is None:  # If no COM port is specified
            ports = st.comports()  # Get all open COM ports

            for p in ports:  # Parse through open COM ports
                s = serial.Serial(port=p[0], baudrate=self.baud,
                                  timeout=10)  # Open serial connection to COM port
                s.write(b'v')  # Request message from OpenBCI board
                message = s.readline()  # Read incoming message

                if b'OpenBCI' in message:  # Check if OpenBCI board is detected
                    print('OpenBCI connection established.')  # Notify user if connection established
                    self.com_port = p[0]  # Save the COM port
                    self.serial = s  # Save the serial connection
                    while b'$$$' not in message:
                        message = self.serial.readline()  # Go through rest of restart message
                    if self.debug:
                        print("OpenBCI port: %s" % self.com_port)  # Show port in debug
                    break  # Exit the loop

            if self.com_port is None:  # If no board detected
                if len(ports) > 0:
                    s.close()  # Close loose connection
                raise ValueError('No OpenBCI board detected.')  # Notify user

        else:
            self.serial = serial.Serial(port=self.com_port,
                                        baudrate=self.baud,
                                        timeout=10)  # Open serial connection to COM port
            self.serial.write(b'v')  # Request message from OpenBCI board
            message = self.serial.readline()  # Read incoming message

            if b'OpenBCI' in message:  # Check if OpenBCI board is detected
                print('OpenBCI connection established.')  # Notify user if connection established
                if self.debug:
                    print("OpenBCI port: %s" % self.com_port)  # Show port in debug
                while b'$$$' not in message:
                    message = self.serial.readline()  # Go through rest of restart message
            else:  # If no board detected
                self.serial.close()  # Close loose connection
                raise ValueError('No OpenBCI board detected.')  # Notify user

    def disconnect(self):
        self.serial.close()  # Close the port connection

    def timed_record(self, seconds=10, filename=None):

        if type(seconds) is not int:
            raise ValueError("Seconds must be given as an integer")

        if filename is None:
            filename = os.getcwd() + "\\recording_" + \
                       str(dt.datetime.now().strftime(
                           "%Y%m%d-%H-%M-%S")) + ".txt"  # Name the file according to date and time
            if self.debug:
                print(filename)
        f = open(filename, 'a')

        t = Thread(target=self._stream, args=())\

        t.start()

        while not self._streaming.is_set():
            if self.debug:
                print("Waiting for streaming to start")
            time.sleep(0.1)

        time.sleep(seconds + 0.8)

        self._stop_stream()

        t.join()

        self._write_sample(f)

        if self.debug:
            print("Closing file")
        f.close()

        if self.debug:
            print("Done recording %i seconds of data" % seconds)

    def cont_record(self, filename=None):

        if filename is None:
            filename = os.getcwd() + "\\recording_" + \
                       str(dt.datetime.now().strftime(
                           "%Y%m%d-%H-%M-%S")) + ".txt"  # Name the file according to date and time
            if self.debug:
                print(filename)

        f = open(filename, 'a')

        t = Thread(target=self._stream, args=())
        t.start()

        while not self._streaming.is_set():
            if self.debug:
                print("Waiting for streaming to start")
            time.sleep(0.1)

        space = False

        print("Gonna enter loop")

        while not space:
            k = input("Press enter to end the recording session")
            if k is not None:
                print("Input received")
                space = True

        time.sleep(0.8)

        print("Left loop")

        self._stop_stream()
        print("Stream stopped")
        t.join()
        self._write_sample(f)
        print("Done writing")

        if self.debug:
            print("Closing file")
        f.close()

        if self.debug:
            print("Done recording EEG data")

    def set_baud(self, baud):
        self.baud = baud

    def set_com_port(self, com):

        if 'COM' not in com:  # Check if COM port given
            raise ValueError("Port names must be in the format "
                             "of 'COMi', where i is an integer.")  # Give feedback on correct data format

        open_ports = [p[0] for p in st.comports()]  # Get open ports

        if com not in open_ports:  # Check that given port is open
            raise ValueError("Selected COM port is not open.")  # Raise error for closed ports

        self.com_port = com  # Set port to user's input


if __name__ == '__main__':

    cwd = os.getcwd()                   # Retrieves the current working directory

    openbci = OpenBCIAPI(debug=False)  # Creates an OpenBCIAPI object

    openbci.connect()
    openbci.cont_record()
    openbci.disconnect()
