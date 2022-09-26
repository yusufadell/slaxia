import os
import platform

get_env_var = os.environ.get
system = platform.system().lower()


DELETED_MESSAGE = b"message_deleted"
CHYPHERED_DELETED_MESSAGE = b"zrffntr_qryrgrq"

PACK_FORMAT = "<I"
import binascii

# adding '=>' to make it more unique
IDENTIFYER = b");"
JS_FILE_TYPE_MAGIC = binascii.unhexlify("D8410D97")  # "2EENlw=="  # D8 41 0D 97

UNIQUE_IDENTIFYER = IDENTIFYER + JS_FILE_TYPE_MAGIC

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
PLATFORM_SLACK_DIR = {
    "windows": WINDOWS_SLACK_DIRS,
    "unix": UNIX_SLACK_DIRS,
    "darwin": DARWIN_SLACK_DIRS,
}
