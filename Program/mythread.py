from PyQt5.QtCore import *


class MyThread(QRunnable,QThread):

    def __init__(self, fn, *args, **kwargs):
        super(MyThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.kwargs = kwargs

    def run(self):
        self.fn(*self.args, **self.kwargs)
