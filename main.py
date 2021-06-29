"""
Main function of the eMOB Tooling Report Generator

:author: Adria Guixa

:since: YYYY-MM-DD
"""
import sys
import logging
from datetime import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.gui_interface import gui_interface
from src.utils import utils


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(message)s",
        handlers=[
            # logging.FileHandler(log_name),
            logging.StreamHandler()
        ])

    logger = logging.getLogger()
    # p arsed_args, unparsed_args = process_cl_args()
    # QApplication expects the first argument to be the program name.
    # qt_args = sys.argv[:1] + unparsed_args
    # app = QApplication(qt_args)
    application = QApplication(sys.argv)
    # ... the rest of your handling: `sys.exit(app.exec_())`, etc.
    application.setWindowIcon(QIcon(utils.resource_path('support/KennyMcCormick.png')))
    win = gui_interface.GuiInterface()
    win.set_logger(logger)
    win.show()
    sys.exit(application.exec_())
