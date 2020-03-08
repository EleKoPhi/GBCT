class IdContainer:

    def __init__(self, data_stream):
        self.ID = data_stream[1]
        self.User = data_stream[2]
        self.change_Date = data_stream[3]


    def format_string(self):

        return self.ID[0:len(self.ID) - 4] + '-' + self.ID[-4:]
