from PIL import Image
import numpy as np

class FileHandler:

    def load_image(self, path):
        img = Image.open(path)

        mode = img.mode  # RGB, RGBA, L
        format = img.format or "PNG"

        arr = np.array(img)

        return arr, mode, format

    def save_image(self, data, path, mode, format):
        img = Image.fromarray(data.astype('uint8'), mode=mode)
        img.save(path, format=format)