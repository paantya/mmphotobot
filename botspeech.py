# -*- coding: utf-8 -*-

from botcommands import *

START_MESSAGE_TEXT = 'Hello. To make an image type "/" and select a parameter you want to specify. ' \
                     'After specifying parameters send or choose a background picture to get the result.'
CANCEL_MESSAGE_TEXT = '👌'
UP_MESSAGE_TEXT = 'I am up 🌚'
EXCEPTION_MESSAGE_TEXT = '‼️ Exception has been thrown'
START_MESSAGE_ADMIN_TEXT = "Set mailing list: /" + SET_MAILING_LIST_COMMAND \
                           + "\nMake a newsletter: /" + SEND_NEWSLETTER_COMMAND
SEND_ME_PHOTO_PARAMETER_TEXT = 'Ok. Send it to me, please'
OPACITY_CLARIFICATION_TEXT = ". Remember, this parameter represents an intensity of darkening layer, " \
                             "so it should be a float from 0 to 1 ☝️ Optimal values are from 0.5 to 1 "
WAIT_FOR_AN_IMAGE_MESSAGE_TEXT = "One moment... ⏳"
DOLORES_KEY_PHRASE = 'I\'m trying, but I don\'t understand 😔 Type /start to get instructions'
OPACITY_VALIDATION_FAIL_MESSAGE_TEXT = 'Sorry, opacity should be a float number from 0 to 1.  Please, try again 🌚'
DONE_MESSAGE_TEXT = 'Done ☑️'
CHOOSE_BACKGROUND_IMAGE_TEXT = 'To get the result you can choose a background image from stock images below. ' \
                               'You also can send me your own image.'
