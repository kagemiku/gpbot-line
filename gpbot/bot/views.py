from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    SourceUser,
    TextMessage,
    StickerMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    LocationMessage,
)

import os
import json
import requests
from .router import Router
from .reply_generator import ReplyGenerator
from .event_processor import (
    text_message_event_processor as tmep,
)

CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)
reply_generator = ReplyGenerator(line_bot_api)


router = Router(
    reply_generator,
    [
        tmep.DefaultTextMessageEventProcessor(),
    ]
)

def callback(request):
    if settings.DEBUG:
        reply = ''
        request_json = json.loads(request.body.decode('utf-8'))
        for e in request_json['events']:
            reply_token = e['replyToken']
            message_type = e['message']['type']
            source_user = SourceUser(user_id=e['source']['userId'])
            if message_type == 'text':
                text = e['message']['text']
                timestamp = e['timestamp']
                text_message = TextMessage(text=text)
                message_event = MessageEvent(timestamp=timestamp, source=source_user, message=text_message)
                router.relay(message_event)

        return HttpResponse()
    else:
        if request.method == 'POST':
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            print('signature: ', signature)
            body = request.body.decode('utf-8')

            try:
                events = parser.parse(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()
            except LineBotApiError:
                return HttpResponseBadRequest()

            for event in events:
                router.relay(event)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

