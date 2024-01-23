# Yeasily
<div style="text-align:center;">
    <img src="images/cover.png" alt="cover image" width="400" height="400">
</div>
    <br>
Yeasily is a CLI utility to effortlessly manage and enhance audio files by intelligently populating metadata. Yeasily enhances the aesthetics and completeness of your digital music library, 

## Features
- **Metadata Enhancement**: Automatically populate metadata, including title, artist, thumbnail image, duration, album cover, and lyrics.
- **Playlist Mode** [-p]: Download all MP3 files from URLs listed in a file.
- **File Mode**: Download MP3 file from a single URL.

Yeasily simplifies the process of downloading and organizing MP3 files from (YouTube) URLs, providing a seamless experience for audio enthusiasts. By enriching MP3 files with comprehensive metadata, including album covers, song information, and lyrics, Yeasily strives to create a listening experience that mirrors popular streaming platforms.

## Requirements
- Python 3.x
- Dependencies: pytube, eyed3, Pillow, ffmpeg

## Installation
1. Clone this repository:
    ```
    git clone https://github.com/ShishirAravindan/yeasily.git
    ```
2. Navigate to the directory:
    ```
    cd yeasily
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
## [Optional] Formalizing the script into a CLI-utility
You could directly use the functionality as a python script or do the following work to convert it to a CLI-utility.
1. Add a Shebang Line
    At the beginning of your `main.py` script, add a shebang line to specify the path to the local Python interpreter. For example:
    ```
    #!/usr/bin/env python3
    ```
2. Make the Script Executable:
    Give execute permissions to your `main.py` script using the chmod command.
    ```
    chmod +x main.py
    ```
3. Create a symbolic link & give execute permissions
    ```
    ln -s main.py yeasily
    chmod +x yeasily
    ```
4. Add to PATH

## Usage
- File Mode
    ```
    yeasily [URL]
    ```
- Playlist mode
    ```
    yeasily -p [FILE.txt]
    ```