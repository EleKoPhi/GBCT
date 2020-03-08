import serial.tools.list_ports
from PyQt5.QtCore import *
from defines import *
from GBCT_gui import *
from PyQt5.QtWidgets import *


class SerialHandler(QObject):
    s_no_card_on_reader = pyqtSignal()  # Signal that is emitted when no card in on the reader
    s_confirm_credit_write = pyqtSignal(str)  # Signal that is emitted when the credit set from user is on the card
    s_new_card_found = pyqtSignal(str, str)  # Signal that is emitted to show the user information from card ID
    s_try_to_write_credit = pyqtSignal()  # Signal that is emitted when credit on card is not credit from gui
    s_serial_connection_set = pyqtSignal()  # Signal that is emitted when the card reader is set up - OK
    s_serial_connection_NOT_set = pyqtSignal()  # Signal that is emitted when the card reader is set up - not OK

    def __init__(self, parent=None):
        super(SerialHandler, self).__init__(parent)

        self.serial_connection = None
        self.connected = False
        self.setup_properly = False
        self.check_for_cards = True
        self.found_new_card = False
        self.update_chip_clicked = False
        self.deposit_type = None
        self.observer_state = True
        self.credit_from_gui = default_str_nr
        self.id_found_by_card_reader = default_str_nr
        self.credit_on_reader = default_str_nr
        self.ports = serial.tools.list_ports.comports

    def get_all_serial_devices(self):
        self.ports = serial.tools.list_ports.comports()
        return self.ports

    def connect_to_device(self, device):
        try:
            self.serial_connection = serial.Serial(device)
            self.connected = True
            self.s_serial_connection_set.emit()
            self.setup_properly = True

            if debug:
                print("Serial connection set up properly")
        except:
            self.connected = False
            self.s_serial_connection_NOT_set.emit()
            self.setup_properly = False

            if debug:
                print("Err in serial connection")

    def reset_class(self):
        self.connected = False
        self.setup_properly = True
        self.check_for_cards = True
        self.found_new_card = False
        self.update_chip_clicked = False
        self.deposit_type = None
        self.observer_state = True
        self.credit_from_gui = default_str_nr
        self.id_found_by_card_reader = default_str_nr
        self.credit_on_reader = default_str_nr

    def is_new_card_present(self):
        self.serial_connection.write(b'IsNewCardPresent')
        return self.serial_connection.readline().decode().replace("\n", "").replace("\r", "")

    def get_id(self):
        self.serial_connection.write(b'getID')
        return self.serial_connection.readline().decode().replace("\n", "").replace("\r", "")

    def read_credit(self):
        self.serial_connection.write(b'ReadCredit')
        return self.serial_connection.readline().decode().replace("\n", "").replace("\r", "")

    def write_credit(self, number):
        self.serial_connection.write(b'WriteCredit')
        self.serial_connection.readline().decode()
        self.flush_serial()
        return self.serial_connection.write(number.encode())

    def flush_serial(self):
        self.serial_connection.flushInput()
        self.serial_connection.flushOutput()

    def close_serial(self):
        self.setup_properly = False
        self.check_for_cards = False

        while self.observer_state: None

        self.serial_connection.close()
        if debug: print("serial connection closed")

    def set_credit_from_gui(self, number):
        self.credit_on_reader = number

    def set_update_chip_clicked(self, state):
        self.update_chip_clicked = state

    def set_gui_information(self, click_state, number):
        self.set_credit_from_gui(number)
        self.set_update_chip_clicked(click_state)

    def set_deposit_type(self, type):
        self.deposit_type = type

    @pyqtSlot()
    def observer_for_cards(self):

        _debounce = 0
        _dot_count = 0
        _reset_done = False
        self.observer_state = True

        while self.check_for_cards and self.setup_properly:

            state = self.is_new_card_present()

            if state == no_card_found_state:
                print("\rLooking for cards " + "." * _dot_count, flush=True, end="")
                _dot_count += 1
                _debounce += 1

                if _dot_count == 4:
                    _dot_count = 0

            elif state == card_found_state:

                _debounce = 0
                _dot_count = 0
                _reset_done = False
                _id = self.get_id()
                _credit = self.read_credit()

                if debug and _id != self.id_found_by_card_reader:
                    self.id_found_by_card_reader = _id
                    print("Card found!\r")
                    print("#####################################")
                    print("Current read ID    : " + _id)
                    print("Current read credit: " + _credit)
                    print("Current set credit : " + self.credit_on_reader)
                    print("#####################################")

                elif self.update_chip_clicked:
                    if self.credit_on_reader == _credit:
                        self.s_confirm_credit_write.emit(_credit)
                        self.update_chip_clicked = False
                        print("passt")
                    else:
                        self.s_try_to_write_credit.emit()
                        self.write_credit(self.credit_on_reader)
                        print("try ")
                    continue

                if _id is not None and str(_credit) != "-1" and self.found_new_card is False:
                    self.s_new_card_found.emit(_id, _credit)
                    self.found_new_card = True

            else:
                print("Undefended state:" + state)
                _debounce += 1

            if _debounce > 3 and (_reset_done is False):
                self.s_no_card_on_reader.emit()
                self.reset_class()
                _reset_done = True
                if debug: print("Reset card reader")
                continue

        self.observer_state = False
