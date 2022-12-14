import binascii
import struct
from pathlib import Path

from consts import (
    CHYPHERED_DELETED_MESSAGE,
    DELETED_MESSAGE,
    IDENTIFYER,
    JS_FILE_TYPE_MAGIC,
    PACK_FORMAT,
    UNIQUE_IDENTIFYER,
    get_env_var,
)


def dispatch_slackpath(
    system,
    slack_dirs,
):

    full_app_path = application_path(system)
    paths = [Path(full_app_path) / slack_dir for slack_dir in slack_dirs]
    _ = lambda: paths
    _handle_nonexists_dirs(paths)

    print(f"=> Searching for Slack dir cache storage: {paths[0]}\n")
    return {
        "windows": _,
        "linux": _,
        "macOS": _,
        "darwin": _,
    }.get(system, _handle_nonexists_dirs(paths))()


def application_path(system):
    return get_env_var("APPDATA") if system == "windows" else get_env_var("HOME")


def _handle_nonexists_dirs(slack_absolute_paths):
    if not is_valid_paths(slack_absolute_paths):
        raise PathDoesNotExists(
            f"Given Slack paths doesn't exists: {slack_absolute_paths} \
            >>> Try to install Slack first!"
        )


def is_valid_paths(paths, path=None):
    if path:
        is_valid_path()
    _valild = [path.exists() for path in paths]
    return any(_valild)


def is_valid_path(path):
    return path.exists()


class PathDoesNotExists(Exception):
    pass


def _handle_dir_content(slack_dirs):
    print(f"[-] Searching for JS code cache files")
    dir_content = get_dir_content(slack_dirs)
    files = filer_files(dir_content)
    return files


def get_dir_content(slack_dirs):
    dir_content = []
    for slack_dir in slack_dirs:
        dir_content += slack_dir.glob("**/*")
    return dir_content


def filer_files(dir_content):
    return [f for f in dir_content if f.is_file()]


def is_empty_dir(paths: Path):
    # for path in path:
    #     if path.
    ...


def patch_file(file):
    cached_static_file_data = b""
    js_compiled_response = file.read_bytes()
    # Check if file needs to be patched
    if is_deteled_message(js_compiled_response):
        print(f"[-] Patching file: {file}")
        # Build cache file
        cached_static_file_data += _handle_file_patching(js_compiled_response)
        # Write the patched file
        return file.write_bytes(cached_static_file_data)
    return "User Didn't Delete any messages YET!"


def is_deteled_message(js_compiled_response):
    return DELETED_MESSAGE in js_compiled_response


def _handle_file_patching(js_compiled_response):
    print(f"[-] Patching file: {js_compiled_response}")
    (
        js_compiled_response,
        cache_file_header,
        cache_file_metadata_and_request,
    ) = identify_header_metadata(js_compiled_response)
    patched_static_file_deleted_message_ignored, updated_CRC = recalculate_CRC(
        js_compiled_response
    )
    final_static_file = (
        cache_file_header,
        patched_static_file_deleted_message_ignored,
        JS_FILE_TYPE_MAGIC,
        cache_file_metadata_and_request[:8],
        updated_CRC,
        cache_file_metadata_and_request[12:],
    )
    return final_static_file


def identify_header_metadata(js_compiled_response):
    # Code Cache File: header, js file path, js data, magic type?, js data size, js crc, request
    offset_js_data_start_index = get_start_index_offset(js_compiled_response)
    cache_file_header = js_compiled_response[:offset_js_data_start_index]
    (
        cache_file_header_and_data,
        cache_file_metadata_and_request,
    ) = extract_header_metadata(js_compiled_response)

    js_compiled_response = insert_identifyer(
        offset_js_data_start_index, cache_file_header_and_data
    )

    return js_compiled_response, cache_file_header, cache_file_metadata_and_request


def insert_identifyer(offset_js_data_start_index, cache_file_header_and_data):
    return cache_file_header_and_data[offset_js_data_start_index:] + IDENTIFYER


def get_start_index_offset(js_compiled_response):
    offset_js_data_start_index = (
        struct.unpack(PACK_FORMAT, js_compiled_response[12:16])[0] + 24
    )
    return offset_js_data_start_index


def extract_header_metadata(js_compiled_response):
    (
        cache_file_header_and_data,
        cache_file_metadata_and_request,
    ) = js_compiled_response.split(UNIQUE_IDENTIFYER)
    return cache_file_header_and_data, cache_file_metadata_and_request


def recalculate_CRC(js_compiled_response):
    # replace deleted_message parameter so it be ignored by js script
    patched_static_file_deleted_message_ignored = ignore_deleted_message_parameter(
        js_compiled_response
    )
    # re-calculate the CRC32 for patched static js file
    updated_CRC = crc(patched_static_file_deleted_message_ignored)
    return patched_static_file_deleted_message_ignored, updated_CRC


def ignore_deleted_message_parameter(js_compiled_response):
    return js_compiled_response.replace(DELETED_MESSAGE, CHYPHERED_DELETED_MESSAGE)


def crc(data):
    # converts a variable-length string into an 8-character string that is a text representation of the hexadecimal value of a 32 bit-binary sequence.
    crc = binascii.crc32(data)
    return struct.pack(PACK_FORMAT, crc)
