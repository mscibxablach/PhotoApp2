import cv2
import numpy as np
import io
from PIL import Image

class ImageUtils:
    @staticmethod
    def convert_inmemory_file_to_cv2_image(inmemory_file):
        nparr = np.fromstring(inmemory_file, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return img

    @staticmethod
    def convert_cv2_image_to_bytes_io(image_array):
        img_pil = Image.fromarray(image_array)

        img_data = io.BytesIO()
        img_pil.save(img_data, format='png')

        return img_data
