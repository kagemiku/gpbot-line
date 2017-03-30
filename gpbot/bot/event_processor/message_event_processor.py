from linebot.models import MessageEvent
from .event_processor import EventProcessor

class MessageEventProcessor(EventProcessor):
    def can_process(self, event):
        return event.type == 'message'

    def process(self, event, rg):
        pass

