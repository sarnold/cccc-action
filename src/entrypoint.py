import os
import subprocess as sp

from shlex import split
from pathlib import Path

__version__ = '0.3'

GITHUB_EVENT_NAME = os.environ['GITHUB_EVENT_NAME']

# Set repository
CURRENT_REPOSITORY = os.environ.get('GITHUB_REPOSITORY', '')
# TODO: How about PRs from forks?
TARGET_REPO = os.environ.get('INPUT_TARGET_REPOSITORY', '')
TARGET_REPOSITORY = TARGET_REPO if TARGET_REPO != '' else CURRENT_REPOSITORY
PULL_REQUEST_REPOSITORY = os.environ.get('INPUT_PULL_REQUEST_REPOSITORY', TARGET_REPOSITORY)
REPOSITORY = PULL_REQUEST_REPOSITORY if GITHUB_EVENT_NAME == 'pull_request' else TARGET_REPOSITORY

# Set branches
GITHUB_REF = os.environ['GITHUB_REF']
GITHUB_HEAD_REF = os.environ['GITHUB_HEAD_REF']
GITHUB_BASE_REF = os.environ['GITHUB_BASE_REF']
CURRENT_BRANCH = GITHUB_HEAD_REF if GITHUB_HEAD_REF != '' else GITHUB_REF.rsplit('/', 1)[-1]
TARGET_BRANCH = os.environ.get('INPUT_TARGET_BRANCH', '')
PULL_REQUEST_BRANCH = os.environ.get('INPUT_PULL_REQUEST_BRANCH', GITHUB_BASE_REF)
BRANCH = PULL_REQUEST_BRANCH if GITHUB_EVENT_NAME == 'pull_request' else TARGET_BRANCH

# Branch vars (eg, BRANCH, TARGET_BRANCH) can be empty if no cfg branch
CAN_COMMIT = True if TARGET_BRANCH != '' else False

GITHUB_ACTOR = os.environ['GITHUB_ACTOR']
GITHUB_REPOSITORY_OWNER = os.environ['GITHUB_REPOSITORY_OWNER']
GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']

# default values
LC_EXTENSIONS = [
    ".c", ".c++", ".cc", ".cpp", ".cxx",
    ".h", ".h++", ".hh", ".hpp", ".hxx",
    ".j", ".jav", ".java",
]

UC_EXTENSIONS = [ext.upper() for ext in LC_EXTENSIONS]

# command related inputs
DO_COMMIT = os.environ.get('INPUT_COMMIT_REPORT', False)
FILE_EXTENSIONS = os.environ.get('INPUT_FILE_EXTENSIONS', "").split()
SOURCE_DIRS = os.environ.get('INPUT_SOURCE_DIRS', "").split()

if FILE_EXTENSIONS == []:
    FILE_EXTENSIONS = LC_EXTENSIONS + UC_EXTENSIONS

if SOURCE_DIRS == []:
    SOURCE_DIRS = ["."]

LANGUAGE = os.environ.get('INPUT_LANGUAGE', "")
OUTPUT_DIR = os.environ.get('INPUT_OUTPUT_DIR', 'metrics')
REPORT_TYPE = os.environ.get('INPUT_REPORT_TYPE', 'html')

command = ""


def prepare_command():
    global command
    command = command + "cccc"
    command = command + " --outdir=" + OUTPUT_DIR
    if LANGUAGE != "":
        command = command + " --lang=" + LANGUAGE
    source_dirs = SOURCE_DIRS
    file_exts = FILE_EXTENSIONS
    src_files = []

    print(f'File extensions: {file_exts}')
    print(f'Source directories: {source_dirs}')
    print(f'Source language: {LANGUAGE}')

    for srcdir in source_dirs:
        files = [f for ext in file_exts
                 for f in Path(srcdir).glob(f'**/*{ext}')]
        src_files += files

    print(f'Source files: {src_files}')
    print(f'Output directory: {OUTPUT_DIR}')

    file_arg = ""
    for fname in src_files:
        file_arg = file_arg + " " + str(fname)

    command = command + "{}".format(file_arg)
    print(f'Full command line string: {command}')
    print(f'Full command line list: {split(command)}')
    print(f'Can we commit the report: {CAN_COMMIT}')


def run_cccc():
    sp.check_call(split(command))


def commit_changes():
    """Commits changes.
    """
    set_email = 'git config --local user.email "cccc-action@main"'
    set_user = 'git config --local user.name "cccc-action"'

    sp.check_call(split(set_email))
    sp.check_call(split(set_user))

    print(f'Base ref var: {GITHUB_BASE_REF}')
    print(f'PR branch var: {BRANCH}')
    print(f'Current branch: {CURRENT_BRANCH}')
    print(f'Target branch: {TARGET_BRANCH}')
    print(f'Target repository: {TARGET_REPOSITORY}')

    git_checkout = f'git checkout {TARGET_BRANCH}'
    git_add = f'git add {OUTPUT_DIR}'
    git_commit = 'git commit -m "cccc report added"'
    if not DO_COMMIT:
        git_commit = 'git commit --dry-run -m "commit report, dry-run only"'
    print(f'Committing {OUTPUT_DIR}')

    sp.check_call(split(git_checkout))
    sp.check_call(split(git_add))
    sp.check_call(split(git_commit))


def push_changes():
    """Pushes commit.
    """
    set_url = f'git remote set-url origin https://x-access-token:{GITHUB_TOKEN}@github.com/{TARGET_REPOSITORY}'
    git_push = f'git push origin {TARGET_BRANCH}'
    sp.check_call(split(set_url))
    sp.check_call(split(git_push))


def main():

    prepare_command()
    run_cccc()
    if CAN_COMMIT:
        commit_changes()
        push_changes()


if __name__ == '__main__':
    main()
