from PIL import Image
import requests
from io import BytesIO
from pytube import YouTube
from whisper import Whisper
import cv2
import numpy as np

class SongMetadata:
    def __init__(self, title, artist, thumbnailURL, duration):
        self.title = title
        self.artist = artist
        self.thumbnailURL = thumbnailURL
        self.duration = duration

def _download_youtube_thumbnail(url):
    yt = YouTube(url)
    thumbnail_url = yt.thumbnail_url
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None
    
def _calculate_energy_map(image):
    """Computes the energy map of an image."""
    # Apply a Sobel operator in both the x and y directions
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1)

    # Compute the gradient magnitude (energy map)
    energy_map = np.sqrt(grad_x**2 + grad_y**2).astype(np.uint8)
    return energy_map

def _find_vertical_seam(energy_map):
    """Finds the vertical seam in an energy map."""
    m, n = energy_map.shape
    seams = np.zeros((m,))

    for i in range(m):
        min_value = np.inf
        index = 0

        # Find the minimum value in each row
        for j in range(n):
            if energy_map[i, j] < min_value:
                min_value = energy_map[i, j]
                index = j + 1

        seams[i] = index - 1
    return seams

def _remove_seam(image, seam, is_vertical=True):
    """Removes a seam from an image."""
    m, n = image.shape
    # Create a copy of the original image
    new_image = np.copy(image)

    for i in range(m):
        if is_vertical:
            j = int(seam[i])
            new_image[i, j:] = new_image[i, j+1:]

        else:
            i_new = n - int(seam[i]) - 1
            new_image[i_new:, i] = new_image[i_new+1:, i]
    return new_image

def seam_carving(thumbnail, targetSize):
    gray = cv2.cvtColor(thumbnail, cv2.COLOR_RGB2GRAY)

    max_reduction = min(targetSize[0], targetSize[1])

    for _ in range(max_reduction):
        energy_map = _calculate_energy_map(gray)
        vertical_seam = _find_vertical_seam(energy_map)

        # Remove the selected seam from the image
        gray = _remove_seam(gray, vertical_seam)

        # If we've reached the target height, break out of the loop
        if max_reduction - _ <= targetSize[0]:
            break

def extractAndResizeThumbnail(youtube_url, targetSize):
    thumbnail = _download_youtube_thumbnail(youtube_url)
    return seam_carving(thumbnail, targetSize)

def getLyrics(filePath:str):
    model = Whisper()
    try:
        return model.generate_text_from_audio(f"music/{filePath}.mp3")
    except Exception as e:
        print(f"ERROR: Generating lyrics with Whisper model. {e}")