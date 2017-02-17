from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import requests

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN
}

def reply_text(reply_token, text):
    reply = text
    payload = {
        'replyToken': reply_token,
        'message': [
            {
                'type': 'text',
                'text': reply,
            },
        ]
    }

    result = requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    print('result: ', result)
    return reply

def callback(request):
    reply = ''
    request_json = json.loads(request.body.decode('utf-8'))
    for e in request_json['events']:
        reply_token = e['replyToken']
        print('replyToken: ', reply_token)
        message_type = e['message']['type']

        if message_type == 'text':
            text = e['message']['text']
            reply += reply_text(reply_token, text)

    return HttpResponse(reply)

