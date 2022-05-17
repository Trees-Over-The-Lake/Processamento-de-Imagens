import menu
import PySimpleGUI as sg
from models import keys

from PIL import Image, ImageTk

window = sg.Window('Tela de teste', layout=menu.layout_tela, size=(800,500))

while True:
    event, values = window.Read()
    
    if event == sg.WIN_CLOSED:
        break
    
    elif event == keys.ABRIR_PASTA_BIRRAD_KEY:
        img_preview = Image.open('../assets/logo-puc-minas.png').resize((384,384))
        photo_img = ImageTk.PhotoImage(img_preview)
        window[keys.TAB_USER_SELECTED_IMAGE_KEY].update(data=photo_img)
        
        img_preview2 = Image.open('../assets/sample_preview_image.png').resize((384,384))
        photo_img2 = ImageTk.PhotoImage(img_preview2)
        window[keys.TAB_PREVIEW_IMAGE_KEY].update(data=photo_img2)
    
        
window.close()