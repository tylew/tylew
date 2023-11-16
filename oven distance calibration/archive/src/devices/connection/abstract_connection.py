from abc import ABC, abstractmethod

class Connection(ABC):
    def __init__(self):
        super().__init__()
        self._isConnected = False

    @property
    def isConnected(self):
        return self._isConnected

    @abstractmethod
    def open(self, **kwargs):
        pass

    @abstractmethod
    def close(self, **kwargs):
        pass

    @abstractmethod
    def sendCommand(self, command):
        pass
