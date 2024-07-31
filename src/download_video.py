import subprocess

from typing import List, NoReturn

def download_video(video_url: str, config_path: str) -> NoReturn:
  """
  Download video using yt-dlp lib with specified configuration

  Args:
    video_url (str) - video url for donwloading
    config_path (str) - path to the yt-dlp lib config (*.conf)

  Raises:
    subprocess.CalledProcessError: If the yt-dlp command fails
  """

  # download command
  download_command: List[str] = [
    'yt-dlp',
    '--config-location', config_path,
    '--verbose',
    video_url
  ]

  #command execution
  try:
    subprocess.run(download_command, check=True)
  except subprocess.CalledProcessError as error:
    raise RuntimeError(f'yt-dlp command failed with error: {error}')
