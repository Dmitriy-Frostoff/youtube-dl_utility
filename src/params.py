import os

# current file dirname
current_dir = os.path.dirname(__file__)

# virtual environment activation script path
virtual_env_act_path: str = os.path.join(current_dir, "..", "env", "Scripts", "activate.bat")

#yt-dlp config location (*.conf)
yt_dlp_config = os.path.join(current_dir, '..', 'configs', 'yt-dlp', 'yt-dlp.conf')
