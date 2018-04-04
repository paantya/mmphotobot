# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw, ImageFilter

MM_LOGO_FILE_PATH = 'images/mm-white-logo.png'
DARKENING_LAYER_COLOR = '#1a2535'
MAIN_FONT_FILE_PATH = 'fonts/OpenSans-Regular.ttf'


# Originally by https://github.com/kuparez at https://github.com/kuparez/studsovet_scripts
def gen_image(heading, subheading, image, blackout, blur):
    image = image.resize((1920, 1080), Image.ANTIALIAS)
    image = image.filter(ImageFilter.GaussianBlur(blur))
    blackout = int(255 * blackout)
    grey_img = Image.new(mode='RGBA', size=(1920, 1080), color=DARKENING_LAYER_COLOR)
    grey_img.putalpha(blackout)
    mask = Image.new('RGBA', (1920, 1080), (0, 0, 0, blackout))
    image.paste(grey_img, mask)
    logo = Image.open(MM_LOGO_FILE_PATH)
    image.paste(logo, (150, 323), logo)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(MAIN_FONT_FILE_PATH, 115)
    draw.multiline_text((120, 650), heading, (255, 255, 255), font=font)
    font = ImageFont.truetype(MAIN_FONT_FILE_PATH, 73)

    if '\n' not in heading:
        draw.multiline_text((120, 800), subheading, (255, 255, 255), font=font)
    else:
        draw.multiline_text((120, 900), subheading, (255, 255, 255), font=font)

    return image
