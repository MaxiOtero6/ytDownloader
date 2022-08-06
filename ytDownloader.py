import re
import pytube
import os
import shutil
import subprocess
import time
from pathlib import Path

YOUTUBE_STREAM_AUDIO_WEBM = "251"
DOWNLOAD_DIRECTORY = str(Path.home() / "Downloads") + "\\yt_downloads"
WEBM_DIR = DOWNLOAD_DIRECTORY + "\\webm_downloads"
MP3_DIR = DOWNLOAD_DIRECTORY + "\\mp3_downloads"
MP4_DIR = DOWNLOAD_DIRECTORY + "\\mp4_downloads"

def clear() -> None:
    '''
    Clean the console
    '''
    #Windows
    if os.name == 'nt':
        os.system('cls')   
    #Linux/Mac
    else:
        os.system('clear')

def menu() -> int:
    """
    Print menu and return which action the user wants to do
    """
    clear()
    print("""Hi, we have these options:

-----------------MP3 OPTIONS-----------------

1 - Download all videos in a playlist
2 - Download single video

-----------------MP4 OPTIONS-----------------

3 - Download all videos in a playlist
4 - Download single video

----------------OTHER OPTIONS----------------
5 - Exit

""")

    action: str = ''
    while (not action.isnumeric() and action not in ['1','2','3','4']):
        action = input('Which action do you want to do?: ')

    action = int(action)
    return action


def filename_filter(filename: str) -> str:
    filename_filtered: str = filename
    filename_filtered = filename_filtered.replace("á","a")
    filename_filtered = filename_filtered.replace("é","e")
    filename_filtered = filename_filtered.replace("í","i")
    filename_filtered = filename_filtered.replace("ó","o")
    filename_filtered = filename_filtered.replace("ú","u")
    filename_filtered = filename_filtered.replace("ü","u")
    
    os.rename(WEBM_DIR + "\\" +  filename, WEBM_DIR + "\\" + filename_filtered)
    return filename_filtered


def ffmpeg_webm_to_mp3(mp3_dir_var: str) -> None:
    
    files: list = os.listdir(WEBM_DIR)
    for file_webm in files:
        try:
            file_webm = filename_filter(file_webm)
            mp3_file: str = (mp3_dir_var + f"\\{file_webm}").replace("webm", "mp3")

            subprocess.call(f"ffmpeg -i \"{WEBM_DIR}\\{file_webm}\" -vn -ab 128k -ar 44100 -y \"{mp3_file}\"", shell=True)
        except:
            print(f"An error has occurred when trying to convert {file_webm} into mp3")

def download_playlist_mp3(playlist_url: str) -> None:
    """
    Download all videos in a playlist in .mp3
    """
    
    clear()
    print("""



-------------------------- Downloading... --------------------------



    """)
    try:
        playlist = pytube.Playlist(playlist_url)

        #Empty playlist.videos list fix
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        #Downloading audio tracks in .webm
        for video in playlist.videos:
            audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO_WEBM)
            
            audioStream.download(output_path=WEBM_DIR)
            
        i: int = 1
        while os.path.isdir(MP3_DIR + f'\\{i}'):
            i += 1
            mp3_dir_var: str = MP3_DIR + f'\\{i}'
        
        os.system(f"mkdir {mp3_dir_var}")
        ffmpeg_webm_to_mp3(mp3_dir_var)

        shutil.rmtree(WEBM_DIR)
        clear()
        print(f"""



-------------------------- Finished --------------------------
-------------------> See downloads folder <-------------------
>> {DOWNLOAD_DIRECTORY}
""")
        time.sleep(3)
    except:
        clear()
        print("You must input a valid playlist url")
        p_url: str = input("Input playlist url (or 0 to exit): ")
        if p_url != '0':
            download_playlist_mp3(p_url)
        else:
            return None
            

def download_video_mp3(video_url: str) -> None:
    """
    Download all videos in a playlist in .mp3
    """
    
    clear()
    print("""



-------------------------- Downloading... --------------------------



    """)  
    try:
        yt = pytube.YouTube(url=video_url)
        video = yt.streams.get_by_itag(YOUTUBE_STREAM_AUDIO_WEBM)
        video.download(output_path=WEBM_DIR)

        i: int = 1
        while os.path.isdir(MP3_DIR + f"\\{i}"):
            i += 1
        mp3_dir_var: str = MP3_DIR + f"\\{i}"
        os.system(f"mkdir {mp3_dir_var}")
    
        ffmpeg_webm_to_mp3(mp3_dir_var)
    
        shutil.rmtree(WEBM_DIR)
        clear()
        print(f"""



-------------------------- Finished --------------------------
-------------------> See downloads folder <-------------------
>> {DOWNLOAD_DIRECTORY}
""")    
        time.sleep(3)
    except:
        clear()
        print("You must input a valid video url")
        v_url: str = input("Input video url (or 0 to exit): ")
        if v_url != '0':
            download_video_mp3(v_url)
        else:
            return None

def download_video_mp4(video_url: str) -> None:
    """
    Download a simple video in .mp4
    """
    
    clear()
    print("""



-------------------------- Downloading... --------------------------



""")
    try:
        yt = pytube.YouTube(video_url).streams.get_highest_resolution()
        i: int = 1
        while os.path.isdir(MP4_DIR + f"\\{i}"):
            i += 1
        mp4_dir_var: str = MP4_DIR + f"\\{i}"
        yt.download(output_path=mp4_dir_var)
        
        clear()

        print(f"""



-------------------------- Finished --------------------------
-------------------> See downloads folder <-------------------
>> {DOWNLOAD_DIRECTORY}
""")   
        time.sleep(3)
    except:
        clear()
        print("You must input a valid video url")
        v_url: str = input("Input video url (or 0 to exit): ")
        if v_url != '0':
            download_video_mp4(v_url)
        else:
            return None

def download_playlist_mp4(playlist_url: str) -> None:
    """
    Download all videos in a playlist in .mp3
    """
    
    clear()
    print("""



-------------------------- Downloading... --------------------------



    """)
    try:
        playlist = pytube.Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        # physically downloading the audio track
        for video in playlist.videos:
            hd_video = video.streams.get_highest_resolution()
            
            hd_video.download(output_path=MP4_DIR)
        clear()
        
        print(f"""



-------------------------- Finished --------------------------
-------------------> See downloads folder <-------------------
>> {DOWNLOAD_DIRECTORY}
""")
        time.sleep(3)
    except:
        clear()
        print("You must input a valid playlist url")
        p_url: str = input("Input playlist url (or 0 to exit): ")
        if p_url != '0':
            download_playlist_mp4(p_url)
        else:
            return None

def main() -> None:
    action: int = 0
    while action != 5:
        action = menu()
        match action:
            case 1:
                playlist_url: str = input("Input playlist url: ")
                download_playlist_mp3(playlist_url)
            case 2:
                video_url: str = input("Input video url: ")
                download_video_mp3(video_url)
            case 3:
                playlist_url: str = input("Input playlist url: ")
                download_playlist_mp4(playlist_url)
            case 4:
                video_url: str = input("Input video url: ")
                download_video_mp4(video_url)

main()
