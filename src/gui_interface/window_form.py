"""
GUI Interface for the element embedded in the main form.

:author: Adria Guixa

:since: YYYY-MM-DD
"""
import logging
from PyQt5 import uic

from src.utils.utils import resource_path

form = resource_path('src/gui_interface/ui/window_form.ui')
Ui_Form, QtBaseClass = uic.loadUiType(form)


class WindowForm(QtBaseClass, Ui_Form):
    """
    Main interface object called by main method.
    """

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.logger = logging.getLogger(__name__)
        self.logger.info('{} is set'.format(__name__))

        self._step = 0
        self.progress_bar.setValue(self._step)

    def set_progress_bar_maximum(self, value):
        """
        Sets the maximum value to the progress bar.
        Args:
            value (int): limit for the progress bar
        """
        self.progress_bar.setMaximum(value)
