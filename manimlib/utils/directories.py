from __future__ import annotations

import os
import tempfile
import appdirs


from manimlib.config import manim_config
from manimlib.config import get_manim_dir
from manimlib.utils.file_ops import guarantee_existence


def get_directories() -> dict[str, str]:
    """
    Returns the directories dictionary.
    """
    return manim_config.directories


def get_cache_dir() -> str:
    """
    Returns the cache directory.
    """
    return get_directories()["cache"] or appdirs.user_cache_dir("manim")


def get_temp_dir() -> str:
    """
    Returns the temporary directory.
    """
    return get_directories()["temporary_storage"] or tempfile.gettempdir()


def get_downloads_dir() -> str:
    """
    Returns the downloads directory.
    """
    return get_directories()["downloads"] or appdirs.user_cache_dir("manim_downloads")


def get_output_dir() -> str:
    """
    Returns the output directory.
    """
    return guarantee_existence(get_directories()["output"])


def get_raster_image_dir() -> str:
    """
    Returns the raster image directory.
    """
    return get_directories()["raster_images"]


def get_vector_image_dir() -> str:
    """
    Returns the vector image directory.
    """
    return get_directories()["vector_images"]


def get_sound_dir() -> str:
    """
    Returns the sound directory.
    """
    return get_directories()["sounds"]


def get_shader_dir() -> str:
    """
    Returns the shader directory.
    """
    return os.path.join(get_manim_dir(), "manimlib", "shaders")
