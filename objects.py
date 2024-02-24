from PIL import Image
import requests
from io import BytesIO

def resize_thumbnail(thumbnailURL):
    try:
        response = requests.get(thumbnailURL)
        response.raise_for_status()
        
        # Open the image using Pillow
        img = Image.open(BytesIO(response.content))
        
        # Resize the image to 4000x4000 pixels
        resized_img = img.resize((4000, 4000))
    
        resized_img.save(f"images/thumbnail.png")
        return f"images/thumbnail.png"

    except Exception as e:
        print(f"Error resizing thumbnail: {e}")
        return None

class SongMetadata:
    def __init__(self, title, artist, thumbnailURL, duration):
        self.title = title
        self.artist = artist
        self.thumbnailURL = resize_thumbnail(thumbnailURL)
        self.duration = duration