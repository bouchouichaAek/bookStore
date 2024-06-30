from paiment.models import *


class payment_method:
    def __init__(self, cc_number, cc_expiry):
        self.__cc_number = cc_number
        self.__cc_expiry = cc_expiry

    def getCardNumber(self):
        return self.__cc_number

    def getCardHolderName(self):
        return self.__card_holder_name


class payment_card:
    def __init__(self, cc_number, cc_expiry, cc_code, card_holder_name):
        self.__cc_number = cc_number
        self.__cc_expiry = cc_expiry
        self.__cc_code = cc_code
        self.__card_holder_name = card_holder_name

    def getCardNumber(self):
        return self.__cc_number

    def setCardNumber(self, cc_number):
        self.__cc_number = cc_number

    def getCardHolderName(self):
        return self.__card_holder_name

    def setCardHolderName(self, card_holder_name):
        self.__card_holder_name = card_holder_name

    def getDateExpiry(self):
        return self.__cc_expiry

    def setDateExpiry(self, cc_expiry):
        self.__cc_expiry = cc_expiry

    def getSecurityCode(self):
        return self.__cc_code

    def setSecurityCode(self, cc_code):
        self.__cc_code = cc_code


class dilevery_address:

    def __init__(self, stats, first_name, last_name, phone_number, address_complete, postal_code, city):
        self.__stats = stats
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__address_complete = address_complete
        self.__postal_code = postal_code
        self.__city = city

    def getState(self):
        return self.__stats

    def setState(self, stats):
        self.__stats = stats

    def getFirstName(self):
        return self.__first_name

    def setFirstName(self, first_name):
        self.__first_name = first_name

    def getLastName(self):
        return self.__last_name

    def setLastName(self, last_name):
        self.__last_name = last_name

    def getPhoneNumber(self):
        return self.__phone_number

    def setPhoneNumber(self, phone_number):
        self.__phone_number = phone_number

    def getAddressComplete(self):
        return self.__address_complete

    def setAddressComplete(self, address_complete):
        self.__address_complete = address_complete

    def getPostalCode(self):
        return self.__postal_code

    def setPostalCode(self, postal_code):
        self.__postal_code = postal_code

    def getCity(self):
        return self.__city

    def setCity(self, city):
        self.__city = city
