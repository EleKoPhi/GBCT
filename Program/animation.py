from GBCT_gui import *
from PyQt5.QtCore import *
from defines import *
from GBCT_gui import *
from PyQt5.QtWidgets import *

class worker(QRunnable,QObject):
    s_animation = pyqtSignal(str)
    animation_f = True

    @pyqtSlot()
    def run(self):

        _dots = 1
        while self.animation_f:
            _txt = checking + " " + "." * _dots
            _dots += 1
            self.s_animation.emit(_txt)

            if _dots > 3: _dots = 1
