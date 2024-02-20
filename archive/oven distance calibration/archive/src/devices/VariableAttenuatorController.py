from connection.serial_connection import SerialClient
import time

AttenuatorCommandset = {
    "GetAttenuation": ['A?'],
    "SetAttenuation": ['A', 'attenuation'],
    "IncrementAttenuation": ['A+', 'increment'],
    "DecrementAttenuation": ['A-', 'decrement'],
    "GetSerialNumber": ['V2'],
    "GetNameAndVersion": ['V?'],
}

def main():
    # print("Testing...")

    attenuator = VariableAttenuatorController()
    attenuator.connect()
   
    print(attenuator.getInfo())
    
    attenuator.setAttenuation(15)

    print(attenuator.getAttenuation())
    attenuator.disconnect()
    


class VariableAttenuatorController:

    def __init__(self):
        self.commands = AttenuatorCommandset
        self.terminatorPrefix = ''
        self.terminatorSuffix = '\r'
        self._client = None

    def connect(self, serial_port='COM3'):
        self._client = SerialClient(serial_port=serial_port)
        self._client.open()

    def disconnect(self):
        if self._client is not None:
            self._client.close()
            self._client = None
        
    def formatCommand(self, function, **args):
        cmd = self.commands.get(function)
        assert cmd is not None, f'{function} is an invalid or unimplemented function'
        
        parameters = cmd[1:]
        formatted_parameters = ''
        # itterate required parameters
        for parameter in parameters:
            assert parameter in args, f'Missing parameter: {parameter}'
            formatted_parameters += str(args[parameter]) 
        
        command = cmd[0] + formatted_parameters
        return self.terminatorPrefix + command + self.terminatorSuffix
    
    def sendCommand(self, function, **args):
        command = self.formatCommand(function, **args)  
        # print(command)
        if self._client is not None:
            while True:
                response = self._client.sendCommand(command)
                if 'Busy' in response:
                    print('Attenuator busy, waiting 1s...')
                    time.sleep(1)  # Sleep only if the device is busy
                else:
                    break
            return response

    def getAttenuation(self):
        function = 'GetAttenuation'
        args = {}
        response = self.sendCommand(function, **args)
        return response

    def setAttenuation(self, attenuation):
        function = 'SetAttenuation'
        args = {
            'attenuation': attenuation
        }
        response = self.sendCommand(function, **args)
        return response

    def incrementAttenuation(self, increment):
        function = 'IncrementAttenuation'
        args = {
            'increment': increment
        }
        response = self.sendCommand(function, **args)
        return response
    
    def decrementAttenuation(self, decrement):
        function = 'DecrementAttenuation'
        args = {
            'decrement': decrement
        }
        response = self.sendCommand(function, **args)
        return response
    
    def getSerial(self):
        function = 'GetSerialNumber'
        args = {}
        response = self.sendCommand(function, **args)
        return response
    
    def getInfo(self):
        function = 'GetNameAndVersion'
        args = {}
        response = self.sendCommand(function, **args)
        return response

if __name__ == "__main__":
    main()