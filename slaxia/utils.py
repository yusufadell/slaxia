import sys
from pathlib import Path

from consts import (
    DARWIN_SLACK_DIRS,
    UNIX_SLACK_DIRS,
    WINDOWS_SLACK_DIRS,
    get_app_dir,
    system,
)


def dispatch_slackpath(
    system,
    slack_dirs,
):

    print("[-] Searching for Slack dir cache storage")
    paths = [Path(full_app_path) / slack_dir for slack_dir in slack_dirs]
    _ = lambda: paths

    print(f"=> Searching for Slack dir cache storage: {paths[0]}\n")
    return {
        "windows": _,
        "linux": _,
        "macOS": _,
        "darwin": _,


    full_app_dir = (
        get_app_dir("APPDATA") if system == "windows" else get_app_dir("HOME")
    )

    get_full_path = lambda: [Path(full_app_dir) / slack_dir for slack_dir in slack_dirs]
    return {
        "windows": get_full_path,
        "linux": get_full_path,
        "macOS": get_full_path,
        "darwin": get_full_path,
    }.get(system, _handle_nonexists_dirs(system))()


slack_dirs = dispatch_slackpath()


def _handle_nonexists_dirs(system):
    if not slack_dirs or all([not slack_dir.exists() for slack_dir in slack_dirs]):
        print(f"ERROR: Unsupported system: {system}")
        sys.exit(1)
