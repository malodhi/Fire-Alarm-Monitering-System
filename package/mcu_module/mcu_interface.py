import time
import serial

class McuInterface(object):

    def __init__(self):
        print("\nConnecting to MCU ...")
        self.port_handler = None
        self._establish_communication()
        time.sleep(2)
        self.port_handler.reset_input_buffer()
        print("Successfully Connected to MCU.")
        
    def _establish_communication(self):
        ## note: the below ports can change everytime the arduino is connected.
        try:
            self.port_handler = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
            print("MCU Conencted to Port: /dev/ttyUSB0 .")
        except:
            try:
                self.port_handler = serial.Serial('/dev/ttyUSB1', 9600, timeout=1.0)
                print("MCU Conencted to Port: /dev/ttyUSB1 .")
            except:
                print("MCU not found at any port. \nPlease connect one.")
                print("Exiting ... ")
                exit()
    
    def get_instant_data(self, wait=0.25):
        try:
            end_time = time.time() + wait
            while time.time() <= end_time:      
                if self.port_handler.in_waiting: #> 0:
                    read_data = self.port_handler.readline().decode('utf-8').rstrip()
                    if read_data:
                        return float(read_data)
            return int(-1)
        except Exception as e:
            print(e)
            print("\nWarning: Problem in communication with arduino.")
    
    def recieve_continuous_data(self):
        try:
            print("Reading mcu serial output if any ...\n")
            while True:      
                if self.port_handler.in_waiting > 0:
                    read_data = self.port_handler.readline().decode('utf-8').rstrip()
                    print(read_data)
        except Exception as e:
            ## note: if there is no serial data from arduino
            # the while-loop will continue, however, if arduino
            # is disconnected within the loop (manually or by keyboard-interrup)
            # then the if-condition, serialData.in_waiting, gives error.
            # Hence, we place the while-loop in try-except condition.
            self.port_handler.close()
            print(e)
            print("\nCommunication with mcu lost.")
            print("Closing the serial communication port.")
            print("Exiting ...")
            exit()
                     
    
if __name__== '__main__':
    mcu_handler = McuInterface()
    print(mcu_handler.get_instant_data())
