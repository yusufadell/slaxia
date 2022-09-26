import os
import platform

get_env_var = os.environ.get
system = platform.system().lower()


DELETED_MESSAGE = b"message_deleted"
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
    "Library/Containers/com.tinyspeck.slackmacgap/Data/Library/Application Support/Slack",
    "Library/Application Support/Slack/Service Worker/CacheStorage",
]
