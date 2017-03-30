from linebot.models import Event, MessageEvent
from .reply_generator import ReplyGenerator
from .event_processor import event_processor, message_event_processor

class Router():
    def __init__(self, reply_generator, message_event_processors):
        self.__reply_generator = reply_generator
        self.__message_event_processors = message_event_processors

    def relay(self, event):
        if isinstance(event, MessageEvent):
            self.relay_message_event(event)
        else:
            print('event: ', event, 'is not MessageEvent')

    def relay_message_event(self, event):
        for mep in self.__message_event_processors:
            if mep.can_process(event):
                mep.process(event, self.__reply_generator)
                break

