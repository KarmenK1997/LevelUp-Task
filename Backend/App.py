from flask import Flask
from flask_cors import CORS
from flask import request
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "hello world", 200

class CreditCard:
    def __init__(self, d, cvv, pan):
        self.date = d
        self.cvv = cvv
        self.pan = pan
        thesebb = pan[0:2]
        if thesebb == "34" or thesebb == "37":
            self.vendor = "amex"
        else:
            self.vendor = "visa"

def check_cvv(cvv, vendor):
    if len(cvv) == 4 and vendor == "amex":
        return True
    if len(cvv) == 3 and not vendor == "amex":
        return True
    return False

def check_date(d):
    n = datetime.now()

    if d >= n:
        return True
    return False

def check_pan(pan):
    range_pan = range(16, 19+1)
    if len(pan) in range_pan:
        return True
    return False

def check_luhn(input):
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

def check_cc(cc):
    if not check_cvv(cc.cvv, cc.vendor):
        print ("cvv")
        return False
    if not check_date(cc.date):
        print ("date")
        return False
    if not check_pan(cc.pan):
        print ("pan")
        return False
    if not check_luhn(cc.pan):
        print ("luhn")
        return False
    return True

@app.route("/validate", methods = ["POST"])
def validate():
    data = request.form

    print(data)

    date = data.get("date")

    if not date:
        return "No date!", 403

    cvv = data.get("cvv")

    if not cvv:
        return "No cvv!", 403

    pan = data.get("pan")

    if not pan:
        return "No pan!", 403
    
    cc = CreditCard(datetime.strptime(data.get("date"), "%Y-%m-%d"), data.get("cvv"), data.get("pan"))

    return {"valid": check_cc(cc)}