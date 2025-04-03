from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(text, filename, size=(800, 600), color=(255, 255, 255)):
    # Create a new image with a solid color background
    image = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(image)
    
    # Add some text
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Center the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_position = ((size[0] - text_bbox[2]) // 2, (size[1] - text_bbox[3]) // 2)
    
    # Draw the text
    draw.text(text_position, text, fill=(0, 0, 0), font=font)
    
    # Save the image
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', filename)
    image.save(image_path, quality=95)
    print(f"Created {filename}")

def main():
    # Create images directory if it doesn't exist
    images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Create test images
    create_test_image("YOU WIN!", "win.jpg", color=(144, 238, 144))  # Light green
    create_test_image("YOU LOSE!", "lose.jpg", color=(255, 182, 193))  # Light red
    create_test_image("IT'S A DRAW!", "draw.jpg", color=(173, 216, 230))  # Light blue

if __name__ == "__main__":
    main() 