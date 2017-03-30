# -*- coding: utf-8 -*-
from linebot.models import MessageEvent, TextMessage
from .message_event_processor import MessageEventProcessor

class TextMessageEventProcessor(MessageEventProcessor):
    def can_process(self, event):
        if not super().can_process(event):
            return False

        return event.message.type == 'text'

    def process(self, event, rg):
        pass


class DefaultTextMessageEventProcessor(TextMessageEventProcessor):
    def can_process(self, event):
        if not super().can_process(event):
            return False

        return True

    def process(self, event, rg):
        reply_text = 'test'
        rg.reply_text(event.reply_token, reply_text)
        print(reply_text)

