from datetime import datetime
import unittest

from App import CreditCard, check_cc, check_cvv, check_date, check_luhn, determine_vendor


class MyTest(unittest.TestCase):
    def test_check_cvv(self):
        assert check_cvv("3", "amex") == False
        assert check_cvv("12", "amex") == False
        assert check_cvv("123", "amex") == False
        assert check_cvv("1234", "amex") == True
        assert check_cvv("1", "visa") == False
        assert check_cvv("12", "visa") == False
        assert check_cvv("123", "visa") == True
        assert check_cvv("1234", "visa") == False
        assert check_cvv("12345", "amex") == False
        assert check_cvv("", "amex") == False
        assert check_cvv(None, None) == False
        assert check_cvv("123", None) == True
        assert check_cvv("12", None) == False
        assert check_cvv("1234", None) == True
        assert check_cvv("12345", None) == False
        assert check_cvv(None, "amex") == False
        assert check_cvv(None, "visa") == False
        assert check_cvv("hgg", "visa") == False

    def test_determine_vendor(self):
        assert determine_vendor("1234567890123456") == "visa"
        assert determine_vendor("abshdktjcuyjensid") == None
        assert determine_vendor("3434567890123456") == "amex"
        assert determine_vendor("3 434 567890 123456") == "amex"
        assert determine_vendor("3 rzuin 567890 12456") == None
        assert determine_vendor("123456789012") == None
        assert determine_vendor("") == None
        assert determine_vendor(None) == None

    def test_check_date(self):
        assert check_date(datetime(2020, 2, 2)) == False
        assert check_date(datetime(2027, 2, 2)) == True
        assert check_date(datetime(2030, 2, 2)) == True
        assert check_date(datetime(2033, 2, 2)) == True
        assert check_date(None) == False

    def test_check_luhn(self):
        assert check_luhn("12345678901234569") == True
        assert check_luhn("1234567890123452") == True
        assert check_luhn("1234 5678 9012 3452") == True
        assert check_luhn("1234 rtui 9012 3452") == False
        assert check_luhn("") == False
        assert check_luhn("1") == False
        assert check_luhn("12") == False
        assert check_luhn(None) == False

    def test_check_cc(self):
        assert check_cc(CreditCard(datetime(2030, 2, 2), "1234", "34123426387253675")) == True
        assert check_cc(CreditCard(datetime(2030, 2, 2), "123", "34123426387253675")) == False
        assert check_cc(CreditCard(datetime(2030, 2, 2), "123", "62839264729164722")) == True
        assert check_cc(CreditCard(datetime(2030, 2, 2), "12", "62839264729164722")) == False
        assert check_cc(CreditCard(datetime(2020, 2, 2), "123", "62839264729164722")) == False
        assert check_cc(CreditCard(datetime(2030, 2, 2), "1234", "34123426387253671")) == False
        assert check_cc(CreditCard(datetime(2020, 2, 2), "123", "34123426387253671")) == False
        assert check_cc(CreditCard((None), "1234", "34123426387253675")) == False
        assert check_cc(CreditCard(datetime(2020, 2, 2), "", "34123426387253671")) == False
        assert check_cc(CreditCard(datetime(2020, 2, 2), "123", "")) == False
        assert check_cc(CreditCard(datetime(2020, 2, 2), None, "34123426387253671")) == False
        assert check_cc(CreditCard(datetime(2020, 2, 2), "123", None)) == False
        assert check_cc(CreditCard(datetime(2030, 2, 2), "1234", "34123426387253675")) == True
        assert check_cc(CreditCard(datetime(2030, 2, 2), "1234", "abchsifjzsncijdt")) == False
        assert check_cc(CreditCard(datetime(2030, 2, 2), "jjhg", "34123426387253675")) == False
  

