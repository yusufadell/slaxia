"""Main module."""

from consts import PLATFORM_SLACK_DIR, system
from utils import _handle_dir_content, dispatch_slackpath, patch_file


def main():
    # /////////////////////////////////|
    slack_dirs = dispatch_slackpath(system, PLATFORM_SLACK_DIR[system])
    # /////////////////////////////////|
    files = _handle_dir_content(slack_dirs)
    for f in files:
        try:
            patch_file(f)
        except Exception as e:
            continue


if __name__ == "__main__":
    main()
    print("[-] Done! restart Slack")
