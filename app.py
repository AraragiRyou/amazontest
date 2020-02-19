from flask import Flask, request
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = "amazon"
app.config["BASIC_AUTH_PASSWORD"] = "candidate"


basic_auth = BasicAuth(app)
inventory = {}
sales = {"sales":0}

@app.route('/')
def return_amazon():
    return 'AMAZON'

@app.route("/secret")
@basic_auth.required
def secret_view():
    return "SUCCESS"

@app.route("/calc", methods=["POST", "GET"])
def calc():
    string = request.query_string
    if string.isupper() or string.islower():
        return "ERROR"
    result = eval(string)
    return str(result)

@app.route("/stocker", methods=["POST", "GET"])
def function_caller():
    function_name = request.args.get("function")

    if function_name == "addstock":
        name = request.args.get("name")

        if name is None or name == "":
            return "ERROR"

        amount = request.args.get("amount")
        return addstock(name, amount)

    elif function_name == "checkstock":
        name = request.args.get("name")
        return checkstock(name)

    elif function_name == "sell":
        name = request.args.get("name")
        amount = request.args.get("amount")
        price = request.args.get("price")

        if name is None or name == "":
            return "ERROR"

        return sell(name,amount,price)

    elif function_name == "checksales":
        return checksales()

    elif function_name == "deleteall":
        return deleteall()

    else :
        return "NO FUNCTION IS SELECTED, ERROR"

def addstock(name, amount):
    if amount is None :
        amount = "1"
    if amount.isdigit():
        amount = int(amount)
    else:
        return "ERROR"
    if name in inventory:
        inventory[name] += amount
    else :
        inventory[name] = amount
    return ""

def checkstock(name):

    if name is None:
        return inventory

    else:
        if name in inventory:
            return name+":"+str(inventory[name])
        else :
            return "ERROR"

def sell(name, amount, price):
    if amount is None :
        amount = "1"
    if amount.isdigit():
        amount = int(amount)
    else:
        return "ERROR"
    if price is None :
        price = "0"
    if price.isdigit():
        price = int(price)
    else:
        return "ERROR"
    
    if name in inventory:
        inventory[name] -= amount
        sales["sales"] += amount*price
        return ""
    else:
        return "ERROR"

def checksales():
    return "sales:"+str(sales["sales"])


def deleteall():
    inventory = {}
    sales = 0
    return ""
