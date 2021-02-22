import os

from pathlib import Path

# default values
LC_EXTENSIONS = [
    ".c", ".c++", ".cc", ".cpp", ".cxx",
    ".h", ".h++", ".hh", ".hpp", ".hxx",
    ".j", ".jav", ".java",
]

UC_EXTENSIONS = [ext.upper() for ext in LC_EXTENSIONS]

# command related inputs
DO_COMMIT = os.environ.get('INPUT_COMMIT_REPORT', False)
FILE_EXTENSIONS = os.environ.get('INPUT_FILE_EXTENSIONS', None)
if not FILE_EXTENSIONS:
    FILE_EXTENSIONS = LC_EXTENSIONS + UC_EXTENSIONS
SOURCE_DIR = os.environ.get('INPUT_SOURCE_DIR', '.')
OUTPUT_DIR = os.environ.get('INPUT_OUTPUT_DIR', 'metrics')
REPORT_TYPE = os.environ.get('INPUT_REPORT_TYPE', 'html')

command = ""


def prepare_command():
    global command
    command = command + "cccc "
    command = command + "--outdir=" + OUTPUT_DIR
    source_dir = SOURCE_DIR

    file_exts = FILE_EXTENSIONS
    print(file_exts)
    src_files = [f for ext in file_exts
                 for f in Path(source_dir).glob('**/*{}'.format(ext))]

    print(src_files)

    file_arg = ""
    for fname in src_files:
        file_arg = file_arg + " " + str(fname)

    print(file_arg)


if __name__ == '__main__':
    prepare_command()
