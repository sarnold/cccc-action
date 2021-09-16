import os
import subprocess as sp

from shlex import quote
from pathlib import Path

__version__ = '0.2'

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
CURRENT_BRANCH = GITHUB_HEAD_REF or GITHUB_REF.rsplit('/', 1)[-1]
TARGET_BRANCH = os.environ.get('INPUT_TARGET_BRANCH', CURRENT_BRANCH)
PULL_REQUEST_BRANCH = os.environ.get('INPUT_PULL_REQUEST_BRANCH', GITHUB_BASE_REF)
BRANCH = PULL_REQUEST_BRANCH if GITHUB_EVENT_NAME == 'pull_request' else TARGET_BRANCH

GITHUB_ACTOR = os.environ['GITHUB_ACTOR']
GITHUB_REPOSITORY_OWNER = os.environ['GITHUB_REPOSITORY_OWNER']
GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']
GITHUB_WORKSPACE = os.environ['GITHUB_WORKSPACE']

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

if FILE_EXTENSIONS == []:
    FILE_EXTENSIONS = LC_EXTENSIONS + UC_EXTENSIONS

LANGUAGE = os.environ.get('INPUT_LANGUAGE', "")
SOURCE_DIRS = os.environ.get('INPUT_SOURCE_DIRS', GITHUB_WORKSPACE).split()
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

    print('Output directory: {}'.format(OUTPUT_DIR))
    print('File extensions: {}'.format(file_exts))
    print('Source directories: {}'.format(source_dirs))
    print('Source language: {}'.format(LANGUAGE))

    for srcdir in source_dirs:
        files = [f for ext in file_exts
                 for f in Path(srcdir).glob('**/*{}'.format(ext))]
        src_files += files

    print('Source files: {}'.format(src_files))

    file_arg = ""
    for fname in src_files:
        file_arg = file_arg + " " + str(fname)

    command = command + "{}".format(file_arg)
    print('Full command line: {}'.format(command))


def run_cccc():
    sp.run(quote(command), shell=True, check=True)


# def rm_unused_rpt():
# """
# We need to remove unused output format.
# """
# file_ext=".xml"
# if REPORT_TYPE == "xml":
    # file_ext = ".html"


def commit_changes():
    """Commits changes.
    """
    set_email = 'git config --local user.email "cccc-action@main"'
    set_user = 'git config --local user.name "cccc-action"'

    sp.call(quote(set_email), shell=True)
    sp.call(quote(set_user), shell=True)

    print('Target branch: {}'.format(TARGET_BRANCH))
    print('Target repository: {}'.format(TARGET_REPOSITORY))

    git_checkout = f'git checkout {TARGET_BRANCH}'
    git_add = f'git add {OUTPUT_DIR}'
    git_commit = 'git commit -m "cccc report added"'
    if not DO_COMMIT:
        git_commit = 'git commit --dry-run -m "commit report, dry-run only"'
    print(f'Committing {OUTPUT_DIR}')

    sp.call(git_checkout, shell=False)
    sp.call(git_add, shell=False)
    sp.call(quote(git_commit), shell=True)


def push_changes():
    """Pushes commit.
    """
    set_url = f'git remote set-url origin https://x-access-token:{GITHUB_TOKEN}@github.com/{TARGET_REPOSITORY}'
    git_push = f'git push origin {TARGET_BRANCH}'
    sp.call(set_url, shell=False)
    sp.call(git_push, shell=False)


def main():

    if (GITHUB_EVENT_NAME == 'pull_request') and (GITHUB_ACTOR != GITHUB_REPOSITORY_OWNER):
        return

    prepare_command()
    run_cccc()
    commit_changes()
    push_changes()


if __name__ == '__main__':
    main()
