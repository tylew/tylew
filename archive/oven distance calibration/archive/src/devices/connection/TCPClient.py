from .abstract_connection import Connection

import socket
import logger


class TCPClient(Connection):
    def __init__(self, ip, port):
        super().__init__()
        self.ip: str = ip
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self):
        print("Connecting via TCP...")
        try:
            self.socket.connect((self.ip, self.port))
            self._isConnected = True
            print("Connected via TCP!")
        except Exception as e:
            logger.exception("Error in TCP Open Connection: " + str(e))

    def close(self):
        try:
            self.socket.close()
            self._isConnected = False
        except Exception as e:
            logger.exception("Error in TCP Close Connection: " + str(e))

    def sendCommand(self, command):
        response: str = ''
        try:
            self.socket.send(bytes(('%s' % command), 'ascii'))
            response = str(self.socket.recv(1024), 'ascii')
        except Exception as e:
            logger.exception("Error in TCP Send Command: " + str(e))
            self.close()
        return response
