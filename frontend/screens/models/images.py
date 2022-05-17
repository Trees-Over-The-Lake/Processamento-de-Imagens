# Arquivo para carregar as imagens do modelo
import PIL

class ImagemModel:
    def __init__(self) -> None:
        self.image_size = (384, 384) # 3 * tamanho da imagem no disco
    
    # Desenhar imagem na tela
    def get_preview_image(self, image: PIL.Image, window, window_key):
        # Aumentando imagem para encaixar no canvas
        preview_img = PIL.ImageTk.PhotoImage(image.resize(self.image_size))
        window[window_key].update(data=preview_img)