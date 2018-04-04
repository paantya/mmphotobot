# -*- coding: utf-8 -*-

from botcommands import *

START_MESSAGE_TEXT = 'Hello. To make an image type "/" and select a parameter you want to specify. ' \
                     'After specifying parameters send or choose a background picture to get the result.'
CANCEL_MESSAGE_TEXT = '👌'
UP_MESSAGE_TEXT = 'I am up 🌚'
EXCEPTION_MESSAGE_TEXT = '‼️ Exception has been thrown'
START_MESSAGE_ADMIN_TEXT = "Set mailing list: /" + SET_MAILING_LIST_COMMAND \
                           + "\nSend a newsletter: /" + SEND_NEWSLETTER_COMMAND
SEND_ME_PHOTO_PARAMETER_TEXT = 'Ok. Send it to me, please'
HEADING_CLARIFICATION_TEXT = ''
SUBHEADING_CLARIFICATION_TEXT = ''
BLACKOUT_CLARIFICATION_TEXT = ". Remember, this parameter represents a background darkening intensity, " \
                              "it should be a float from 0 to 1 ☝️, " \
                              "where 0 means \"no darkening\", 1 — \"absolute darkness\". " \
                              "Default value has been set to 0.3"
BLUR_CLARIFICATION_TEXT = '. This parameter represents a fuzziness of the background ' \
                          'and it can be any non-negative number. The bigger number, ' \
                          'the more indistinct a background photo. Optimal values are from 0 to 15. ' \
                          'Default value has been set to 5'
WAIT_FOR_AN_IMAGE_MESSAGE_TEXT = "One moment... ⏳"
BLACKOUT_VALIDATION_FAIL_MESSAGE_TEXT = 'Sorry, blackout intensity should be a float number from 0 to 1. ' \
                                        'Please, try again 🌚'
BLUR_VALIDATION_FAIL_MESSAGE_TEXT = 'Sorry, it should be a non-negative integer.  Please, try again 🌚'
DONE_MESSAGE_TEXT = 'Done ☑️'
CHOOSE_BACKGROUND_IMAGE_TEXT = 'To get the result you can choose a background image from stock images below. ' \
                               'You can also send me your own image.'
