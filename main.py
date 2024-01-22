#!/Users/shishiraravindan/Documents/coding/yeasily/.musicVenv/bin/python

from pytube import YouTube
from objects import SongMetadata
import subprocess
import eyed3
import urllib.request
from PIL import Image
from io import BytesIO
import argparse

def main():
    args = parse_args()
    if args.mode == "playlist":
        print("PLAYLIST MODE")
        with open(args.source, 'r') as f:
            for line in f:
                print(f"ADDING {line}")
                addSongToLibrary(line)
    else:
        print("FILE MODE")
        addSongToLibrary(args.source)

def addSongToLibrary(URL: str):
    metadata = extractSongMetadata(URL)
    print("metadata extracted.")
    downloadMP4(URL)
    print("MP4 downloaded.")
    convertToMP3(metadata)
    print("MP3 downloaded.")
    setMetadata(metadata)
    print("Metadata Updated.")


def extractSongMetadata(URL:str) -> SongMetadata:
    YouTubeVideo = YouTube(URL)
    metadata = SongMetadata(YouTubeVideo.title, YouTubeVideo.author, 
                            YouTubeVideo.thumbnail_url, YouTubeVideo.length)
    metadata.title = metadata.title.replace('/', ' ')
    return metadata

def downloadMP4(URL):
    YouTubeVideo = YouTube(URL)
    try:
        YouTubeVideo.streams.filter(progressive=True, 
                                    file_extension='mp4').first().download(output_path='raw/', filename='1.mp4')
    except:
        print("ERROR: Could not dowload MP4")

def convertToMP3(metadata:SongMetadata):
    command = [
        "ffmpeg",
        "-i", f"raw/1.mp4",
        "-vn",
        "-sn",
        "-c:a", "mp3",
        "-ab", "192k",
        "-f", "mp3",
        f"music/{metadata.title}.mp3"
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Converted to MP3: {metadata.title}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")

def setMetadata(metadata:SongMetadata):
    
    try:
        audio = eyed3.load(f"music/{metadata.title}.mp3")
    except:
        print("ERROR: Loading mp3 file.")
        return

    audio.tag.title, audio.tag.artist  = metadata.title, metadata.artist
    
    response = urllib.request.urlopen(f"{metadata.thumbnailURL}")
    imagedata = response.read()

    audio.tag.images.set(3, imagedata, "image/jpeg", u"cover")
    
    audio.tag.save()
    

def parse_args():
    parser = argparse.ArgumentParser(description="CLI utility to download MP3 file")
    
    parser.add_argument("source", metavar="SOURCE FILE/URL", help="File name for playlist mode or URL for file mode")

    # Mode-specific arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--playlist", dest="mode", action="store_const", const="playlist", 
                       help="mode to download all MP3 from URLs in file")
    return parser.parse_args()


if __name__ == "__main__":
    main()