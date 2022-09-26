import os
import platform

get_app_dir = os.environ.get
system = platform.system().lower()


MESSAGE_DELETED = "message_deleted"
MESSAGE_DELETED_REP = b"zrffntr_qryrgrq"


import binascii

JS_FILE_TYPE_MAGIC = binascii.unhexlify("D8410D97")  # D8 41 0D 97


WINDOWS_SLACK_DIRS = [
    "Slack",
]
UNIX_SLACK_DIRS = [
    ".config/Slack/Service Worker/CacheStorage",
]

DARWIN_SLACK_DIRS = [
    "Containers/com.tinyspeck.slackmacgap/Data/Library/Application Support/Slack",
    "Application Support/Slack/Service Worker/CacheStorage",
]
