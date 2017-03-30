from abc import ABCMeta, abstractmethod

class EventProcessor(metaclass=ABCMeta):
    @abstractmethod
    def can_process(self, event):
        pass

    @abstractmethod
    def process(self, event, rg):
        pass

