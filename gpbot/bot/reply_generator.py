from django.conf import settings
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
)

class ReplyGenerator():
    def __init__(self, line_bot_api):
        self.__line_bot_api = line_bot_api
        self.__history = []
        self.__recent_user_ids = []

    def reply_text(self, reply_token, text):
        if not settings.DEBUG:
            result = self.__line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=text)
            )
            print('result: ', result)

    def reply_sticker(self, reply_token, package_id, sticker_id):
        if not settings.DEBUG:
            result = self.__line_bot_api.reply_message(
                reply_token,
                StickerSendMessage(package_id=package_id, sticker_id=sticker_id)
            )
            print('result: ', result)

