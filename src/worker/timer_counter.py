"""
Simple counter to test the capabilities of the progress bar.

:author: Adria Guixa

:since: YYYY-MM-DD
"""
from PyQt5.QtCore import QTimer
import logging
import time


class TimerCounter(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)

    def init_timer(self):
        """
        Initialize timer counter.
        """
        self.timer.start()
        self.logger.info('Timer has been initialized')

    def recurring_timer(self):
        """
        Increments the counter by 1.
        """
        self.counter += 1
        self.logger.info('Counter: {}'.format(self.counter))
