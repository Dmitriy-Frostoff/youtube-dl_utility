import subprocess
import os
import glob
import json
import re
from typing import List, Dict

def clean_filename(title: str) -> str:
  """
  Remove <>:"/\\|?* from the string

  Args:
    title (str): string with potentially incorrect symbols

  Returns:
    str: string without incorrect symbols

  Examples:
     >>> clean_filename('f<f>m:p/e\\g?*')
     ffmpeg
     >>> clean_filename('stringData')
     stringData
     >>> clean_filename('valid_filename.txt')
     valid_filename.txt
  """
  return re.sub(r'[<>:"/\\|?*]', '_', title)

# best practicies to use main as entry point of a function like in a C type languages
# also best practice for variables incapsulation
# use Docstring with Google Docs style whenever possible!
# type everything)))
def main() -> None:
  """
  Main function to download and combine video and audio from YouTube and similar site.
  User's URL of the video input is required after programm execution.

  This function downloads the best available video (1080p currently) and audio (alac) from the specified
  site URL and combines them into a single output file in the filesystem in a *.mp4 extension.

  Raises:
    ValueError: If video or audio files are not found.
  """
  try:
    # current file dirname
    current_dir = os.path.dirname(__file__)

    # url settings
    ffmpeg_path: str = os.path.join(current_dir, '..', 'libs', 'ffmpeg', 'bin', 'ffmpeg.exe')
    download_path: str = os.path.join(current_dir, '..', 'downloads')
    print('Enter URL of the video for downloading: ')
    video_url: str = input('URL: ').strip()

    if not video_url:
      raise ValueError('Empty or incorrect input')

    # activating virtual environment
    activate_env: str = os.path.join(current_dir, "..", "env", "Scripts", "activate.bat")
    subprocess.call([activate_env], shell=True)

    # get video information and save to JSON file
    info_command: List[str] = ['yt-dlp', '--dump-json', video_url]
    with open(os.path.join(current_dir, '..', 'video_info.json'), 'w', encoding='utf-8') as file:
      subprocess.run(info_command, stdout=file)

    # download command
    video_command: List[str] = [
      'yt-dlp',
      '--config-location', os.path.join(current_dir, '..', 'configs', 'yt-dlp.video.conf'),
      '--ffmpeg-location', ffmpeg_path,
      '--verbose',
      video_url
    ]

    audio_command: List[str] = [
        'yt-dlp',
        '--config-location', os.path.join(current_dir, '..', 'configs', 'yt-dlp.audio.conf'),
        '--ffmpeg-location', ffmpeg_path,
        '--verbose',
        video_url
    ]

    #command execution
    subprocess.run(video_command)
    subprocess.run(audio_command)

    # get info about audio and video files from JSON file
    info_json: Dict[str, str]
    with open(os.path.join(current_dir, '..', 'video_info.json'), encoding='utf-8') as file:
      info_json = json.load(file)

    # get the video name from json and cut it up to 10 symbols
    title: str = clean_filename(info_json['title'][:10])

    # video and audio patterns
    video_pattern: str = os.path.join(download_path, '*.mp4')
    audio_pattern: str = os.path.join(download_path, '*.m4a')

    # paths to the video and audio files
    video_files: List[str] = glob.glob(video_pattern)
    audio_files: List[str] = glob.glob(audio_pattern)

    # check that files exist
    if not video_files or not audio_files:
      raise ValueError('There\'s no video or audio')

    video_file: str = video_files[0]
    audio_file: str = audio_files[0]

    # output filename
    output_file: str = os.path.join(download_path, 'combined', 'video_combined.mp4')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    combine_command: List[str] = [
      ffmpeg_path,
      '-i', video_file,
      '-i', audio_file,
      '-c:v', 'libx264',
      '-c:a', 'aac',
      '-strict', 'experimental',
      output_file
    ]

    subprocess.run(combine_command)

    final_output_file: str = os.path.join(download_path, 'combined', f'{title}.mp4')
    os.rename(output_file, final_output_file)
  except KeyboardInterrupt:
    print('\n The programm was interrupted by User')

# if run this script personally not as a module => main()
# else None (mean run as a module in a another file)
if __name__ == '__main__':
  main()
