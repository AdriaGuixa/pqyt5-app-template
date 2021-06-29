"""
Worker class thread

:author: Adria Guixa

:since: YYYY-MM-DD
"""
import sys
import traceback

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
        Supported signals are:
            finished
                No data
            error
                `tuple` (exctype, value, traceback.format_exc() )
            result
                `object` data returned from processing, anything
            progress
                `int` indicating % progress
    """
    finished = pyqtSignal(bool)
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    """
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    """
    def __init__(self, fn, *args, **kwargs):
        """
        Init method
        Args:
            fn (callback): The function callback to run on this worker thread. Supplied args and
            kwargs will be passed through to the runner.
            *args: Arguments to pass to the callback function
            **kwargs: Keywords to pass to the callback function
        """
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit(result)
