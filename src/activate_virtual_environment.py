import os
import subprocess

from typing import NoReturn

def activate_virtual_environment(env_path: str) -> NoReturn:
  """
  Activate the virtual environment

  Args:
    env_path (str) - path to virtual environment activation script.

  Raises:
    FileNotFoundError: if the activation script doesn't exist.
  """

  if not os.path.exists(env_path):
    raise FileNotFoundError(f"Virtual environment activation file not found at {env_path}")

  subprocess.call(env_path, shell=True)
