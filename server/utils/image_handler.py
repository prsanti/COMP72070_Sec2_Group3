import base64
import os

class ImageHandler:
    def __init__(self):
        self.image_paths = {
            'win': 'images/win.jpg',
            'lose': 'images/lose.jpg',
            'draw': 'images/draw.jpg'
        }

    def get_image_data(self, result):
        try:
            image_path = self.image_paths.get(result)
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"Error loading image: {e}")
        return None 