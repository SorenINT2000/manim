from __future__ import annotations

import subprocess
import threading
import platform

from manimlib.utils.directories import get_sound_dir
from manimlib.utils.file_ops import find_file


def get_full_sound_file_path(sound_file_name: str) -> str:
    """
    Returns the full path to a sound file.
    """
    return find_file(
        sound_file_name,
        directories=[get_sound_dir()],
        extensions=[".wav", ".mp3", ""]
    )


def play_sound(sound_file):
    """
    Play a sound file using the system's audio player in a new thread.
    """
    def play_sound_thread(sound_file):
        full_path = get_full_sound_file_path(sound_file)
        system = platform.system()

        if system == "Windows":
            # Windows
            subprocess.Popen(
                ["powershell", "-c", f"(New-Object Media.SoundPlayer '{full_path}').PlaySync()"],
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        elif system == "Darwin":
            # macOS
            subprocess.Popen(
                ["afplay", full_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                ["aplay", full_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    
    thread = threading.Thread(target=play_sound_thread, args=(sound_file,))
    thread.start()
