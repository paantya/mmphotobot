# -*- coding: utf-8 -*-
import telebot
import os
import logging
import re
from PIL import Image
from datetime import datetime
from telebot import types
from io import BytesIO

from chatdata import ChatState
from mmphoto import gen_image
from botutil import image_to_file, get_dolores_emoji
from chatdata import ChatCache

TOKEN = os.environ.get('PHOTOBOT_TOKEN')
ADMIN_ID = int(os.environ.get('PHOTOBOT_ADMIN_ID'))

MAKE_NEWSLETTER_COMMAND = 'make_newsletter'
SET_ADMIN_PARAMETER_COMMAND = 'set_admin_parameter'
MAILING_LIST_PARAMETER_KEY = 'mailing_list'

START_MESSAGE_TEXT = 'Hello. To make an image type "/" and select a parameter you want to specify. ' \
                     'After specifying parameters send or choose a background picture to get the result.'
CANCEL_MESSAGE_TEXT = '👌'
UP_MESSAGE_TEXT = 'I am up 🌚'
EXCEPTION_MESSAGE_TEXT = '‼️ Exception has been thrown. Go to logs for more info️'
START_MESSAGE_ADMIN_TEXT = "Set admin parameter: /" + SET_ADMIN_PARAMETER_COMMAND\
                           + "\nMake a newsletter: /" + MAKE_NEWSLETTER_COMMAND\
                           + "\n\nMailing list parameter name: " + MAILING_LIST_PARAMETER_KEY
SEND_ME_PHOTO_PARAMETER_TEXT = 'Ok. Send it to me, please'
OPACITY_CLARIFICATION_TEXT = " Remember, this parameter represents an intensity of darkening layer, " \
                             "so it should be a float from 0 to 1 ☝️ Optimal values are from 0.5 to 1 "
WAIT_FOR_AN_IMAGE_MESSAGE_TEXT = "One moment... ⏳"
DOLORES_KEY_PHRASE = 'I\'m trying, but I don\'t understand 😔 Type /start to get instructions'
OPACITY_VALIDATION_FAIL_MESSAGE_TEXT = 'Sorry, opacity should be a float number from 0 to 1.  Please, try again 🌚'
DONE_MESSAGE_TEXT = 'Done ☑️'

STOCK_IMAGES_DIRECTORY = 'images/stock/'
SENT_IMAGE_FILE_NAME = 'image.jpg'

ALL_CONTENT_TYPES = ["text",
                     "audio",
                     "document",
                     "photo",
                     "sticker",
                     "video",
                     "video_note",
                     "voice",
                     "location",
                     "contact",
                     "new_chat_members",
                     "left_chat_member",
                     "new_chat_title",
                     "new_chat_photo",
                     "delete_chat_photo",
                     "group_chat_created",
                     "supergroup_chat_created",
                     "channel_chat_created",
                     "migrate_to_chat_id",
                     "migrate_from_chat_id",
                     "pinned_message"]

telebot.logger.setLevel(logging.DEBUG)

# A cache for chat data.
cache = ChatCache()

# A cache for some photobot parameters
parameters = {MAILING_LIST_PARAMETER_KEY: ''}

# Start the bot.
bot = telebot.TeleBot(TOKEN)

# Read stock images names, make a keyboard
stock_photo_names = []
imageSelect = types.ReplyKeyboardMarkup()
for d, dirs, files in os.walk(os.getcwd() + '/' + STOCK_IMAGES_DIRECTORY):
    for f in files:
        stock_photo_names.append(f)
        imageSelect.add(f)


def debug_message_processing(message):
    chat_id = message.chat.id

    if chat_id == ADMIN_ID:
        if (len(message.text) > 11) and (message.text[:1] == '$'):
            array = message.text[2:].split()
            if len(array) > 1:
                id_of_chat_where_to_send = array[0]
                text = message.text[2 + len(id_of_chat_where_to_send) + 1:]
                bot.send_message(id_of_chat_where_to_send, text)
                bot.send_message(chat_id, "MESSAGE SENT")
    else:
        bot.send_message(ADMIN_ID, "MESSAGE FROM " + str(message.chat.first_name) + " @" + str(
            message.chat.username) + " " + str(chat_id) + "\n\n" + str(message.text))


def handle_free_text(message):
    if message.text in stock_photo_names:
        build_and_send_image(message, Image.open(STOCK_IMAGES_DIRECTORY + message.text).convert('RGB'))
    else:
        bot.send_message(message.chat.id, DOLORES_KEY_PHRASE)

        debug_message_processing(message)


def reply_done(chat_id):
    bot.send_message(chat_id, DONE_MESSAGE_TEXT, reply_markup=imageSelect)


def set_heading(message):
    chat_id = message.chat.id

    cache.set_heading(chat_id, message.text)
    cache.set_state(chat_id, ChatState.FREE)

    reply_done(chat_id)


def set_subheading(message):
    chat_id = message.chat.id

    cache.set_subheading(chat_id, message.text)
    cache.set_state(chat_id, ChatState.FREE)

    reply_done(chat_id)


def validate_opacity(opacity):
    return re.match("[01^\d+?\.\d+?$]", opacity) is not None


def set_opacity(message):
    chat_id = message.chat.id
    opacity = message.text

    if validate_opacity(opacity):
        cache.set_opacity(chat_id, float(opacity))
        cache.set_state(chat_id, ChatState.FREE)

        reply_done(message.chat.id)
    else:
        bot.send_message(chat_id, OPACITY_VALIDATION_FAIL_MESSAGE_TEXT)


def specify_param_name(message):
    chat_id = message.chat.id

    if message.text in parameters.keys():
        cache.set_cached_message(chat_id, message)
        cache.set_state(chat_id, ChatState.SETTING_PARAMETER_VALUE)
        bot.send_message(chat_id, "VALUE:")
    else:
        bot.send_message(chat_id, "WRONG PARAMETER NAME. TRY AGAIN")


def set_param_value(message):
    chat_id = message.chat.id
    param_name = cache.get_cached_message(chat_id).text

    parameters[param_name] = message.text
    cache.set_state(chat_id, ChatState.FREE)
    bot.send_message(chat_id, "VALUE OF \"" + param_name + "\": \n\n" + str(parameters[param_name]))


def enter_newsletter_message(message):
    chat_id = message.chat.id

    cache.set_cached_message(chat_id, message)
    bot.send_message(chat_id, "YOUR MESSAGE:")
    bot.send_message(chat_id, cache.get_cached_message(chat_id).text, parse_mode="markdown")
    bot.send_message(chat_id, "ENTER CURRENT DAY OF MONTH TO CONFIRM")
    cache.set_state(chat_id, ChatState.CONFIRMING_NEWSLETTER)


def validate_chat_id(chat_id):
    return chat_id.isdigit()


def confirm_and_make_newsletter(message):
    chat_id = message.chat.id
    message_to_send = cache.get_cached_message(chat_id).text

    if len(parameters[MAILING_LIST_PARAMETER_KEY]) > 0:
        if message.text == str(datetime.now().day):
            for chat_id_from_list in parameters[MAILING_LIST_PARAMETER_KEY].split('\n'):
                if validate_chat_id(chat_id_from_list):
                    bot.send_message(chat_id_from_list, message_to_send, parse_mode="markdown")
            bot.send_message(chat_id, 'SENT')
            cache.set_state(chat_id, ChatState.FREE)
        else:
            bot.send_message(chat_id, 'WRONG')
    else:
        print(chat_id)
        bot.send_message(chat_id, 'MAILING LIST IS EMPTY')
        cache.set_state(chat_id, ChatState.FREE)


def handle_preliminary_admin_command(chat_id, text_to_send, state_to_set):
    cache.set_state(chat_id, state_to_set)
    bot.send_message(chat_id, text_to_send, reply_markup=types.ReplyKeyboardRemove())


def handle_preliminary_command(message, text_to_send, state_to_set):
    chat_id = message.chat.id

    if chat_id != ADMIN_ID:
        handle_free_text(message)
    else:
        handle_preliminary_admin_command(chat_id, text_to_send, state_to_set)


def get_image_from_message(message):
    received_photo = message.photo
    file_id = received_photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image = Image.open(BytesIO(downloaded_file))

    return image


def build_image(chat_id, background_image):
    heading = cache.get_heading(chat_id)
    subheading = cache.get_subheading(chat_id)
    opacity = cache.get_opacity(chat_id)

    return gen_image(heading, subheading, background_image, opacity)


def send_photo_debug_info(chat, photo, date):
    chat_id = chat.id

    if chat_id != ADMIN_ID:
        first_name = chat.first_name
        last_name = chat.last_name
        username = chat.username
        caption = "PHOTO BY " + str(first_name) + " " + str(last_name) + " @" + str(username) + " " + str(chat_id) \
                  + ", " + str(datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S'))
        bot.send_photo(ADMIN_ID, image_to_file(photo, SENT_IMAGE_FILE_NAME), caption=caption)


def build_and_send_image(message, background_image):
    chat_id = message.chat.id

    wait_for_an_image_message = bot.send_message(chat_id, WAIT_FOR_AN_IMAGE_MESSAGE_TEXT)

    built_image = build_image(chat_id, background_image)

    bot.send_document(chat_id, image_to_file(built_image, SENT_IMAGE_FILE_NAME))
    bot.send_photo(chat_id, image_to_file(built_image, SENT_IMAGE_FILE_NAME))
    bot.delete_message(chat_id, wait_for_an_image_message.message_id)

    send_photo_debug_info(message.chat, built_image, message.date)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    chat_id = message.chat.id

    cache.set_state(chat_id, ChatState.FREE)
    bot.send_message(chat_id, START_MESSAGE_TEXT, reply_markup=types.ReplyKeyboardRemove())

    if chat_id == ADMIN_ID:
        bot.send_message(chat_id, START_MESSAGE_ADMIN_TEXT)


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    chat_id = message.chat.id

    cache.set_state(chat_id, ChatState.FREE)
    bot.send_message(chat_id, CANCEL_MESSAGE_TEXT, reply_markup=imageSelect)


@bot.message_handler(commands=['set_heading', 'set_subheading', 'set_opacity'])
def handle_setter(message):
    chat_id = message.chat.id

    cache.set_state(chat_id, ChatState(message.text))
    answer = SEND_ME_PHOTO_PARAMETER_TEXT
    if message.text == '/set_opacity':
        answer = answer + OPACITY_CLARIFICATION_TEXT
    bot.send_message(chat_id, answer, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=[SET_ADMIN_PARAMETER_COMMAND])
def handle_par_name_setter(message):
    handle_preliminary_command(message,
                               "EXISTING PARAMETERS: \n\n" + str(parameters.keys()) + "\n\n ENTER PARAMETER NAME",
                               ChatState.SPECIFYING_PARAMETER_NAME)


@bot.message_handler(commands=[MAKE_NEWSLETTER_COMMAND])
def handle_make_newsletter(message):
    handle_preliminary_command(message,
                               "ENTER NEWSLETTER MESSAGE",
                               ChatState.ENTERING_NEWSLETTER_MESSAGE)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    state = cache.get_state(message.chat.id)

    if state == ChatState.FREE:
        handle_free_text(message)
    elif state == ChatState.SETTING_HEADING:
        set_heading(message)
    elif state == ChatState.SETTING_SUBHEADING:
        set_subheading(message)
    elif state == ChatState.SETTING_OPACITY:
        set_opacity(message)
    elif state == ChatState.SPECIFYING_PARAMETER_NAME:
        specify_param_name(message)
    elif state == ChatState.SETTING_PARAMETER_VALUE:
        set_param_value(message)
    elif state == ChatState.ENTERING_NEWSLETTER_MESSAGE:
        enter_newsletter_message(message)
    elif state == ChatState.CONFIRMING_NEWSLETTER:
        confirm_and_make_newsletter(message)


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    received_image = get_image_from_message(message)
    build_and_send_image(message, received_image)


@bot.message_handler(content_types=ALL_CONTENT_TYPES)
def handle_any_other_message(message):
    chat_id = message.chat.id

    if chat_id == ADMIN_ID:
        if message.sticker is not None and message.text is not None \
                and len(message.text) >= 3 and message.text[:1] == '$':
            id_of_chat_where_to_send = message.text[2:].split()[0]
            bot.send_sticker(id_of_chat_where_to_send, message.sticker)
            bot.send_message(chat_id, "STICKER SENT")
    else:
        # Forward.
        message_id = message.message_id

        bot.forward_message(ADMIN_ID, chat_id, message_id)
        bot.send_message(chat_id, get_dolores_emoji())


try:
    bot.send_message(ADMIN_ID, UP_MESSAGE_TEXT)
    bot.polling(none_stop=True)
except Exception:
    bot.send_message(ADMIN_ID, EXCEPTION_MESSAGE_TEXT)
