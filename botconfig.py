import os

TOKEN = os.environ.get('PHOTOBOT_TOKEN')
# -*- coding: utf-8 -*-

ADMIN_ID = int(os.environ.get('PHOTOBOT_ADMIN_ID'))

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
