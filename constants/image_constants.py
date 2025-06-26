#contants/image_constants.py
import os
from constants.global_constants import GUIPath
from utils.helpers_paths import get_resource_path

# Background
menu = 'menu.png'
MOON_FRAME = 'moonFrame.png'
MOON_FEEDBACK =  'moon.jpg'
MOON_RELATE =  'moonRelate.png'
PLAYFUL_BACKGROUND = os.path.join(GUIPath, 'Background', 'oralnita.png')

#btn global
BUBBLE_STATIC = get_resource_path(GUIPath, 'bubble.png')
BTN_RECORD = get_resource_path(GUIPath, 'btnRec/img (0).png')
BTN_RECORD_HOVERED = get_resource_path(GUIPath, 'btnRec/img (22).png')
ORALNITA = get_resource_path(GUIPath, "Oralnita/oralnita86.png")





# UNIT SCENE  load inside the ui_shared
btn_syllable =  'btn_syllable.png'
btn_phoneme =  'btn_phoneme.png'
btn_oralnita =  'btn_oralnita.png'
btn_back_path =  'btn_back.png'
btn_menu_path = 'btn_menu.png'
btn_next_path = 'btn_next.png'
btn_scan_hand = 'btn_scan_hand.png'
btn_scan_face = 'btn_scan_face.png'



# btn GS1
yes_idle = get_resource_path(GUIPath, "btnYes/img (0).png")
no_idle = get_resource_path(GUIPath, "btnNo/img (0).png")

# btn GS4
micro_idle = os.path.join(GUIPath, "Micro", "img (0).png")

# btn GS5
CLOUD_EXPLOSION_STATIC = os.path.join(GUIPath, "Explosions", "img (0).png")
DARKER_CLOUD = os.path.join(GUIPath, "Cloud", "darker_cloud_2.png")
friends = os.path.join(GUIPath, "Friends", "img (0).png")



