"""Main module."""
import binascii
import struct
import sys

from .consts import JS_FILE_TYPE_MAGIC, MESSAGE_DELETED, MESSAGE_DELETED_REP
from .utils import slack_dirs


def crc(data):
    # The CRC32 function converts a variable-length string into an 8-character string that is a text representation of the hexadecimal value of a 32 bit-binary sequence.
    crc = binascii.crc32(data)
    return struct.pack("<I", crc)


def patch_file(file):
    cache_file_data_fixed = b""
    js_file_data = file.read_bytes()

    # Check if file needs to be patched
    if MESSAGE_DELETED in js_file_data:
        print(f"[-] Patching file: {file}")
        # Code Cache File: header, js file path, js data, magic type?, js data size, js crc, request
        offset_js_data_start_pos = struct.unpack("<I", js_file_data[12:16])[0] + 24
        cache_file_header = js_file_data[:offset_js_data_start_pos]  # 1
        # adding ');' to make it more unique
        (
            cache_file_header_and_data,
            cache_file_metadata_and_request,
        ) = js_file_data.split(b");" + JS_FILE_TYPE_MAGIC)
        js_file_data = (
            cache_file_header_and_data[offset_js_data_start_pos:] + b");"
        )  # 2
        # Replace and fix crc
        js_file_data_fixed = js_file_data.replace(MESSAGE_DELETED, MESSAGE_DELETED_REP)
        crc_calc = crc(js_file_data_fixed)
        # Build cache file
        cache_file_data_fixed = (
            cache_file_header
            + js_file_data_fixed
            + JS_FILE_TYPE_MAGIC
            + cache_file_metadata_and_request[:8]
            + crc_calc
            + cache_file_metadata_and_request[12:]
        )
        # Write the patched file
        return file.write_bytes(cache_file_data_fixed)
    return False


if __name__ == "__main__":

    print(f"[-] Searching for JS code cache files")
    dir_content = [slack_dir.glob("**/*") for slack_dir in slack_dirs]
    files = [f for f in dir_content if f.is_file()]
    for f in files:
        try:
            patch_file(f)
        except Exception as e:
            continue

    print("[-] Done! restart Slack")
