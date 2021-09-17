import os

from pathlib import Path

# default values
CURRENT_BRANCH = 'phony'
TARGET_BRANCH = os.environ.get('INPUT_TARGET_BRANCH', CURRENT_BRANCH)

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

    print(f'Target branch: {TARGET_BRANCH}')


if __name__ == '__main__':
    prepare_command()
