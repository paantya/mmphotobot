from enum import Enum


class ChatState(Enum):
    FREE = '/cancel'
    SETTING_HEADING = '/set_heading'
    SETTING_SUBHEADING = '/set_subheading'
    SETTING_OPACITY = '/set_opacity'
    SPECIFYING_PARAMETER_NAME = '/set_admin_parameter'
    SETTING_PARAMETER_VALUE = 'setting_parameter_value'
    ENTERING_NEWSLETTER_MESSAGE = '/make_newsletter'
    CONFIRMING_NEWSLETTER = 'confirming_newsletter'


class ChatData:
    chat_id = 0
    heading = 'Heading'
    subheading = 'Subheading'
    opacity = 0.6
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

    def set_opacity(self, chat_id, value):
        self.get_chat_data_from_cache(chat_id).opacity = value
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

    def get_opacity(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).opacity

    def get_cached_message(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).cached_message

    def get_state(self, chat_id):
        return self.get_chat_data_from_cache(chat_id).state
