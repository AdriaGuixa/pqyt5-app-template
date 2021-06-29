"""
Method created to update the App name and version automatically when generating the .exe

:author: Adria Guixa

:since: YYYY-MM-DD
"""

from src import __name__ as app_name
from src import __version__ as app_version

IN_FILE = 'support/grab_version.txt'
OUT_FILE = 'support/file_grab_version.txt'


REPLACE_EXPRESSIONS = {
    'app_version_1': app_version[0],
    'app_version_2': app_version[2],
    'app_version_3': app_version[4],
    'app_version': app_version,
    'app_name': app_name,
    'exe_app_name': '{}.exe'.format(app_name.replace(' ', '_'))
}


def create_grab_version_file():
    """
    """
    counter_num = 0
    with open(IN_FILE, 'r') as reader:
        lines = reader.readlines()
        for counter, line in enumerate(lines):
            for item in REPLACE_EXPRESSIONS:
                if item in line:
                    line = line.replace(item, REPLACE_EXPRESSIONS[item])
            counter_num = counter
            lines[counter_num] = line
    with open(OUT_FILE, 'w+') as writer:
        writer.writelines(lines)


if __name__ == '__main__':
    create_grab_version_file()
