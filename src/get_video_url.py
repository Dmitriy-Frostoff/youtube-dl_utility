def get_video_url() -> str:
  '''
  Get the video URL for downloading

  Returns:
    str: the URL of the video from the user's input
  Raises:
    ValueError: If the input is empty or incorrect
  '''

  print('Enter URL of the video for downloading: ')
  video_url: str = input('URL: ').strip()

  if not video_url:
    raise ValueError('Empty or incorrect input')

  return video_url
