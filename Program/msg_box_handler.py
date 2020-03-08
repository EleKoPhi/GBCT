from PyQt5.QtCore import *
from defines import *
from PyQt5.QtWidgets import *


class msgBoxHandler(QWidget, QObject):
    s_edit_user = pyqtSignal(str)
    s_new_user = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def deposit_message_box(self, deposit):

        format_str_deposit = "Datum:\t\t{date}\nBetrag in €:\t\t{Amount}\nAltes Guthaben:\t{old_amount}" + \
                             "\nNeues Guthaben:\t{new_amount}\nArt:\t\t{type_of_deposit}"

        popup_window = QMessageBox()
        popup_window.setDefaultButton(QMessageBox.Close)
        popup_window.setWindowTitle("Einzahlung ...")

        popup_window.setStandardButtons(QMessageBox.Close)

        txt = format_str_deposit.format(date=deposit.date, Amount=deposit.amount, old_amount=deposit.old_credit,
                                        new_amount=deposit.new_credit, type_of_deposit=deposit.get_tye_string())
        popup_window.setText(txt)
        popup_window.exec_()

    @pyqtSlot()
    def new_user_from_id(self, unknown_id):

        txt = unknow_id_msg_box_text.format(ID=unknown_id)

        popup_window = QMessageBox()

        popup_window.setText(txt)
        popup_window.addButton(QPushButton(back_label), QMessageBox.YesRole)
        popup_window.addButton(QPushButton(new_user_label), QMessageBox.YesRole)
        popup_window.addButton(QPushButton(edit_user_label), QMessageBox.YesRole)

        popup_window.setIcon(QMessageBox.Information)

        click_status = popup_window.exec_()

        if click_status == 1:
            self.s_new_user.emit(unknown_id)
        elif click_status == 2:
            self.s_edit_user.emit(unknown_id)

    def delete_user_question(self, user_name):

        _txt = delete_question_txt.format(name=user_name.replace("\t", " "))
        return QMessageBox.question(self, "???", _txt, QMessageBox.Yes | QMessageBox.No)

    def delete_id_question(self, id):

        _txt = delete_question_txt.format(name=id)
        return QMessageBox.question(self, "???", _txt, QMessageBox.Yes | QMessageBox.No)

    def show_id_data(self, _id):

        format_str_deposit = "ID:\t\t{id}\nNutzer:\t\t{User}\nAustauschdatum:\t{change_date}"

        popup_window = QMessageBox()
        popup_window.setDefaultButton(QMessageBox.Close)
        popup_window.setWindowTitle("ID Information")

        popup_window.setStandardButtons(QMessageBox.Close)

        txt = format_str_deposit.format(id=_id.ID, User=_id.User, change_date=_id.change_Date)
        popup_window.setText(txt)
        popup_window.exec_()

    def get_passed_id(self):
        _ID, okPressed = QInputDialog.getText(self, "Get ID", "Chip ID:", QLineEdit.Normal, "")
        if not okPressed: return False, False
        _Date, okPressed = QInputDialog.getText(self, "Change Date", "Date (JJJJ-MM-DD):", QLineEdit.Normal, "")

        _ID = _ID.replace("-", "").replace(".", "")

        return _ID, _Date

    def want_to_change(self, old_id, new_id, name):

        _txt = "Do you want to change ID: %s to new ID: %s for user %s" % (old_id, new_id, name)

        return QMessageBox.question(self, "???", _txt, QMessageBox.Yes | QMessageBox.No)
