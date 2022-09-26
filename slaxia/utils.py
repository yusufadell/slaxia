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
