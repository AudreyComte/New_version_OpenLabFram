import time

import serial


class Arduino(object):

    def __init__(self, port):
        self.test = None
        self.port = port
        self.ser = None

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

    def write_read(self, g_code):
        self.ser.write((g_code + "\r\n").encode())
        time.sleep(0.1)
        print(g_code)
        # while True:
        #     data = self.ser.readline()
        #     if data == b'ok\r\n':
        #         print(data)
        #         break

    def close_port(self):
        try:
            # Close port
            if self.ser is not None:
                self.ser.close()
                print(f"Port {self.port} closed successfully")
        except Exception as e:
            print(f"An error occurred while closing the port: {str(e)}")

    def test_G2(self) -> bool:
        self.write_read("$G")
        self.test = True

        while True:
            try:
                if self.ser.in_waiting > 0:
                    available_bytes = self.ser.in_waiting
                    bytes_data = self.ser.read(available_bytes)
                    message = bytes_data.decode("utf-8")
                    print("Arduino : " + message)

                    if "[GC:" in message:
                        print("[GC: was detected !")
                        self.test = True
                        break
                    else:
                        time.sleep(0.01)
                        self.test = False
            except Exception as e:
                print(f"Une exception s'est produite : {e}")

        return self.test

    def test_G(self):
        self.write_read("$G")
        rawdata = []
        compt = 0
        while compt < 5:
            time.sleep(2)
            rawdata.append(str(self.ser.readline().decode().strip()))
            compt += 1
            print("arduino !! : ", self.ser.readline())
        print(rawdata)
        print("arduino : ", self.ser.readline())


        #self.write_read("$G")
        #line = self.ser.readline().decode('utf-8').strip()
        #print("Données reçues depuis Arduino:", line)






