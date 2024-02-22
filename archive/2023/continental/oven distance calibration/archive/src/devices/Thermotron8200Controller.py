import sys
# sys.path.append("..")
import time

# import connection
from connection.TCPClient import TCPClient 
# print(dir(connection))

ThermotronCommandset = {
    "PauseOven": ['HOLD'],
    "ResumeOven": ['RESM'],
    "StartOven": ['RUNM'],
    "StopOven": ['STOP'],
    "SetRampRate": ['MRMP', 'channel', 'value'], 
    "RequestRampRate": ['MRMP?', 'channel'],
    "SetTemperatureSetpoint": ['SETP', 'channel', 'setpoint'],
    "RequestTemperatureSetpoint": ['SETP?', 'channel',],
    "RequestOvenStatus": ['STAT?'],
    "RequestTemperature": ['PVAR?', 'channel'],
    "RequestDeviation": ['DEVN?', 'channel',],
    "SetDeviation": ['DEVN', 'channel', 'value']
}

class Thermotron8200Controller:
    
    
    def __init__(self, ip: str = '10.0.0.100', port: int = 8888):
        self.commands = ThermotronCommandset
        self.terminatorPrefix = ''
        self.terminatorSuffix = '\n'
        self._client = TCPClient(ip, port)
        self._client.open()
        
    def __del__(self):
        self._client.close()

    def formatCommand(self, function, **args):
        cmd = self.commands.get(function)
        assert cmd is not None, f'{function} is an invalid or unimplemented function'
        parameters = cmd[1:]
        formatted_parameters = ''
        # itterate required parameters
        for parameter in parameters:
            assert parameter in args, f'Missing parameter: {parameter}'
            formatted_parameters += str(args[parameter]) + ','
        # remove right trailing (rstrip) comma if exists
        try: 
            formatted_parameters = formatted_parameters.rstrip(',')
        except Exception:
            pass
        # re-format for query: '?' comes at end of query command
        if cmd[0][-1] == '?':
            return cmd[0][:-1] + formatted_parameters + '?'
        else:
            return cmd[0] + formatted_parameters

    def sendCommand(self, command):
        full_command = self.terminatorPrefix + command + self.terminatorSuffix
        response = self._client.sendCommand(full_command)
        return response

    def pause(self):
        function = 'PauseOven'
        args = {}
        command = self.formatCommand(function, **args)
        response = self.sendCommand(command)
        return response

    def resume(self):
        function = 'ResumeOven'
        args = {}
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response

    def start(self):
        function = 'StartOven'
        args = {}
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response

    def stop(self):
        function = 'StopOven'
        args = {}
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response
  
    def set_temperature(self, temperature):
        function = 'SetTemperatureSetpoint'
        args = {
            'channel': 3,
            'setpoint': temperature
            }
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response
    
    def status(self):
        function = 'RequestOvenStatus'
        args = {}
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response

    def current_temperature(self):
        function = 'RequestTemperature'
        args = {'channel':1}
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response
    
    def current_set_temperature(self):
        function = 'RequestTemperatureSetpoint'
        args = {'channel':1}
        command = self.formatCommand(function, **args)  
        response = self.sendCommand(command)
        return response
  

def main():
    controller = Thermotron8200Controller()
    # print("status:", controller.status())
    # print("start:", controller.start())
    # print("status:", controller.status())
    # # time.sleep(3)
    # try:
    #     inp = input("type a temp ")
    controller.set_temperature(30)
    #     print("set temp",inp)
    # except Exception:
    #     print("not valid input")
    #     pass
    time.sleep(.1)
    # controller.start()
    # controller.stop()
    print("curr set temp",controller.current_set_temperature())
    # print("curr temp",controller.current_temperature())
    # time.sleep(3)
    # print("pause:", controller.pause())
    # print("status:", controller.status())
    # time.sleep(3)
    # print("stop:", controller.stop())
    # time.sleep(3)

if __name__ == "__main__":
    main()
