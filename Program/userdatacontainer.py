class UserDataContainer:

    def __init__(self, data):
        self.surname = data[1]
        self.first_name = data[2]
        self.current_department = data[3]
        self.current_id = data[4]
        self.current_status = data[5]
        self.current_price = data[6]

    def __str__(self):
        user_str = "Display user with the following information...\nFirst name:\t{}\nSurname:\t{}\nDepartment:\t{" \
                   "}\nID:\t\t\t{}\nStatus:\t\t{}\nPrice: \t\t{}\n".format(self.surname, self.first_name,
                                                                           self.current_department, self.current_id,
                                                                           self.current_status, self.current_price)

        return user_str

