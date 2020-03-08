from defines import *


class Deposit:

    def __init__(self, data):

        self.amount = data[1]
        self.user_name = data[2]
        self.old_credit = data[3]
        self.new_credit = data[4]
        self.consumption = data[5]
        self.Type = data[6]
        self.date = data[7]

    def get_tye_string(self):

        if self.Type == PayPal:
            return paypal_label

        if self.Type == Bar:
            return cash_label

        if self.Type == Material:
            return material_label
        else:
            return self.Type
