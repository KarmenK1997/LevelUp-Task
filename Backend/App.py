from flask import Flask
from flask_cors import CORS
from flask import request
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "hello world", 200

def determine_vendor(pan):
    if pan is None:
        return None
    pan = pan.replace(" ", "")
    if not pan.isdigit():
        return None
    range_pan = range(16, 19+1)
    if len(pan) not in range_pan:
        return None
    first_two = pan[0:2]
    if first_two == "34" or first_two == "37":
        return "amex"
    return "visa"

class CreditCard:
    def __init__(self, d, cvv, pan):
        self.date = d
        self.cvv = cvv
        self.pan = pan
        self.vendor = determine_vendor(pan)

def check_cvv(cvv, vendor):
    if cvv is None:
        return False
    if not cvv.isdigit():
        return False

    if vendor is None:
        return len(cvv) == 3 or len(cvv) == 4

    if len(cvv) == 4 and vendor == "amex":
        return True
    if len(cvv) == 3 and not vendor == "amex":
        return True
    return False

def check_date(d):
    if d is None:
        return False
    n = datetime.now()

    if d >= n:
        return True
    return False

def check_luhn(input):
    if input is None:
        return False
    
    input = input.replace(" ", "") 
 
    if len(input) <= 2 or not input.isdigit():
        return False

    def digits_of(input):
        return [int(digit) for digit in str(input)]

    check_digit = int(input[-1])

    payload = input[0:-1]

    odd = payload[-2::-2]
    even = payload[::-2]

    total = 0

    for digit in odd:
        total = total + int(digit)
    for digit in even:
        total += sum(digits_of(int(digit)*2))

    deduced_check_digit = (10-total%10)

    if check_digit == deduced_check_digit:
        return True
    return False

def check_cc(cc):
    if not check_cvv(cc.cvv, cc.vendor):
        print ("cvv")
        return False
    if not check_date(cc.date):
        print ("date")
        return False
    if determine_vendor(cc.pan) is None:
        print ("pan")
        return False
    if not check_luhn(cc.pan):
        print ("luhn")
        return False
    return True

@app.route("/validate", methods = ["POST"])
def validate():
    data = request.get_json()

    print(data)

    dateString = data.get("date")
    cvv = data.get("cvv")
    pan = data.get("pan")

    try:
        date = datetime.strptime(dateString, "%Y-%m")
    except:
        date = None

    cc = CreditCard(date, cvv, pan)

    return {"date_valid": check_date(cc.date), 
            "cvv_valid": check_cvv(cc.cvv, cc.vendor), 
            "vendor": cc.vendor, 
            "luhn_valid": check_luhn(cc.pan)
    }