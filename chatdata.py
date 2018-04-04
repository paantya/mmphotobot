# -*- coding: utf-8 -*-

from enum import Enum
from botcommands import *


class ChatState(Enum):
    FREE = '/cancel'
    SETTING_HEADING = "/" + SET_HEADING_COMMAND
    SETTING_SUBHEADING = "/" + SET_SUBHEADING_COMMAND
    SETTING_BLACKOUT = "/" + SET_BLACKOUT_COMMAND
    SETTING_BLUR = "/" + SET_BLUR_COMMAND
    SPECIFYING_MAILING_LIST = "/" + SET_MAILING_LIST_COMMAND
    ENTERING_NEWSLETTER_MESSAGE = "/" + SEND_NEWSLETTER_COMMAND
    CONFIRMING_NEWSLETTER = 'confirming_newsletter'


class ChatData:
    chat_id = 0
    heading = 'Heading'
    subheading = 'Subheading'
    blackout = 0.3
    blur = 5
    cached_message = None
    state = ChatState.FREE

    def __init__(self, chat_id):
        self.chat_id = chat_id
        pass


class ChatCache:
    cache = {}

    def __init__(self):
        self.cache = {}
        pass

    def get_chat_data_from_cache(self, chat_id):
        if chat_id not in self.cache.keys():
            self.cache[chat_id] = ChatData(chat_id)
        return self.cache.get(chat_id)

    def set_heading(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).heading = value
        pass

    def set_subheading(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).subheading = value
        pass

    def set_blackout(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).blackout = value
        pass

    def set_blur(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).blur = value
        pass

    def set_cached_message(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).cached_message = value
        pass

    def set_state(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).state = value
        pass

    def get_heading(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).heading

    def get_subheading(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).subheading

    def get_blackout(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).blackout

    def get_blur(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).blur

    def get_cached_message(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).cached_message

    def get_state(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).state
