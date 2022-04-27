from skimage import io
from matplotlib import pyplot as plt

# Showing image to the user
def showImage(image_path):
    io.imshow(image_path)
    plt.show()