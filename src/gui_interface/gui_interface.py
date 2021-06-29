"""
GUI Interface main window for sample tool template

:author: Adria Guixa

:since: YYYY-MM-DD
"""

import os
import logging
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QMessageBox, QFileDialog, QActionGroup,\
    QPushButton, QLineEdit
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from src.worker.worker import Worker
from src.utils.utils import resource_path
from src.gui_interface.window_form import WindowForm
from src.worker.timer_counter import TimerCounter
import time

from src import __name__ as app_name
from src import __version__ as app_version


form = resource_path('src/gui_interface/ui/gui_interface.ui')
Ui_MainWindow, QtBaseClass = uic.loadUiType(form)


class GuiInterface(QMainWindow, Ui_MainWindow):
    """
    Main interface object called by main method.
    """
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self._current_path = os.getcwd()
        self.logger = logging.getLogger(__name__)
        self.logging_enabled = False
        self.timer_counter_obj = None
        self.current_input = None
        self.error_message = None
        self._input_files = None

        self.threadpool = QThreadPool()

        widget = QWidget()
        self.layout = QGridLayout(widget)
        self.setCentralWidget(widget)

        self.button_about.setShortcut('Ctrl+H')
        self.button_about.triggered.connect(self.show_about_message)

        self.option_activate_logging.triggered.connect(self.clicked_button_activate_logging)

        self.button_exit.setShortcut('Ctrl+Q')
        self.button_exit.triggered.connect(self.close)

        self.setWindowTitle("{} v{}".format(app_name, app_version))

        self.clicked_button_set_window()

        self.show()

    def clear_layout(self):
        """
        It clears the entire layout to let add another one.
        """
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        self.logger.info('Layout cleared')

    def clicked_button_set_window(self):
        """
        This method sets the window form as the current active frame.
        """
        self.clear_layout()
        self.current_input = WindowForm()

        self.layout.addWidget(self.current_input)
        self.current_input.push_button_start.setEnabled(False)
        # Configure layout
        self.current_input.push_button_input.clicked.connect(self.clicked_push_button_input)
        self.current_input.push_button_output.clicked.connect(self.clicked_push_button_output)

        self.current_input.line_edit_output.setText(self._current_path)
        # self.current_input.line_edit_template.setEnabled(False)
        self.enable_line_edits(False)
        self.enable_line_edits(True)

        self.current_input.push_button_start.clicked.connect(self.clicked_push_button_start)

        self.current_input.set_progress_bar_maximum(10)

    def set_logger(self, logger):
        """
        Function only to set the logger from the main function, otherwise other objects cannot use the main logger.
        Args:
            logger (logger): logger initialized in main function.
        """
        self.logger = logger

    def clicked_push_button_input(self):
        """
        Opens a file dialog to select all INI initial files to be used.
        """
        self._input_files, inut_file_format = QFileDialog.getOpenFileNames(
            self, 'Select INI files', self._current_path, filter='*.ini')
        self.logger.info('Initial INI files selected: {}'.format(self._input_files))
        if len(self._input_files) > 0:
            self.current_input.line_edit_input.setText(';'.join(self._input_files))
            self.current_input.line_edit_input.setEnabled(True)
            self.activate_start_button(self.current_input.groupbox_input)

    def clicked_push_button_output(self):
        """
        Opens a file dialog to select the output file.
        """
        folder_path = QFileDialog.getExistingDirectory(self, 'Select report folder', self._current_path)
        if folder_path != "":
            self.current_input.line_edit_output.clear()
            self.current_input.line_edit_output.setText(folder_path)
            self._output_path = folder_path
            self.logger.info('Output path updated to {}'.format(self._output_path))

    def window_report_generator(self, progress_callback):
        """
        Callback function to perform all the actions by the Table Maker.
        Args:
            progress_callback (callback): callback function to update the progress bar

        Returns:
            finalization_ok (bool): True if everything finished ok
        """
        finalization_ok = False
        try:
            self.logger.info('window_report_generator method is called.')

            for n in range(0, 10):
                time.sleep(1)
                progress_callback.emit(n)
            finalization_ok = True
        except Exception as error:
            self.error_message = str(error)
            self.logger.error(error)
        finally:
            return finalization_ok

    def thread_complete(self, finalized_ok):
        """
        Message raised after all the action are performed and the thread is over.
        Args:
            finalized_ok (bool): values indicating if the finalization is ok or not
        Returns:
            message box is raised with the result
        """
        # Enable elements while processing
        self.enable_buttons(True)
        self.enable_line_edits(True)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("{} v{}".format(app_name, app_version))
        if finalized_ok:
            msg_box.setIconPixmap(QPixmap(resource_path(r'support/success32.png')))
            msg_box.setText("Work has been completed successfully.")
        else:
            msg_box.setIconPixmap(QPixmap(resource_path(r"support/error32.png")))
            msg_box.setText("Error has occurred.\r\n{}".format(self.error_message))
        self.current_input.progress_bar.setValue(self.current_input.progress_bar.maximum())
        msg_box.exec_()

    def enable_buttons(self, action):
        """
        Enables or disables all buttons.
        Args:
            action (bool): True for enable, False for disable
        """
        for item in self.current_input.findChildren(QPushButton):
            item.setEnabled(action)

    def enable_line_edits(self, action):
        """
        Enables or disables all line edits.
        Args:
            action (bool): True for enable, False for disable
        """
        for item in self.current_input.findChildren(QLineEdit):
            if action:
                if item.text():
                    item.setEnabled(action)
            else:
                item.setEnabled(action)

    def clicked_push_button_start(self):
        """
        Button start actions
        """
        # Disable elements while processing
        self.enable_buttons(False)
        self.enable_line_edits(False)
        # Initialize status bar
        self.current_input.progress_bar.setValue(0)
        # Create Report Generator instance and the worker to run it
        self.timer_counter_obj = TimerCounter()
        self.logger.info('TableMaker object created')
        worker = Worker(self.window_report_generator)
        # Connect signals
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_bar)
        # Execute
        self.threadpool.start(worker)

    def clicked_button_activate_logging(self):
        """
        Method called when the option to activate the logging in the app menu is selected. It basically creates and
        adds a handler for a log file.
        """
        if self.option_activate_logging.isChecked():
            log_name = '{}_logfile.log'.format(datetime.now().strftime('%y%m%d%H%M%S'))
            handler = logging.FileHandler(log_name)
            formatter = logging.Formatter("%(asctime)s [%(name)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            if len(self.logger.handlers) > 0:
                for handler in self.logger.handlers:
                    if isinstance(handler, logging.FileHandler):
                        self.logger.info('Removing logging handler')
                        self.logger.removeHandler(handler)

    def progress_bar(self, n):
        """
        Update the progress bar
        """
        self.current_input.progress_bar.setValue(n)

    def activate_start_button(self, groupbox):
        """
        Check whether any of the INI files is not empty in order to activate or not the start button.
        Args:
            groupbox (QGroupBox): QGroupBox containing QLineEdit items to check whether whether they are empty or not
        """
        for item in groupbox.findChildren(QLineEdit):
            if item.text():
                self.current_input.push_button_start.setEnabled(True)
                self.current_input.push_button_start.setToolTip('')
                self.logger.info('Create Report button activated')
                return
        self.current_input.push_button_start.setEnabled(False)
        self.current_input.push_button_start.setToolTip('At least one INI file must be selected!')

    def show_about_message(self):
        """
        About message info
        """
        message_box = QMessageBox()
        message_box.about(self, '{}'.format(app_name),
                          '<p><b>Adria Guixa</b></p>'
                          '<p>Credits:'
                          '<br>Adria Guixa - '
                          'adriaguixa@gmail.com</p>'
                          '<p><b>Version: {}</b></p>'.format(app_version))
