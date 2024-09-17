import time

import serial

# Definition of the Arduino class to manage communication with an Arduino device over a serial port
class Arduino(object):

    def __init__(self, port):
        self.test = None  # Variable to store the result of the G-code test
        self.port = port  # Serial port to which the Arduino is connected
        self.ser = None  # Serial connection object

    # Method to open the serial port and establish communication with the Arduino
    def open_port(self):
        # Specify the serial port of the Arduino
        port = self.port
        try:
            # Try to open the serial port
            self.ser = serial.Serial(port, 115200, timeout=.1)
            # 115200

            # The serial port was opened successfully
            print(f"Port {port} opened successfully")

        except serial.SerialException:
            # A SerialException is raised if the port cannot be opened
            print(f"Failed to open port {port}. Check if it's available and try again.")
        except Exception as e:
            # Handle any other possible exceptions
            print(f"An error occurred: {str(e)}")

    # Method to send a G-code command to the Arduino
    def write_read(self, g_code):
        self.ser.write((g_code + "\r\n").encode())
        time.sleep(0.1)
        print(g_code)
        # while True:
        #     data = self.ser.readline()
        #     if data == b'ok\r\n':
        #         print(data)
        #         break

    # Method to close the serial port connection
    def close_port(self):
        try:
            # Close port
            if self.ser is not None:
                self.ser.close()
                print(f"Port {self.port} closed successfully")
        except Exception as e:
            print(f"An error occurred while closing the port: {str(e)}")

    # Method to test the $G command by sending a G-code and checking for a response from the Arduino
    def test_G2(self) -> bool:
        self.write_read("$G")  # Send the $G command to get the current G-code state
        self.test = True  # Set the test result to True by default

        while True:
            try:
                # Check if there is data waiting to be read from the serial port
                if self.ser.in_waiting > 0:
                    available_bytes = self.ser.in_waiting  # Get the number of available bytes
                    bytes_data = self.ser.read(available_bytes)  # Read the available data
                    message = bytes_data.decode("utf-8")  # Decode the data into a string
                    print("Arduino : " + message)

                    # Check if the response contains the "[GC:" string, indicating valid G-code
                    if "[GC:" in message:
                        print("[GC: was detected !")
                        self.test = True  # Mark the test as successful
                        break  # Exit the loop
                    else:
                        time.sleep(0.01)  # Wait briefly and continue checking
                        self.test = False  # Mark the test as failed if no valid response
            except Exception as e:
                print(f"Une exception s'est produite : {e}")

        return self.test

    # Another method to test G-code communication, which reads several lines from the Arduino
    def test_G(self):
        self.write_read("$G")  # Send the $G command
        rawdata = []  # List to store raw data from the Arduino
        compt = 0  # Counter to track the number of reads
        while compt < 5:
            time.sleep(2)
            rawdata.append(str(self.ser.readline().decode().strip()))  # Read and decode the response
            compt += 1  # Increment the counter
            print("arduino !! : ", self.ser.readline())  # Print each line read from the Arduino
        print(rawdata)  # Print the collected raw data
        print("arduino : ", self.ser.readline())  # Print the final line read from the Arduino


        #self.write_read("$G")
        #line = self.ser.readline().decode('utf-8').strip()
        #print("Données reçues depuis Arduino:", line)






