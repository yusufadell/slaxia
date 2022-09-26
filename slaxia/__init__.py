"""Top-level package for slaxia."""

__author__ = """Yusuf Adel"""
__email__ = "yusufadell.dev@gmail.com"
__version__ = "0.1.0"
from slaxia.slaxia import patch_file
from slaxia.utils import _handle_file_patching, dispatch_slackpath

__all__ = [
    "patch_file",
    "_handle_file_patching",
    "dispatch_slackpath",
]
