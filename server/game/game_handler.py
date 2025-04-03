import os
import base64
import logging
from connection.packet import Packet
from connection.types import Type, Category

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GameHandler:
    def __init__(self):
        self.image_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        logger.debug(f"Image directory path: {self.image_dir}")

    def handle_game_move(self, client, data):
        logger.debug(f"Received game move data: {data}")
        
        if isinstance(data, dict):
            if data.get('request_type') == 'result_image':
                # Map result types to actual image filenames
                image_map = {
                    'win': 'youWin.jpg',
                    'lose': 'youLose.jpg',
                    'draw': 'youTie.jpg'
                }
                
                result_type = data.get('result')
                image_filename = image_map.get(result_type)
                if not image_filename:
                    logger.error(f"Invalid result type: {result_type}")
                    return
                    
                image_path = os.path.join(self.image_dir, image_filename)
                logger.debug(f"Attempting to load image: {image_path}")
                
                if os.path.exists(image_path):
                    try:
                        with open(image_path, 'rb') as image_file:
                            image_data = image_file.read()
                            base64_image = base64.b64encode(image_data).decode('utf-8')
                            logger.debug("Successfully loaded and encoded image")
                            
                            # Create and send response packet
                            response_data = {
                                'type': 'result_image',
                                'image_data': base64_image
                            }
                            response_packet = Packet(Type.IMG, Category.GAME, response_data)
                            client.send(response_packet.serialize())
                            logger.debug("Sent image response packet")
                    except Exception as e:
                        logger.error(f"Error processing image: {e}")
                else:
                    logger.error(f"Image file not found: {image_path}") 