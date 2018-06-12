# -*- coding: utf-8 -*-

import random
from io import BytesIO


def image_to_file(image, name):
    bio = BytesIO()
    bio.name = name
    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio


def get_dolores_emoji():
    r = random.randint(0, 2)
    if r == 0:
        return '🤔'
    elif r == 1:
        return '👀'
    elif r == 2:
        return '👻'
