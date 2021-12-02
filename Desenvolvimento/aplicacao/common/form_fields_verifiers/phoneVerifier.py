import phonenumbers

DEFAULT_REGION_CODE = 55

class Telephone:

    # Construtor
    def __init__(self, tel):
        tel = self.format_phone(tel)
        if tel[0] == '+':
            self.tel = phonenumbers.parse(tel, None)
        else:
            self.tel = phonenumbers.parse(f'+{DEFAULT_REGION_CODE}{tel}', None)

    def __str__(self):
        return phonenumbers.format_number(self.tel, phonenumbers.PhoneNumberFormat.NATIONAL)

    def is_valid(self, tel=None):
        if self.is_static(tel):
            return phonenumbers.is_valid_number(tel)
        return phonenumbers.is_valid_number(self.tel)

    @staticmethod
    def is_static(var):
        if var is None:
            return False
        return True

    @staticmethod
    def format_phone(tel):
        return tel.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

def is_telephone_valid(tel):
    return Telephone(tel).is_valid()
