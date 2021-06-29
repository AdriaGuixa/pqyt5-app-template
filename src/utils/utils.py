"""
Class implemented to have some useful functions generically used by other objects

:author: Adria Guixa

:since: YYYY-MM-DD
"""
import sys
import os
import enum
import re


class ReportType(enum.Enum):
    FPT = 0
    FPT_Reduced = 1
    K02 = 2
    K02_Reduced = 3
    K06 = 4
    MergeTool = 5


def get_temperature_from_name(file_name):
    """
    Given a file name, get the temperature if it is present in the name (..._temp1_temp2...).
    Args:
        file_name (str): file name
    Returns:
        temperature (list): list of two strings with file temperatures [temp_amb, temp_cool]
    """
    try:
        basename = os.path.basename(file_name)
        temperature = re.findall('-?[0-9]+', re.findall('_-?[0-9]+_-?[0-9]+', basename)[0])
    except IndexError:
        temperature = []
    return temperature


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS,
        # and places our data files in a folder relative to that temp
        # folder named as specified in the datas tuple in the spec file
        base_path = sys._MEIPASS
    except Exception:
        # sys._MEIPASS is not defined, so use the original path
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


def logging_errors(method):
    """
    Decorator function to log any exception raised by the decorated function
    Args:
        method (function): function decorated
    Raises:
        raised_exception: exception raised by decorated function if any
    Returns:
        any: return of the decorated function
    """
    def _wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as raised_exception:
            self.logger.error(
                "Problem during the execution of {method}".format(method=method.__name__))
            template = 'An exception of type {0} occurred. Arguments: {1!r}'
            self.logger.error(template.format(type(raised_exception).__name__, raised_exception.args))

            raise raised_exception
    return _wrapper
