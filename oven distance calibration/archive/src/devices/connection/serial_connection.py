from .abstract_connection import Connection
import serial
import serial.tools.list_ports
import time

BAUDRATES = [9600, 19200, 38400, 57600, 115200]

class SerialClient(Connection):
    def __init__(self, serial_port='COM3', baudrate=9600, timeout=1, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE):
        super().__init__()
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.serial = None
        
        self._isConnected = False

    def open(self):
        try:
            self.serial = serial.Serial(port=self.serial_port, baudrate=self.baudrate, timeout=self.timeout,
                                        bytesize=self.bytesize, stopbits=self.stopbits)
            #self.serial.open()
            self._isConnected = self.serial.isOpen()
            print('Connected? ' + str(self._isConnected))
        except Exception as e:
            print(str(e))

    def close(self):
        try:
            if self.serial:
                self.serial.close()
            self._isConnected = False
        except Exception as e:
            print("Error occurred while closing the connection: " + str(e))

    def sendCommand(self, command):
        if not self.serial:
            print('Connect to device!')
            return 'Error in serial function sendCommand'
            
        response = ''
        try:
            self.serial.reset_input_buffer()
            self.serial.write(bytes(command, encoding='ascii'))
            time.sleep(0.5)
            response_bytes = self.serial.read_all()
            response = response_bytes.decode('ascii')
        except Exception as e:
            print("Error occurred while sending command: " + str(e))
        return response
           

    @staticmethod
    def get_ports():
        ports = []
        serial_ports = serial.tools.list_ports.comports()
        for port in serial_ports:
            ports.append(str(port).split(' ')[0])
        return ports
