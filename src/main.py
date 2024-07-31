import subprocess
import os
import glob
import json
import re

from typing import List, Dict, NoReturn

from params import current_dir, virtual_env_act_path, yt_dlp_config
from activate_virtual_environment import activate_virtual_environment
from get_video_url import get_video_url
from download_video import download_video

# best practicies to use main as entry point of a function like in a C type languages
# also best practice for variables incapsulation
# use Docstring with Google Docs style whenever possible!
# type everything)))
def main() -> NoReturn:
  """
  Main function to download and combine video and audio from YouTube and similar site.
  User's URL of the video input is required after programm execution.

  This function downloads the best available video (1080p or best below currently with highest average video bitrate (VBR)) and audio (best quality audio bitrate (ABR)) from the specified
  site URL and combines them into a single output file in the filesystem in a *.mkv extension.

  Steps:
    1. Ask the user for the URL of the video.
    2. Activate the virtual environment.
    3. Retrieve video information.
    4. Download video and audio (will be mixed automatically) or just best video (with audio already included).

  Raises:
    ValueError: If video or audio files are not found.
  """
  try:
    video_url: str = get_video_url()

    # activating virtual environment
    activate_virtual_environment(virtual_env_act_path)

    # download video
    download_video(video_url, yt_dlp_config)

  except (FileNotFoundError, RuntimeError) as error:
    print(f'An error occured: {error}')

  except KeyboardInterrupt:
    print('\n The programm was interrupted by User')

# if run this script personally not as a module => main()
# else None (mean run as a module in a another file)
if __name__ == '__main__':
  main()
