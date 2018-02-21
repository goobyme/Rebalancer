import csv
import re
import logging
import openpyxl


class FileReader:
    """Requires data"""
    def __init__(self, file_location):
        self.file_location = file_location
        if self.check(file_location) == 'csv':
            self.parse_csv()
        elif self.check(file_location) == 'xlsx':
            self.parse_xlsx()
        else:
            logging.error('FileTypeError: Need to read either csv or xlsx file type')
            pass

    @staticmethod
    def check(file_loc):
        csv_check = re.compile(r"\.csv")
        xl_check = re.compile(r"\.xlsx")
        if csv_check.findall(file_loc):
            return 'csv'
        elif xl_check.findall(file_loc):
            return 'xlsx'
        else:
            return None

    def parse_csv(self):
        with open(self.file_location, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # TODO set up readers to read each row and create list with each piece of info
            name_list = list(reader)
            amount_list = reader
            basis_list = reader

            stockdics = [{'Stock': name, 'Amount': amount, 'Basis': purchase_basis}
                         for name, amount, purchase_basis in zip(name_list, amount_list, basis_list)]
            yield stockdics

    def parse_xlsx(self):
        # TODO add excel data reader

        pass


class AllocReader(FileReader):

    def parse_csv(self):
        pass

    def parse_xlsx(self):
        pass
