"""Main module."""
import binascii
import struct
import sys

from .consts import JS_FILE_TYPE_MAGIC, MESSAGE_DELETED, MESSAGE_DELETED_REP
from .utils import slack_dirs


    files = _handle_dir_content(slack_dirs)
    for f in files:
        try:
            patch_file(f)
        except Exception as e:
            continue

    print("[-] Done! restart Slack")
