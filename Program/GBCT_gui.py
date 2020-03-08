from serial_handler import *
from DataBase import *
from userdatacontainer import *
from deposit import *
from datetime import date
from time import sleep
from msg_box_handler import *
from iddataconatiner import *
from QT_Line import *
from mythread import *


class GbctMain(QWidget, QObject):
    # Begin define Gui signals #

    update_credit_from_gui = pyqtSignal(str)
    s_animation = pyqtSignal(str)

    # End define gui signals #

    def __init__(self):
        super(GbctMain, self).__init__()
        QObject.__init__(self)

        # Begin GUI Objects

        self.active_ids = []
        self.top_left = QFrame()
        self.user_Tabs = QTabWidget()
        self.Active_user_tab = QWidget()
        self.Inactive_user_tab = QWidget()
        self.Inactive_User_List = QListWidget()
        self.Inactive_User_List.installEventFilter(self)
        self.Active_User_List = QListWidget()
        self.Active_User_List.installEventFilter(self)

        self.top_right = QFrame()
        self.user_name_label = QLabel(name_label)
        self.username_dsp = QTextEdit()
        self.user_id_label = QLabel(actual_id_label)
        self.user_id_dsp = QTextEdit()
        self.price = QRadioButton(reduced_price_label)
        self.user_status_dsp = QRadioButton(active_user_label)
        self.change_button = QPushButton(edit_label)
        self.new_user_button = QPushButton(new_user_label)
        self.total_inpay_lable = QLabel(total_deposit_label)
        self.total_inpay_value = QTextEdit()
        self.total_consumption_lable = QLabel(total_consumption_label)
        self.total_consumption_value = QTextEdit()
        self.User_tab_view = QTabWidget()
        self.old_id_tab = QWidget()
        self.inplay_tab = QWidget()
        self.deposits_dsp = QListWidget()
        self.old_id_list_widget = QListWidget()
        self.old_id_list_widget.installEventFilter(self)

        self.bottom = QFrame()
        self.serial_ports_selector = QComboBox()
        self.connect_button = QPushButton(connect_label)
        self.connection_display = QCheckBox(connect_label)
        self.serial_terminal_2_layout = QGridLayout()
        self.cash_deposit_dsp = QTextEdit()
        self.amount_lable = QLabel(amount_label_txt)
        self.old_credits_on_card_dsp = QTextEdit()
        self.old_amount_lable = QLabel(old_amount_label_txt)
        self.new_cedits_on_card_dsp = QTextEdit()
        self.new_credits_on_card_lable_disp = QLabel(new_amount_label_txt)
        self.UploadButton = QPushButton(upload_button_txt)
        self.ResetButton = QPushButton(reset_button_txt)
        self.deposit_type_selector = QComboBox()
        self.deposit_type_lable = QLabel(deposit_type_label_txt)
        self.serial_terminal_layout = QGridLayout()

        # End GUI Objects

        self.active_deposits = {}
        self.users = {}

        self.threadpool = QThreadPool()

        self.data_handler = DataHandler()
        self.card_reader = SerialHandler()
        self.message_box_handler = msgBoxHandler()

        self.check_animation_flag = True
        self.update_chip_clicked = False
        self.user_found_by_card_reader = None

        self.id_found_by_card_reader = default_str_nr
        self.credit_on_reader = default_str_nr
        self.displayed_user = None

        self.debounce = initial_debounce

        # Begin signal connections

        self.card_reader.s_new_card_found.connect(self.new_card_task)
        self.card_reader.s_confirm_credit_write.connect(self.log_new_deposit)
        self.card_reader.s_no_card_on_reader.connect(self.no_card_on_reader_task)
        self.card_reader.s_serial_connection_set.connect(self.card_reader_thread)

        self.message_box_handler.s_new_user.connect(self.new_user_from_signal)
        self.message_box_handler.s_edit_user.connect(self.edit_user_from_signal)

        self.s_animation.connect(self.s_animation_handler)

        self.Active_User_List.doubleClicked.connect(lambda: self.show_user(active_user_flag))
        self.Inactive_User_List.doubleClicked.connect(lambda: self.show_user(inactive_user_flag))
        self.deposits_dsp.doubleClicked.connect(self.build_deposit_popup)
        self.old_id_list_widget.doubleClicked.connect(self.show_id)

        self.UploadButton.clicked.connect(self.write_new_credit_task)
        self.deposit_type_selector.activated.connect(self.service_payment_gui_update)
        self.connect_button.clicked.connect(self.toggle_serial_selector)
        self.new_user_button.clicked.connect(self.log_new_user)
        self.change_button.clicked.connect(self.edit_user_from_button)

        self.UploadButton.clicked.connect(lambda: self.card_reader.set_update_chip_clicked(True))

        # End signal connections

        self.initialize()

    def show_id(self):

        _key = self.old_id_list_widget.currentItem().text().replace('-', '')
        if _key == no_old_ids_txt or _key == new_ID_list_label: return
        print(_key)
        print(self.active_ids)
        _id = self.active_ids[_key]

        self.message_box_handler.show_id_data(_id)

    def initialize(self):

        self.setWindowTitle(gui_title)
        self.setGeometry(300, 100, initial_width, initial_height)

        self.top_left.setFrameShape(QFrame.StyledPanel)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.top_right.setFrameShape(QFrame.StyledPanel)

        help_box: QHBoxLayout = QHBoxLayout(self)
        vertical_splitter: QSplitter = QSplitter(Qt.Vertical)

        horizontal_splitter = QSplitter(Qt.Horizontal)
        horizontal_splitter.addWidget(self.top_left)
        horizontal_splitter.addWidget(self.top_right)
        horizontal_splitter.setSizes([2, 3])

        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(self.bottom)
        vertical_splitter.setSizes([2, 3])

        help_box.addWidget(vertical_splitter)

        self.build_user_selector()
        self.build_data_viewer()
        self.build_serial_terminal()

        self.show()

    def build_user_selector(self):

        self.user_selector_layout = QVBoxLayout()

        self.user_Tabs.setMinimumSize(320, 250)

        self.user_Tabs.addTab(self.Active_user_tab, user_selector_active_name)
        self.user_Tabs.addTab(self.Inactive_user_tab, user_selector_inactive_name)

        self.Active_user_tab.layout = QVBoxLayout()
        self.Inactive_user_tab.layout = QVBoxLayout()

        self.update_user_dsp()

        self.Active_user_tab.layout.addWidget(self.Active_User_List)
        self.Inactive_user_tab.layout.addWidget(self.Inactive_User_List)

        self.Active_user_tab.setLayout(self.Active_user_tab.layout)
        self.Inactive_user_tab.setLayout(self.Inactive_user_tab.layout)

        self.user_selector_layout.addWidget(self.user_Tabs)

        self.top_left.setLayout(self.user_selector_layout)

    def build_data_viewer(self):

        self.data_viewer_layout = QGridLayout()
        self.data_viewer_left = QGroupBox(self)
        self.data_viewer_left_layout = QVBoxLayout()

        self.user_name_label.setMaximumHeight(30)

        self.username_dsp.setReadOnly(True)
        self.username_dsp.setMaximumHeight(30)

        self.user_id_label.setMaximumHeight(30)

        self.user_id_dsp.setReadOnly(True)
        self.user_id_dsp.setMaximumHeight(30)

        self.price.setMaximumHeight(30)
        self.price.setAutoExclusive(False)

        self.user_status_dsp.setMaximumHeight(30)
        self.user_status_dsp.setAutoExclusive(False)

        self.change_button.setMaximumHeight(30)

        self.new_user_button.setMaximumHeight(30)
        self.new_user_button.setDisabled(True)

        self.total_inpay_lable.setMaximumHeight(30)

        self.total_inpay_value.setReadOnly(True)
        self.total_inpay_value.setMaximumHeight(30)

        self.total_consumption_lable.setMaximumHeight(30)

        self.total_consumption_value.setReadOnly(True)
        self.total_consumption_value.setMaximumHeight(30)

        self.user_status_dsp.setEnabled(False)
        self.price.setEnabled(False)

        self.data_viewer_left_layout.addWidget(self.user_name_label, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(self.username_dsp, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(QHLine())
        self.data_viewer_left_layout.addWidget(self.user_id_label, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(self.user_id_dsp, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(QHLine())
        self.data_viewer_left_layout.addWidget(self.price, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(QHLine())
        self.data_viewer_left_layout.addWidget(self.user_status_dsp, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(QHLine())
        self.data_viewer_left_layout.addWidget(self.total_inpay_lable, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(self.total_inpay_value, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(QHLine())
        self.data_viewer_left_layout.addWidget(self.total_consumption_lable, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(self.total_consumption_value, alignment=Qt.AlignTop)
        self.data_viewer_left_layout.addWidget(QHLine())
        self.data_viewer_left_layout.addWidget(self.change_button, alignment=Qt.AlignBottom)
        self.data_viewer_left_layout.addWidget(self.new_user_button, alignment=Qt.AlignBottom)

        self.data_viewer_left.setLayout(self.data_viewer_left_layout)

        self.User_tab_view.setMinimumSize(300, 300)

        self.User_tab_view.addTab(self.inplay_tab, user_deposits_tab_name)
        self.User_tab_view.addTab(self.old_id_tab, user_id_history_tab_name)

        self.inplay_tab.layout = QVBoxLayout()
        self.old_id_tab.layout = QVBoxLayout()

        self.deposits_dsp.addItem(no_deposits_txt)
        self.old_id_list_widget.addItem(no_old_ids_txt)

        self.inplay_tab.layout.addWidget(self.deposits_dsp)
        self.old_id_tab.layout.addWidget(self.old_id_list_widget)

        self.inplay_tab.setLayout(self.inplay_tab.layout)
        self.old_id_tab.setLayout(self.old_id_tab.layout)

        self.data_viewer_layout.addWidget(self.data_viewer_left, 0, 0)
        self.data_viewer_layout.addWidget(QVLine(), 0, 1)
        self.data_viewer_layout.addWidget(self.User_tab_view, 0, 2)

        self.top_right.setLayout(self.data_viewer_layout)

    def build_serial_terminal(self):

        self.serial_terminal_1 = QGroupBox(self)
        self.serial_terminal_2 = QGroupBox(self)
        self.serial_terminal_1_layout = QVBoxLayout()

        for port in self.card_reader.get_all_serial_devices():
            self.serial_ports_selector.addItem(port.device)

        self.serial_terminal_1_layout.addWidget(self.serial_ports_selector)
        self.serial_terminal_1_layout.addWidget(self.connect_button)

        self.serial_terminal_1.setLayout(self.serial_terminal_1_layout)

        self.cash_deposit_dsp.setMaximumHeight(30)

        self.old_credits_on_card_dsp.setMaximumHeight(30)
        self.old_credits_on_card_dsp.setReadOnly(True)

        self.new_cedits_on_card_dsp.setMaximumHeight(30)
        self.new_cedits_on_card_dsp.setReadOnly(True)
        self.cash_deposit_dsp.setText(initial_number_value)

        self.deposit_type_selector.addItem(paypal_label)
        self.deposit_type_selector.addItem(cash_label)
        self.deposit_type_selector.addItem(material_label)
        self.deposit_type_selector.addItem(service_label)

        self.serial_terminal_2_layout.addWidget(self.old_amount_lable, 0, 0, 1, 1)
        self.serial_terminal_2_layout.addWidget(self.old_credits_on_card_dsp, 1, 0, 1, 1)

        self.serial_terminal_2_layout.addWidget(self.amount_lable, 0, 1, 1, 1)
        self.serial_terminal_2_layout.addWidget(self.cash_deposit_dsp, 1, 1, 1, 1)

        self.serial_terminal_2_layout.addWidget(self.new_credits_on_card_lable_disp, 0, 3, 1, 1)
        self.serial_terminal_2_layout.addWidget(self.new_cedits_on_card_dsp, 1, 3, 1, 1)

        self.serial_terminal_2_layout.addWidget(self.deposit_type_lable, 0, 2, 1, 1)
        self.serial_terminal_2_layout.addWidget(self.deposit_type_selector, 1, 2, 1, 1)

        self.serial_terminal_2_layout.addWidget(self.UploadButton, 0, 4, 1, 1)
        self.serial_terminal_2_layout.addWidget(self.ResetButton, 1, 4, 1, 1)
        self.ResetButton.setDisabled(True)
        self.ResetButton.setText("-")

        self.serial_terminal_layout.addWidget(self.serial_terminal_1, 0, 0, 1, 1)
        self.serial_terminal_layout.addWidget(QVLine(), 0, 1, 1, 1)
        self.serial_terminal_layout.addWidget(self.serial_terminal_2, 0, 2, 1, 2)

        self.serial_terminal_2.setLayout(self.serial_terminal_2_layout)

        self.bottom.setLayout(self.serial_terminal_layout)

    def build_deposit_popup(self):

        self.message_box_handler.deposit_message_box(self.active_deposits[self.deposits_dsp.currentItem().text()])

    def toggle_serial_selector(self):

        if self.serial_ports_selector.isEnabled():
            self.card_reader.connect_to_device(self.serial_ports_selector.currentText())
            self.serial_ports_selector.setEnabled(False)
            self.card_reader.check_for_cards = True

        else:
            self.serial_ports_selector.setEnabled(True)
            self.card_reader.close_serial()
            self.card_reader.check_for_cards = False
            self.card_reader.close_serial()

        self.serial_ports_selector.repaint()

    def service_payment_gui_update(self):

        if self.deposit_type_selector.currentText() == service_label:
            self.cash_deposit_dsp.setText(service_payment_information)
            self.cash_deposit_dsp.setDisabled(True)
            self.new_cedits_on_card_dsp.setReadOnly(False)
            self.old_amount_lable.setText(new_amount_label_txt)
            self.new_credits_on_card_lable_disp.setText(service_amound_txt)


        else:
            self.new_cedits_on_card_dsp.setReadOnly(True)
            self.cash_deposit_dsp.setDisabled(False)
            self.cash_deposit_dsp.setText(initial_number_value)
            self.old_amount_lable.setText(old_amount_label_txt)
            self.new_credits_on_card_lable_disp.setText(new_amount_label_txt)

    def checking_animation(self):

        _dots = 1

        self.check_animation_flag = True

        while self.check_animation_flag:
            _txt = checking + " " + "." * _dots
            _dots += 1
            if _dots > 3: _dots = 1
            self.s_animation.emit(_txt)
            sleep(1)

    def s_animation_handler(self, txt):

        if self.deposit_type_selector.currentText() == service_label:
            self.old_credits_on_card_dsp.setText(txt)
        else:
            self.new_cedits_on_card_dsp.setText(txt)

    def show_user(self, user_status, repaint=False):

        if user_status == active_user_flag:
            user_name = self.replace_tabs(self.Active_User_List.currentItem().text().replace('\t', ' '))

            if repaint == False:
                self.user_status_dsp.setChecked(True)
        else:

            user_name = self.replace_tabs(self.Inactive_User_List.currentItem().text().replace('\t', ' '))

            if user_name == new_user_list_label: return
            if repaint == False:
                self.user_status_dsp.setChecked(False)

        self.user_status_dsp.setEnabled(False)
        self.price.setEnabled(False)


        try:
            _user = self.data_handler.users[user_name]
        except:
            self.user_status_dsp.setChecked(False)
            return

        if _user.current_price == reduced_price_flag:
            self.price.setChecked(True)
        else:
            self.price.setChecked(False)

        self.price.setEnabled(False)

        self.username_dsp.setText(_user.surname + ' ' + _user.first_name)

        if _user.current_id == "None":
            self.user_id_dsp.setText(needs_to_be_edited_label)
        else:
            txt = _user.current_id[0:len(_user.current_id) - 4] + '-' + _user.current_id[-4:]
            txt = txt.replace("--", "-")
            self.user_id_dsp.setText(txt)

        self.deposits_dsp.clear()

        _key = _user.surname + ' ' + _user.first_name
        self.displayed_user = _key

        sql_cmd = "DEPOSIT WHERE user_name = '{}'".format(_key)

        user_deposits_sql_stream = self.data_handler.get_from_db(sql_cmd)

        if len(user_deposits_sql_stream) is not 0:

            _total_deposit = 0

            try:
                self.active_deposits = {}
                for sql_deposit in user_deposits_sql_stream:
                    deposit_data = Deposit(sql_deposit)
                    self.active_deposits[deposit_data.date] = deposit_data
                    self.deposits_dsp.addItem(deposit_data.date)
                    try:
                        _total_deposit = _total_deposit + float(deposit_data.amount)
                    except:
                        None

                self.total_inpay_value.setText("{0:.2f}".format(_total_deposit))
                self.total_consumption_value.setText(str(int(float(_total_deposit) / 0.45)))

            except:
                print("Err @ display all user deposits")

        else:

            self.deposits_dsp.addItem("Keine Einzahlungen gefunden")
            self.total_inpay_value.setText("0")
            self.total_consumption_value.setText("0")

        self.update_id_dsp(_key)

    def no_card_on_reader_task(self):

        self.credit_on_reader = "-1"
        self.id_found_by_card_reader = -10
        self.old_credits_on_card_dsp.setText(no_text)
        self.new_cedits_on_card_dsp.setText(no_text)
        self.cash_deposit_dsp.setText(initial_number_value)
        self.update_chip_clicked = False
        self.old_amount_lable.setText(old_amount_label_txt)
        self.old_amount_lable.repaint()

    def log_new_user(self):
        _user_txt = self.username_dsp.toPlainText()

        try:
            _user_txt = _user_txt.replace(",", "")
            _user_txt = _user_txt.split(" ")
        except:
            return

        _fist_name = _user_txt[0]
        _last_name = _user_txt[1]
        _current_id = self.user_id_dsp.toPlainText().replace("-", "")
        _status = self.user_status_dsp.isChecked()

        if _status:
            _status = active_user_flag
        else:
            _status = inactive_user_flag

        _price = self.price.isChecked()

        if _price:
            _price = reduced_price_flag
        else:
            _price = normal_price_flag

        self.data_handler.add_user_to_database(first_name=_fist_name, last_name=_last_name, currentID=_current_id,
                                               status=_status, price=_price)

        _new_user = UserDataContainer((self.data_handler.get_from_db(
            "USER WHERE first_name = '%s' AND last_name = '%s'" % (_fist_name, _last_name)))[0])

        self.setup_after_new_user(_new_user)

    def log_new_deposit(self, credits_to_log):

        _t = self.deposit_type_selector.currentText()
        self.check_animation_flag = False

        if _t == service_label:
            _amount = self.cash_deposit_dsp.setText(service_payment_information)
            self.old_credits_on_card_dsp.setText(credits_to_log)
            self.new_cedits_on_card_dsp.setText(credits_to_log)
        else:
            _amount = self.cash_deposit_dsp.toPlainText()
            self.new_cedits_on_card_dsp.setText(str(credits_to_log))


        _name = self.username_dsp.toPlainText()
        _old_credit = self.old_credits_on_card_dsp.toPlainText()
        _key = self.user_found_by_card_reader.surname + ' ' + self.user_found_by_card_reader.first_name


        sql_cmd = "DEPOSIT WHERE user_name = '{}'".format(_key)
        user_deposits_sql_stream = self.data_handler.get_from_db(sql_cmd)

        if len(user_deposits_sql_stream) > 0:
            _consumption = "0"
        else:
            _consumption = "0"

        _day = date.today().strftime("%Y-%m-%d")

        if _t == paypal_label:
            _type = PayPal
        elif _t == cash_label:
            _type = Bar
        elif _t == material_label:
            _type = Material
        elif _t == service_label:
            _type = Serivce
        else:
            _type = Unknown

        self.data_handler.add_deposit_to_database(_amount, _name, _old_credit, credits_to_log, _consumption, _type,
                                                  _day)

        _key = self.user_found_by_card_reader.surname + ' ' + self.user_found_by_card_reader.first_name
        sql_cmd = "DEPOSIT WHERE user_name = '{}'".format(_key)
        user_deposits_sql_stream = self.data_handler.get_from_db(sql_cmd)

        if user_deposits_sql_stream is not []:
            _total_deposit = 0
            self.deposits_dsp.clear()
            self.deposits_dsp.repaint()
            try:
                self.active_deposits = {}
                for sql_deposit in user_deposits_sql_stream:
                    deposit_data = Deposit(sql_deposit)
                    self.active_deposits[deposit_data.date] = deposit_data
                    self.deposits_dsp.addItem(deposit_data.date)
                    try:
                        _total_deposit = _total_deposit + float(deposit_data.amount)
                    except:
                        None
                #self.total_inpay_value.setText("{0:.2f}".format(_total_deposit))
                #self.total_consumption_value.setText(str(int(float(_total_deposit) / 0.45)))
            except:
                print("Err @ display all user deposits")

            self.old_amount_lable.setText(old_amount_label_txt)
            self.old_amount_lable.repaint()

    def card_reader_thread(self):

        self.card_reader.check_for_cards = True
        thread = MyThread(self.card_reader.observer_for_cards)
        self.threadpool.start(thread)

    def write_new_credit_task(self):

        _type = self.deposit_type_selector.currentText()
        thread = MyThread(self.checking_animation)
        self.threadpool.start(thread)

        if _type == "Service":
            new_credit_to_upload = self.new_cedits_on_card_dsp.toPlainText()

        else:
            old_credit = self.old_credits_on_card_dsp.toPlainText()

            if self.user_found_by_card_reader.current_price == reduced_price_flag:
                new_credit_to_upload = round(
                    (float(old_credit)) + (float(self.cash_deposit_dsp.toPlainText()) / reduced_price_value))
            elif self.user_found_by_card_reader.current_price == normal_price_flag:
                new_credit_to_upload = round(
                    (float(old_credit)) + (float(self.cash_deposit_dsp.toPlainText()) / normal_price_value))

        self.credit_on_reader = str(new_credit_to_upload)
        self.card_reader.set_gui_information(True, self.credit_on_reader)
        self.new_cedits_on_card_dsp.repaint()

    def update_user_dsp(self):

        self.data_handler.update_users_from_db()
        self.users = {}
        self.Active_User_List.clear()
        self.Inactive_User_List.clear()

        self.data_handler.update_users_from_db()

        self.Active_User_List.addItem(new_user_list_label)
        self.Inactive_User_List.addItem(new_user_list_label)

        for _user in self.data_handler.users:

            _u = self.data_handler.users[_user]
            if _u.current_status == active_user_flag:
                if len(_u.surname) <= 11:
                    self.Active_User_List.addItem(_u.surname + '\t\t' + _u.first_name)
                else:
                    self.Active_User_List.addItem(_u.surname + '\t' + _u.first_name)
            else:
                if len(_u.surname) <= 11:
                    self.Inactive_User_List.addItem(_u.surname + '\t\t' + _u.first_name)
                else:
                    self.Inactive_User_List.addItem(_u.surname + '\t' + _u.first_name)

        self.Active_User_List.repaint()
        self.Inactive_User_List.repaint()
        self.repaint()
        self.Active_User_List.repaint()
        self.Inactive_User_List.repaint()
        self.repaint()

    def new_card_task(self, card_id, credit):

        sql_cmd = "USER WHERE currentID = '{}'".format(card_id)

        user_stream = self.data_handler.get_from_db(sql_cmd)

        if len(user_stream) != 0:

            try:
                self.user_found_by_card_reader = UserDataContainer(user_stream[0])
            except:
                print("err in new_card_task")
                return
        else:
            self.message_box_handler.new_user_from_id(card_id)
            return

        self.old_credits_on_card_dsp.setText(credit)
        self.cash_deposit_dsp.setText(no_text)

        self.set_user_active(self.user_found_by_card_reader)

    def set_user_active(self, user):

        if not isinstance(user, UserDataContainer): return

        if user.current_status == active_user_flag:
            self.user_Tabs.setCurrentIndex(0)

            for person_nr in range(self.Active_User_List.count()):
                self.Active_User_List.setCurrentRow(person_nr)

                if self.Active_User_List.currentItem().text().replace('\t', '') == (
                        user.surname + user.first_name):
                    self.show_user(user.current_status)

                    self.Active_User_List.repaint()
                    self.Active_User_List.setFocus()
                    return

        elif user.current_status == inactive_user_flag:
            self.user_Tabs.setCurrentIndex(1)

            for person_nr in range(self.Inactive_User_List.count()):
                self.Inactive_User_List.setCurrentRow(person_nr)

                if self.Inactive_User_List.currentItem().text().replace('\t', '') == (
                        user.surname + user.first_name):
                    self.show_user(user.current_status)

                    self.Inactive_User_List.repaint()
                    self.Inactive_User_List.setFocus()
                    return

    def new_user_from_signal(self, unknown_id):
        self.new_user_button.setDisabled(False)
        self.username_dsp.setText(no_text)
        self.user_id_dsp.setText(unknown_id[0:len(unknown_id) - 4] + '-' + unknown_id[-4:])
        self.user_id_dsp.setReadOnly(True)
        self.price.setDisabled(False)
        self.user_status_dsp.setDisabled(False)
        self.user_name_label.setText(surname + ", " + given_name)
        self.username_dsp.setReadOnly(False)
        self.total_consumption_value.setDisabled(True)
        self.total_consumption_lable.setDisabled(True)
        self.total_inpay_value.setDisabled(True)
        self.total_inpay_lable.setDisabled(True)
        try:
            self.Active_User_List.doubleClicked.disconnect()
            self.Inactive_User_List.doubleClicked.disconnect()
        except:
            print("Err in disconnect()")
        self.change_button.setText(Cancel_lable)
        self.change_button.clicked.disconnect()
        self.change_button.clicked.connect(self.setup_after_new_user)

    def edit_user_from_signal(self, unknown_id):

        self.Active_User_List.doubleClicked.disconnect()
        self.Inactive_User_List.doubleClicked.disconnect()

        self.Active_User_List.doubleClicked.connect(lambda: self.change_id(unknown_id))
        self.Inactive_User_List.doubleClicked.connect(lambda: self.change_id(unknown_id))

        self.username_dsp.setText(edit_from_signal_txt)
        self.user_id_dsp.setText(unknown_id)
        self.total_inpay_lable.setDisabled(True)
        self.total_inpay_value.setDisabled(True)
        self.total_consumption_lable.setDisabled(True)
        self.total_consumption_value.setDisabled(True)
        self.change_button.setDisabled(True)
        self.repaint()

    def edit_user_from_button(self):

        try:

            if self.user_Tabs.currentIndex() == 0:
                if self.Active_User_List.currentItem().text() == (new_user_list_label or None): return
                self.show_user(active_user_flag, repaint=True)
            else:
                if self.Inactive_User_List.currentItem().text() == (new_user_list_label or None): return
                self.show_user(inactive_user_flag, repaint=True)
        except:
            print("Err in edit_user_from_button")
            return

        if self.change_button.text() == edit_label:
            self.change_button.setText(safe_label_txt)
            self.price.setEnabled(True)
            self.user_status_dsp.setEnabled(True)

        else:
            self.change_button.setText(edit_label)

            try:

                if self.user_Tabs.currentIndex() == 0:
                    _user = self.replace_tabs(self.Active_User_List.currentItem().text().replace('\t', ' '))
                elif self.user_Tabs.currentIndex() == 1:
                    _user = self.replace_tabs(self.Inactive_User_List.currentItem().text().replace('\t', ' '))
            except:
                print("Err at save user")
                return

            if _user == new_user_list_label:
                self.price.setEnabled(False)
                self.user_status_dsp.setEnabled(False)
                self.price.repaint()
                self.user_status_dsp.repaint()
                print("Selected user was: " + new_user_list_label)
                return

            if self.price.isChecked():
                self.data_handler.set_value(reduced_price_flag, _user, price_sql_txt)
                self.data_handler.users[_user].current_price = reduced_price_flag
            else:
                self.data_handler.set_value(normal_price_flag, _user, price_sql_txt)
                self.data_handler.users[_user].current_price = normal_price_flag

            self.data_handler.update_users_from_db()

            # self.user_status_dsp.setChecked(False)

            print(self.user_status_dsp.isChecked())

            if self.user_status_dsp.isChecked() == True:
                self.data_handler.users[_user].current_status = active_user_flag
                self.Active_User_List.clear()
                self.data_handler.set_value(active_user_flag, _user, status_sql_txt)
                self.update_user_dsp()
                self.user_Tabs.setCurrentIndex(0)

                for i in range(self.Active_User_List.count()):
                    self.Active_User_List.setCurrentRow(i)
                    if self.replace_tabs(self.Active_User_List.currentItem().text().replace('\t', ' ')) == _user:
                        break

            elif self.user_status_dsp.isChecked() != True:
                self.data_handler.users[_user].current_status = inactive_user_flag
                self.Inactive_User_List.clear()
                self.data_handler.set_value(inactive_user_flag, _user, status_sql_txt)
                self.update_user_dsp()
                self.user_Tabs.setCurrentIndex(1)

                for i in range(self.Inactive_User_List.count()):
                    self.Inactive_User_List.setCurrentRow(i)
                    if self.replace_tabs(self.Inactive_User_List.currentItem().text().replace('\t', ' ')) == _user:
                        break
            else:
                print("err in edit")

            self.price.setEnabled(False)
            self.user_status_dsp.setEnabled(False)

        self.price.repaint()
        self.user_status_dsp.repaint()

    def change_id(self, unknown_id):

        if self.Active_User_List.hasFocus():
            _user = self.Active_User_List.currentItem().text()
        elif self.Inactive_User_List.hasFocus():
            _user = self.Inactive_User_List.currentItem().text()

        _user_name = self.replace_tabs(_user.replace("\t", " "))

        _name = _user_name.split(" ")
        sql_cmd = "USER WHERE first_name = '%s' AND last_name = '%s'" % (_name[0], _name[1])
        _user_from_sql = self.data_handler.get_from_db(sql_cmd)
        _user = UserDataContainer(_user_from_sql[0])

        if self.message_box_handler.want_to_change(_user.current_id, unknown_id,
                                                   _user.first_name + " " + _user.surname) == QMessageBox.Yes:
            self.data_handler.set_value(unknown_id, _user_name, 'currentID')
            self.data_handler.add_id_to_database(unknown_id, _user_name, date.today().strftime("%Y-%m-%d"))

        self.Active_User_List.doubleClicked.disconnect()
        self.Inactive_User_List.doubleClicked.disconnect()

        self.Active_User_List.doubleClicked.connect(lambda: self.show_user(active_user_flag))
        self.Inactive_User_List.doubleClicked.connect(lambda: self.show_user(inactive_user_flag))

        self.data_handler.update_users_from_db()

        self.total_inpay_lable.setDisabled(False)
        self.total_inpay_value.setDisabled(False)
        self.total_consumption_lable.setDisabled(False)
        self.total_consumption_value.setDisabled(False)
        self.change_button.setDisabled(False)

        if self.Active_User_List.hasFocus():
            self.show_user(active_user_flag)
        elif self.Inactive_User_List.hasFocus():
            self.show_user(inactive_user_flag)

        self.repaint()

    def setup_after_new_user(self, new_user):
        self.username_dsp.setReadOnly(True)
        self.total_consumption_value.setDisabled(False)
        self.total_consumption_lable.setDisabled(False)
        self.total_inpay_value.setDisabled(False)
        self.total_inpay_lable.setDisabled(False)
        self.Active_User_List.doubleClicked.connect(lambda: self.show_user(active_user_flag))
        self.Inactive_User_List.doubleClicked.connect(lambda: self.show_user(inactive_user_flag))
        self.new_user_button.setDisabled(True)
        self.change_button.setText(edit_label)
        self.change_button.clicked.connect(self.edit_user_from_button)
        self.user_id_dsp.setReadOnly(True)
        self.update_user_dsp()
        if isinstance(new_user, UserDataContainer):
            self.set_user_active(new_user)
            self.show_user(new_user.current_status)
        self.user_name_label.setText(name_label)
        self.user_name_label.repaint()

    def update_id_dsp(self, _key):
        sql_cmd = "IDS WHERE User = '{}'".format(_key)
        user_ids_sql_stream = self.data_handler.get_from_db(sql_cmd)

        if len(user_ids_sql_stream) is not 0:

            self.active_ids = {}
            self.old_id_list_widget.clear()
            self.old_id_list_widget.addItem(new_ID_list_label)

            for id in user_ids_sql_stream:
                _data = IdContainer(id)
                self.active_ids[_data.ID] = _data
                self.old_id_list_widget.addItem(_data.format_string())

        else:
            self.active_ids = {}
            self.old_id_list_widget.clear()
            self.old_id_list_widget.addItem(new_ID_list_label)
            self.old_id_list_widget.addItem(no_old_ids_txt)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.ContextMenu and
                ((source is self.Active_User_List) or (source is self.Inactive_User_List))):

            menu = QMenu()

            click = source.itemAt(event.pos())

            if click is not None and click.text() != new_user_list_label:
                delete_action = menu.addAction(delete_lable)

                click_on = menu.exec_(event.globalPos())

                if click_on == delete_action:
                    item = source.itemAt(event.pos())

                    if item is not None:
                        _user = item.text()
                        if self.message_box_handler.delete_user_question(_user) == QMessageBox.Yes:
                            self.data_handler.delete_user(_user)
                            self.update_user_dsp()
                            self.reset_user_dsp()
            else:

                new_user_action = menu.addAction(add_user_lable)
                click_on = menu.exec_(event.globalPos())

                if click_on == new_user_action:
                    self.new_user_from_signal("")
                    self.user_id_dsp.setReadOnly(False)
                    self.user_id_dsp.setText("")
                    self.repaint()

            return True

        elif event.type() == QEvent.ContextMenu and source is self.old_id_list_widget:

            menu = QMenu()
            click = source.itemAt(event.pos())

            if click is not None and click.text() != new_ID_list_label and click.text() != no_old_ids_txt:
                delete_action = menu.addAction(delete_lable)
                click_on = menu.exec_(event.globalPos())

                if click_on == delete_action:
                    item = source.itemAt(event.pos())

                    if item is not None:
                        _ID = item.text()
                        if self.message_box_handler.delete_user_question(_ID) == QMessageBox.Yes:
                            self.data_handler.delete_id(_ID)
                            self.update_id_dsp(self.displayed_user)
                return True
            else:

                new_id_action = menu.addAction(add_id_lable)
                click_on = menu.exec_(event.globalPos())

                if click_on == new_id_action:
                    _ID, _Date = self.message_box_handler.get_passed_id()

                    if _ID is not False:
                        self.data_handler.add_id_to_database(_ID, self.username_dsp.toPlainText(), _Date)
                        self.update_id_dsp(self.displayed_user)

        return super(GbctMain, self).eventFilter(source, event)

    def reset_user_dsp(self):
        self.username_dsp.setText(no_text)
        self.user_id_dsp.setText(no_text)
        self.price.setChecked(False)
        print("H")
        self.user_status_dsp.setChecked(False)
        self.total_inpay_value.setText(no_text)
        self.total_consumption_value.setText(no_text)
        self.repaint()

    def replace_tabs(self, key):
        new_key = ""
        found = False

        for i in key:

            if i == ' ' and found == True:
                continue
            elif i == ' ':
                found = True

            new_key = new_key + i

        return new_key
