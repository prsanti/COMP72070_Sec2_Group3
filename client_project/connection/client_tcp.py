import socket
from .packet import Packet
from .types import Type, Category
import base64
from PIL import Image, ImageTk
import io
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TCPClient:
    def __init__(self, host='127.0.0.1', port=27000):
        self.host = host
        self.port = port
        self.client_id = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def send(self, packet):
        if self.socket:
            try:
                self.socket.send(packet.serialize())
                return True
            except Exception as e:
                print(f"Send failed: {e}")
                return False
        return False

    def send_game_move(self, game_id, position):
        logger.debug(f"Sending game move: {position}")
        if isinstance(position, dict) and position.get('request_type') == 'result_image':
            # For image requests, use IMG type
            packet = Packet(Type.IMG, Category.GAME, position)
        else:
            # For regular game moves
            packet = Packet(Type.GAME, Category.MOVE, {
                'game_id': game_id,
                'position': position
            })
        self.send(packet)

    def receive_game_result_image(self, base64_image):
        logger.debug("Attempting to process received image data")
        try:
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            logger.debug("Successfully processed image")
            return photo
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return None

    def handle_game_update(self, data):
        logger.debug(f"Received game update: {data}")
        if isinstance(data, dict):
            if data.get('type') == 'result_image':
                logger.debug("Received result image update")
                image_data = data.get('image_data')
                if hasattr(self, 'current_game') and self.current_game:
                    self.current_game.display_result_image(image_data)
            # ... existing handle_game_update code ... 