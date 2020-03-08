from GBCT_gui import *
from serial_handler import *
import sys


def main():
    app = QApplication(sys.argv)
    GbctMain()
    sys.exit(app.exec_())
