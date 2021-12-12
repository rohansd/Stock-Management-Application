import mysql.connector
import PySimpleGUI as sg
import requests
import traceback

import mysql
import hashlib
from pip._internal.cli.cmdoptions import progress_bar

cnx = mysql.connector.connect(user="doadmin", password="oIBYQkL5DkeOMWwi", host="db-mysql-nyc3-51583-do-user-8820074-0.b.db.ondigitalocean.com", port=25060, database="Project2", auth_plugin='mysql_native_password')
cursor = cnx.cursor()


def brokerLandingPage():
    sg.theme('BluePurple')
    layout = [
        [sg.Button("Search", size=(15, 1))],
        [sg.Button("Place Order", size=(15, 1))],
        [sg.Button("View Portfolio", size=(15, 1))],
        [sg.Button("Add Client", size=(15, 1))],
        [sg.Button("Log Out", size=(15, 1))]
    ]
    window = sg.Window("brokerLandingPage", layout)
    while True:
        event, values = window.read()
        if event == 'Log Out' or event == sg.WIN_CLOSED:
            break
        elif event == 'Search':
            window.close()
            brokerSearch()
        elif event == 'Place Order':
            window.close()
            CustomerSelection()
        elif event == 'View Portfolio':
            window.close()
            ViewPortfolioCustomerSelection()
        elif event == 'Add Client':
            window.close()
            AddClient()

def AddClient():
    logging.info("AddClient")
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("First Name : ", font=15),
            sg.InputText(key='-fname-', font=15)
        ],
        [
            sg.Text("Last Name : ", font=15),
            sg.InputText(key='-lname-', font=15)
        ],
        [
            sg.Text("Email :          ", font=15),
            sg.InputText(key='-Email-', font=15)
        ],
        [
            sg.Text("funds :           ", font=15),
            sg.InputText(key='-funds-', font=15)
        ],
        [
            sg.Text("SSN :            ", font=15),
            sg.InputText(key='-ssn-', font=15)
        ],
        [
            sg.Button("Add client")
        ]
    ]
    window = sg.Window("Select", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                brokerLandingPage()
            elif event == "Add client":
                window.close()
                query = ("INSERT INTO client(fname,lname,email,funds,ssn,brokerssn) VALUES (%s,%s,%s,%s,%s,%s)")
                cursor.execute(query, (values['-fname-'],values['-lname-'],values['-Email-'],int(values['-funds-']),int(values['-ssn-']),brokerssn))
                cnx.commit()
                brokerdisplayMessage("Client has been added")

def ViewPortfolioCustomerSelection():
    logging.info("ViewPortfolioCustomerSelection")
    query = ("SELECT Id,fname,lname,funds FROM client where brokerssn = %s")
    cursor.execute(query, (brokerssn,))
    data = []
    for i in cursor:
        data.append((list(i)))
    list_of_client_Id = []
    for li in data:
        list_of_client_Id.append(li[0])
    logging.info(f"ViewPortfolioCustomerSelection {data}")
    header_list = ["Id", "fname", "lname", "funds"]
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Select your client : ", font=15),
            sg.InputText(key='-clientId-', font=15),
            sg.Button("Select")
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  col_widths=[25, 25, 25],
                  justification="center",
                  size=(100, 1),
                  num_rows=min(100, len(data)))
        ],
    ]
    window = sg.Window("Select", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                brokerLandingPage()
            elif event == "Select":
                if(int(values['-clientId-']) in list_of_client_Id):
                    window.close()
                    displayportfolio(int(values['-clientId-']))
                else:
                    brokerdisplayErrorMessage("Client Id is invalid")

def displayportfolio(clientId):
    logging.info(f"displayportfolio")
    global clientssn
    query = ("SELECT ssn,funds FROM client where Id = %s")
    cursor.execute(query, (clientId,))
    data = []
    for i in cursor:
        data.append((list(i)))
    clientssn = data[0][0]
    clientfunds = data[0][1]
    sg.theme('BluePurple')
    query = ("SELECT companysharecode,sum(quantity) FROM clientportfolio where clientssn = %s GROUP BY companysharecode")
    cursor.execute(query, (clientssn,))

    data = []
    for i in cursor:
        data.append((list(i)))

    header_list = ["Company Ticker", "Invested amount $"]

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Client Id : ", font=15),sg.Text(str(clientId), font=15),
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  col_widths=[25, 25, 25],
                  justification="center",
                  size=(100, 1),
                  num_rows=min(100, len(data)))]
    ]
    window = sg.Window("ViewPortfolio", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                brokerLandingPage()

def CustomerSelection():
    logging.info(f"CustomerSelection")
    query = ("SELECT Id,fname,lname,funds FROM client where brokerssn = %s")
    cursor.execute(query, (brokerssn,))
    data = []
    for i in cursor:
        data.append((list(i)))
    list_of_client_Id = []
    for li in data:
        list_of_client_Id.append(li[0])
    header_list = ["Id", "fname", "lname", "funds"]
    logging.info(f"{data}")
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Select your client : ", font=15),
            sg.InputText(key='-clientId-', font=15),
            sg.Button("Select")
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  col_widths=[25, 25, 25],
                  justification="center",
                  size=(100, 1),
                  num_rows=min(100, len(data)))
        ],
    ]
    window = sg.Window("Select", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                brokerLandingPage()
            elif event == "Select":
                if(int(values['-clientId-']) in list_of_client_Id):
                    window.close()
                    brokerplaceNewOrder(int(values['-clientId-']))
                else:
                    brokerdisplayErrorMessage("Client Id is invalid")


def brokerplaceNewOrder(clientId):
    logging.info(f"brokerplaceNewOrder")
    global clientssn
    query = ("SELECT ssn,funds FROM client where Id = %s")
    logging.info(f"{query}")
    cursor.execute(query, (clientId,))
    data = []
    for i in cursor:
        data.append((list(i)))
    clientssn = data[0][0]
    clientfunds = data[0][1]
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Avaliable funds of client : ", font=25),
            sg.Text(str(clientfunds) + " $", font=25)
        ],
        [
            sg.Text("Enter company ticker : ", font=25),
            sg.InputText(key='-symbol-', font=25),
        ],
        [
            sg.Button("Buy", size=(25, 1)),sg.Button("Sell", size=(25, 1))
        ]
    ]
    window = sg.Window("placeNewOrder", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                brokerLandingPage()
            if event == "Buy":
                window.close()
                brokerBuyShare(values['-symbol-'],clientfunds)
            if event == "Sell":
                window.close()
                brokersellShare(values['-symbol-'])


def brokersellShare(symbol):
    logging.info(f"brokersellShare")
    params = {
        'access_key': 'f5d7053a98721044c02228c1f607e55b',
        'symbols': symbol
    }
    api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
    api_response = api_result.json()
    logging.info(f"{api_response}")
    response = dict()
    response = api_response['data'][0]
    sg.theme('BluePurple')
    query = (
        "SELECT companysharecode,sum(quantity) FROM clientportfolio where clientssn = %s GROUP BY companysharecode")
    cursor.execute(query, (clientssn,))
    data = []
    for i in cursor:
        data.append((list(i)))
    header_list = ["Company Ticker", "Invested amount $"]
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  col_widths=[25, 25, 25],
                  justification="center",
                  size=(100, 1),
                  num_rows=min(100, len(data)))
         ],
        [
            sg.Text("Enter Company Ticker to sell : ", size=(40, 1), font=15),
            sg.InputText(key='-CompanyTicker-', size=(25, 1), font=15)
        ],
        [
            sg.Text("Quantity : ", size=(40, 1), font=15),
            sg.InputText(key='-quantity-', size=(25, 1), font=15)
        ],
        [
            sg.Button("Sell", size=(25, 1))
        ]
    ]
    window = sg.Window("brokersellShare", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                brokerLandingPage()
            elif event == "Sell":
                query = ("SELECT companysharecode,sum(quantity) FROM clientportfolio where clientssn = %s and brokerssn = %s and companysharecode = %s GROUP BY companysharecode")
                cursor.execute(query, (clientssn, brokerssn, values['-CompanyTicker-'],))
                data = []
                for i in cursor:
                    data.append((list(i)))
                avaliableQuantity = int(data[0][1])
                if (avaliableQuantity < int(values['-quantity-'])):
                    brokerdisplayErrorMessage("Please enter valid quantity")
                else:
                    window.close()
                    brokertransactionForSelling(values['-CompanyTicker-'], values['-quantity-'])

def brokertransactionForSelling(symbol,quantity):
    logging.info(f"brokertransactionForSelling")
    query = (
        "INSERT INTO placedorders(companysharecode, clientssn, brokerssn, quantity, status, type) VALUES(%s, %s, %s, %s, 'active', 'Sell')")
    cursor.execute(query, (symbol, clientssn, brokerssn, quantity))
    cnx.commit()
    brokerdisplayMessage("Your Sell order has been placed")

def brokerBuyShare(symbol,clientfunds):
    logging.info(f"brokerBuyShare")
    sg.theme('BluePurple')
    params = {
        'access_key': 'f5d7053a98721044c02228c1f607e55b',
        'symbols': symbol
    }
    api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
    api_response = api_result.json()
    logging.info(f"{api_response}")
    response = dict()
    response = api_response['data'][0]

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Available Funds : " + str(clientfunds) + " $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Company Share Code : ", size=(25, 1), font=15),
            sg.Text(response['symbol'], size=(25, 1), font=15)
        ],
        [
            sg.Text("Current Share Price: ", size=(25, 1), font=15),
            sg.Text(str((response['open'] + response['close']) / 2) + " $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Enter amount : ", size=(25, 1), font=15),
            sg.InputText(key='-amount-', size=(25, 1), font=15)
        ],
        [
            sg.Button("Buy", size=(25, 1))
        ]
    ]
    window = sg.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                brokerLandingPage()
            elif event == "Buy":
                value = int(values['-amount-'])
                if (value > clientfunds):
                    brokerdisplayErrorMessage("You don't have enough funds available to place order")
                else:
                    window.close()
                    brokertransactionForBuying(response['symbol'], value, ((response['open'] + response['close']) / 2),clientfunds)


def brokertransactionForBuying(symbol, value,currentprice,funds):
    logging.info(f"brokertransactionForBuying")
    query = ("Select * from company where sharecode = %s")
    cursor.execute(query, (symbol,))
    data = []
    for i in cursor:
        data = list(i)

    if((value/currentprice)<=data[3]):
        query = ("INSERT INTO placedorders(companysharecode, clientssn, brokerssn, quantity, currentprice, status, type) VALUES(%s, %s, %s, %s, %s, 'completed', 'Buy')")
        cursor.execute(query, (symbol, clientssn, brokerssn, value, currentprice))

        query = ("UPDATE Project2.client SET funds = %s WHERE(ssn = %s)")
        cursor.execute(query, ((funds-value), clientssn,))

        query = ("UPDATE Project2.company SET quantity = %s WHERE(sharecode = %s)")
        cursor.execute(query, ((data[3]-(value/currentprice)), symbol,))

        query = ("INSERT INTO trade(companyid, clientssn, brokerssn, quantity, purchasedprice) VALUES(%s, %s, %s, %s, %s)")
        cursor.execute(query, (data[0], clientssn, brokerssn, value, currentprice))

        query = ("INSERT INTO clientportfolio( clientssn, brokerssn, companyid, quantity, purchasedprice, companysharecode ) VALUES(%s,%s,%s,%s,%s,%s)")
        cursor.execute(query,(clientssn, brokerssn, data[0], value, currentprice, symbol))

        cnx.commit()
        brokerdisplayMessage("Trade has been completed")

    else:
        query = ("INSERT INTO placedorders(companysharecode, clientssn, brokerssn, quantity, currentprice, status, type) VALUES(%s, %s, %s, %s, %s, 'active', 'Buy')")
        cursor.execute(query, (symbol, clientssn, brokerssn, value, currentprice))

        query = ("UPDATE Project2.client SET funds = %s WHERE(ssn = %s)")
        cursor.execute(query, ((funds - value), clientssn,))

        cnx.commit()
        brokerdisplayMessage("Your order has been placed")

def brokerSearch():
    logging.info(f"brokerSearch")
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Search for company stock by share code : ", font=15),
            sg.InputText(key='-sharecode-', font=15),
            sg.Button("Search")
        ]
    ]
    window = sg.Window("Search", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event =="Menu":
                window.close()
                brokerLandingPage()
            elif event == "Search":
                value = str(values['-sharecode-'])
                if (len(value)>1):
                    window.close()
                    brokergetCurrentStockPrice(values['-sharecode-'])
                else:
                    window.close()
                    brokerdisplayMessage("Share code doesn't exist")

def brokerdisplayErrorMessage(error):
    logging.info(f"brokerdisplayErrorMessage")
    sg.theme('BluePurple')
    layout = [
        [
            sg.Text(error, font=15),
        ]
    ]
    window = sg.Window("displayErrorMessage", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

def brokerdisplayMessage(error):
    logging.info(f"brokerdisplayMessage")
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text(error, font=15),
        ]
    ]
    window = sg.Window("displayMessage", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                brokerLandingPage()

def brokergetCurrentStockPrice(symbol):
    logging.info(f"brokergetCurrentStockPrice")
    params = {
        'access_key': 'f5d7053a98721044c02228c1f607e55b',
        'symbols' : symbol
    }
    api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
    api_response = api_result.json()
    logging.info(f"{api_response}")
    response = dict()
    response = api_response['data'][0]
    sg.theme('BluePurple')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Company Share Code : ", size=(25, 1), font=15),
            sg.Text(response['symbol'], size=(25, 1), font=15)
        ],
        [
            sg.Text("Open at: ", size=(25, 1), font=15),
            sg.Text(str(response['open'])+" $", size=(25, 1), font=15)
        ],
        [
            sg.Text("High : ", size=(25, 1), font=15),
            sg.Text(str(response['high'])+" $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Low : ", size=(25, 1), font=15),
            sg.Text(str(response['low'])+" $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Closed at: ", size=(25, 1), font=15),
            sg.Text(str(response['close'])+" $", size=(25, 1), font=15)
        ]
    ]
    window = sg.Window("Search", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                brokerLandingPage()

def mainLandingPage():
    logging.info(f"mainLandingPage")
    sg.theme('LightBlue2')
    layout = [
        [sg.Button("Search", size=(15, 1))],
        [sg.Button("Place Order", size=(15, 1))],
        [sg.Button("View Portfolio", size=(15, 1))],
        [sg.Button("Add Funds", size=(15, 1))],
        [sg.Button("Log Out", size=(15, 1))]
    ]

    window = sg.Window("mainLandingPage", layout)

    while True:
        event, values = window.read()
        if event == 'Log Out' or event == sg.WIN_CLOSED:
            break
        elif event == 'Search':
            window.close()
            Search()
        elif event == 'Place Order':
            window.close()
            PlaceOrder()
        elif event == 'View Portfolio':
            window.close()
            ViewPortfolio()
        elif event == 'Add Funds':
            window.close()
            AddFunds()

def AddFunds():
    logging.info(f"AddFunds")
    sg.theme('LightBlue2')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Add funds to your account : ", font=15),
            sg.InputText(key='-funds-', font=15, size=(25, 1)),
        ],
        [sg.Button("Add", size=(15, 1))]
    ]
    window = sg.Window("AddFunds", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                mainLandingPage()
            elif event == "Add":
                funds = int(values['-funds-'])
                if(funds<0):
                    displayErrorMessage("Please add valid funds")
                else:
                    query = ("Select funds from Project2.customer WHERE ssn = %s")
                    cursor.execute(query, (customerssn,))
                    data= []
                    for i in cursor:
                        data = list(i)
                    query = ("UPDATE Project2.customer SET funds = %s WHERE ssn = %s")
                    cursor.execute(query, ((funds+data[0]),customerssn,))
                    cnx.commit()
                    displayErrorMessage("Funds have been added successfully!")

def ViewPortfolio():
    logging.info(f"ViewPortfolio")
    sg.theme('LightBlue2')
    query = ("SELECT companysharecode,quantity,purchasedprice FROM portfoliocustomer where customerssn = %s")
    cursor.execute(query, (customerssn,))

    data = []
    for i in cursor:
        data.append((list(i)))

    header_list = ["Company Ticker","Invested amount $","Purchased price $"]

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  col_widths=[25, 25, 25],
                  justification="center",
                  size=(100, 1),
                  num_rows=min(100, len(data)))]
    ]
    window = sg.Window("ViewPortfolio", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                mainLandingPage()

def PlaceOrder():
    logging.info(f"ViewPortfolio")
    sg.theme('LightBlue2')

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Button("Place new order", size=(25, 1)),sg.Button("Cancel existing order", size=(25, 1))
        ]
    ]
    window = sg.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                mainLandingPage()
            elif event == "Place new order":
                window.close()
                placeNewOrder()
            elif event == "Cancel existing order":
                window.close()
                cancelExistingOrder()

def placeNewOrder():
    sg.theme('LightBlue2')

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Button("Buy", size=(25, 1)),sg.Button("Sell", size=(25, 1))
        ]
    ]
    window = sg.Window("placeNewOrder", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                mainLandingPage()
            if event == "Buy":
                window.close()
                searchBuyShare()
            if event == "Sell":
                window.close()
                sellShare()

def searchBuyShare():
    sg.theme('LightBlue2')

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Search for company share you want to buy : ", font=15),
            sg.InputText(key='-sharecode-', font=15),
            sg.Button("Search")
        ]
    ]
    window = sg.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event =="Menu":
                window.close()
                mainLandingPage()
            elif event == "Search":
                window.close()
                if len(values['-sharecode-'])>1:
                    buyShare(values['-sharecode-'])
                else:
                    window.close()
                    displayMessage("Share code doesn't exist")

def buyShare(symbol):
    sg.theme('LightBlue2')
    query = ("SELECT * FROM customer where ssn = %s")
    cursor.execute(query, (customerssn,))

    data = []
    for i in cursor:
        data = (list(i))
    params = {
        'access_key': 'f5d7053a98721044c02228c1f607e55b',
        'symbols': symbol
    }
    api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
    api_response = api_result.json()
    logging.info(f"{api_response}")
    response = dict()
    response = api_response['data'][0]
    sg.theme('LightBlue2')

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Available Funds : " + str(data[3]) + " $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Company Share Code : ", size=(25, 1), font=15),
            sg.Text(response['symbol'], size=(25, 1), font=15)
        ],
        [
            sg.Text("Current Share Price: ", size=(25, 1), font=15),
            sg.Text(str((response['open']+response['close'])/2) + " $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Enter amount : ", size=(25, 1), font=15),
            sg.InputText(key='-amount-', size=(25, 1), font=15)
        ],
        [
            sg.Button("Buy", size=(25, 1))
        ]
    ]
    window = sg.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                mainLandingPage()
            elif event =="Buy":
                value = int(values['-amount-'])
                if(value>data[3]):
                    displayErrorMessage("You don't have enough funds available to place order")
                else:
                    window.close()
                    transactionForBuying(response['symbol'],value,((response['open']+response['close'])/2),data[3])


def transactionForBuying(symbol, value,currentprice,funds):
    args = [symbol, value, currentprice, int(funds),customerssn]
    query = ("Select * from company where sharecode = %s")
    cursor.execute(query, (symbol,))
    data = []
    for i in cursor:
        data = list(i)
    if((value/currentprice)<=data[3]):
        cursor.callproc('transaction_for_buying', args)
        cnx.commit()
        displayMessage("Trade has been completed")
    else:
        cursor.callproc('transaction_for_buying', args)
        cnx.commit()
        displayMessage("Your order has been placed")


def displayErrorMessage(error):
    sg.theme('LightBlue2')
    layout = [
        [
            sg.Text(error, font=15),
        ]
    ]
    window = sg.Window("displayErrorMessage", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

def sellShare():
    sg.theme('LightBlue2')
    query = ("SELECT companysharecode,sum(quantity) FROM portfoliocustomer where customerssn = %s GROUP BY companysharecode")
    cursor.execute(query, (customerssn,))
    data = []
    for i in cursor:
        data.append((list(i)))

    header_list = ["Company Ticker","Invested amount $"]

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  col_widths=[25, 25, 25],
                  justification="center",
                  size=(100, 1),
                  num_rows=min(100, len(data)))
        ],
        [
            sg.Text("Enter Company Ticker to sell : ", size=(40, 1), font=15),
            sg.InputText(key='-CompanyTicker-', size=(25, 1), font=15)
        ],
        [
            sg.Text("Quantity : ", size=(40, 1), font=15),
            sg.InputText(key='-quantity-', size=(25, 1), font=15)
        ],
        [
            sg.Button("Sell", size=(25, 1))
        ]
    ]
    window = sg.Window("sellShare", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                mainLandingPage()
            elif event == "Sell":

                query = (
                    "SELECT companysharecode,sum(quantity) FROM portfoliocustomer where customerssn = %s and companysharecode = %s GROUP BY companysharecode")
                cursor.execute(query, (customerssn, values['-CompanyTicker-'],))
                data = []
                for i in cursor:
                    data.append((list(i)))
                avaliableQuantity = int(data[0][1])
                if (avaliableQuantity < int(values['-quantity-'])):
                    displayErrorMessage("Please enter valid quantity")
                else:
                    window.close()
                    transactionForSelling(values['-CompanyTicker-'],values['-quantity-'])

# //Transaction for selling
def transactionForSelling(symbol,quantity):
    query = (
        "INSERT INTO placedorders(companysharecode, customerssn, quantity, status, type) VALUES(%s, %s, %s, 'active', 'Sell')")
    cursor.execute(query, (symbol, customerssn, quantity))
    cnx.commit()
    displayMessage("Your Sell order has been placed")


def cancelExistingOrder():
    sg.theme('LightBlue2')
    query = ("SELECT * FROM placedorders where customerssn = %s and status = %s ")
    cursor.execute(query, (customerssn,'active',))
    data = []

    for i in cursor:
        data.append(list(i))

    header_list = ['id', 'companysharecode', 'customerssn','clientssn','brokerssn','quantity', 'currentprice', 'status', 'type']

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  size=(15,1),
                  num_rows=min(25, len(data)))],
        [
            sg.Text("Enter Order Id that you want to cancel : ", size=(40, 1), font=15),
            sg.InputText(key='-OrderId-', size=(25, 1), font=15)
        ],
        [
            sg.Button("Cancel", size=(25, 1))
        ]

    ]
    window = sg.Window("cancelExistingOrder", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Menu":
                window.close()
                mainLandingPage()
            if event == "Cancel":
                window.close()
                query = ("UPDATE Project2.placedorders SET status = 'cancelled' WHERE id = "+values['-OrderId-']+"")
                cursor.execute(query)
                cnx.commit()
                displayMessage("Your order"+ str(values['-OrderId-']) +" has been successfully cancelled")


def displayMessage(error):
    sg.theme('LightBlue2')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text(error, font=15),
        ]
    ]
    window = sg.Window("displayMessage", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                mainLandingPage()

def Search():
    sg.theme('LightBlue2')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Search for company stock by share code : ", font=15),
            sg.InputText(key='-sharecode-', font=15),
            sg.Button("Search")
        ]
    ]
    window = sg.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event =="Menu":
                window.close()
                mainLandingPage()
            elif event == "Search":
                value = str(values['-sharecode-'])
                if (len(value)>1):
                    window.close()
                    getCurrentStockPrice(values['-sharecode-'])
                else:
                    window.close()
                    displayMessage("Share code doesn't exist")

def getCurrentStockPrice(symbol):
    params = {
        'access_key': 'f5d7053a98721044c02228c1f607e55b',
        'symbols' : symbol
    }
    api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)
    api_response = api_result.json()
    logging.info(f"{api_response}")
    response = dict()
    response = api_response['data'][0]
    sg.theme('LightBlue2')

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Company Share Code : ", size=(25, 1), font=15),
            sg.Text(response['symbol'], size=(25, 1), font=15)
        ],
        [
            sg.Text("Open at: ", size=(25, 1), font=15),
            sg.Text(str(response['open'])+" $", size=(25, 1), font=15)
        ],
        [
            sg.Text("High : ", size=(25, 1), font=15),
            sg.Text(str(response['high'])+" $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Low : ", size=(25, 1), font=15),
            sg.Text(str(response['low'])+" $", size=(25, 1), font=15)
        ],
        [
            sg.Text("Closed at: ", size=(25, 1), font=15),
            sg.Text(str(response['close'])+" $", size=(25, 1), font=15)
        ]
    ]
    window = sg.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                mainLandingPage()

def create_account():
    sg.theme('LightBlue2')
    layout = [[sg.Text("Already have an account?, click continue!", font=40)],
              [sg.Text("E-mail", size=(15, 1), font=15), sg.InputText(key='-email-', font=15)],
              [sg.Text("Re-enter E-mail", size=(15, 1), font=15), sg.InputText(key='-remail-', font=15)],
              [sg.Text("Enter First Name", size=(15, 1), font=15), sg.InputText(key='-fname-', font=15)],
              [sg.Text("Enter Last Name", size=(15, 1), font=15), sg.InputText(key='-lname-', font=15)],
              [sg.Text("Enter SSN", size=(15, 1), font=15),
               sg.InputText(key='-ssn-', font=15, password_char='*')],
              [sg.Text("Create Password", size=(15, 1), font=15),
               sg.InputText(key='-password-', font=15, password_char='*')],
              [sg.Button("Submit"), sg.Button("Cancel"),sg.Button("Continue")]]

    window = sg.Window("Sign Up", layout)

    while True:
        event, values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Submit":
                epassword = hashlib.md5((values['-password-']).encode("utf-8")).hexdigest()
                sql = "INSERT INTO customer (fname, lname, email, funds, ssn, password) VALUES(%s, %s, %s, %s, %s, %s)"
                val = (values['-fname-'],values['-lname-'],values['-email-'],None,values['-ssn-'],epassword)
                cursor.execute(sql, val)
                cnx.commit()

                cnx.commit()
                if values['-email-'] != values['-remail-']:
                    sg.popup_error("Error", font=15)
                    continue
                elif values['-email-'] == values['-remail-']:
                    progress_bar()
                    window.close()
                    login()
            if event == "Continue":
                window.close()
                login()
        window.close()

def brokercreate_account():
    sg.theme('BluePurple')
    layout = [[sg.Text("Already have an account?, click continue!", font=40)],
              [sg.Text("E-mail", size=(15, 1), font=15), sg.InputText(key='-email-', font=15)],
              [sg.Text("Re-enter E-mail", size=(15, 1), font=15), sg.InputText(key='-remail-', font=15)],
              [sg.Text("Enter First Name", size=(15, 1), font=15), sg.InputText(key='-fname-', font=15)],
              [sg.Text("Enter Last Name", size=(15, 1), font=15), sg.InputText(key='-lname-', font=15)],
              [sg.Text("Enter SSN", size=(15, 1), font=15),
               sg.InputText(key='-ssn-', font=15, password_char='*')],
              [sg.Text("Create Password", size=(15, 1), font=15),
               sg.InputText(key='-password-', font=15, password_char='*')],
              [sg.Button("Submit"), sg.Button("Cancel"),sg.Button("Continue")]]

    window = sg.Window("Sign Up", layout)

    while True:
        event, values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Submit":
                if values['-email-'] != values['-remail-']:
                    sg.popup_error("Error", font=15)
                    continue
                elif values['-email-'] == values['-remail-']:
                    epassword = hashlib.md5((values['-password-']).encode("utf-8")).hexdigest()
                    sql = "INSERT INTO broker (fname, lname, email, ssn, password) VALUES(%s, %s, %s, %s, %s)"
                    val = (values['-fname-'], values['-lname-'], values['-email-'], values['-ssn-'], epassword)
                    cursor.execute(sql, val)
                    cnx.commit()
                    brokerprogress_bar()
                    window.close()
                    brokerlogin()
            if event == "Continue":
                window.close()
                brokerlogin()
        window.close()

def brokerlogin():
    global brokerssn
    sg.theme("BluePurple")
    layout = [[sg.Text("Log In", size=(15, 1), font=40)],
              [sg.Text("Email", size=(15, 1), font=16), sg.InputText(key='-email-', font=15)],
              [sg.Text("Password", size=(15, 1), font=16), sg.InputText(key='-pwd-', password_char='*', font=15)],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                epassword = hashlib.md5((values['-pwd-']).encode("utf-8")).hexdigest()
                esql = ("SELECT email,password,ssn from broker where email = %s and password = %s")
                evals = (values['-email-'], epassword)
                cursor.execute(esql, evals)
                myresult = cursor.fetchall()
                if values['-email-'] == myresult[0][0] and epassword == myresult[0][1] and values['-email-'] != '':
                    window.close()
                    brokerssn = myresult[0][2]
                    brokerLandingPage()


def login():
    global customerssn
    sg.theme("LightBlue2")
    layout = [[sg.Text("Log In", size=(15, 1), font=40)],
              [sg.Text("Email", size=(15, 1), font=16), sg.InputText(key='-email-', font=15)],
              [sg.Text("Password", size=(15, 1), font=16), sg.InputText(key='-pwd-', password_char='*', font=15)],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                epassword = hashlib.md5((values['-pwd-']).encode("utf-8")).hexdigest()
                esql = ("SELECT email,password,ssn from customer where email = %s and password = %s")
                evals=(values['-email-'], epassword)
                cursor.execute(esql, evals)
                myresult = cursor.fetchall()
                if values['-email-'] == myresult[0][0] and epassword == myresult[0][1] and values['-email-'] != '' :
                    window.close()
                    customerssn = myresult[0][2]
                    mainLandingPage()

def progress_bar():
    sg.theme('LightBlue2')
    layout = [[sg.Text('Creating your account...')],
              [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
              [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()

def brokerprogress_bar():
    sg.theme('BluePurple')
    layout = [[sg.Text('Creating your account...')],
              [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
              [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()

def start():
    logging.info("Started At the Main Page")
    sg.theme('LightBlue')
    layout = [[sg.Button("Broker" , size=(20, 1))], [sg.Button("Customer", size=(20, 1))], [sg.Button("Admin", size=(20, 1))],[sg.Button('Quit', size=(20, 1))]]

    window = sg.Window("start", layout)

    while True:
        event, values = window.read()
        if event == 'Quit' or event == sg.WIN_CLOSED:
            break
        elif event == 'Customer':
            window.close()
            create_account()
        elif event == 'Broker':
            window.close()
            brokercreate_account()
        elif event == 'Admin':
            window.close()
            adminlogin()

def adminlogin():
    logging.info("Entered Admin login")
    sg.theme("LightBlue4")
    layout = [[sg.Text("Log In", size=(15, 1), font=40)],
              [sg.Text("Email", size=(15, 1), font=16), sg.InputText(key='-email-', font=15)],
              [sg.Text("Password", size=(15, 1), font=16), sg.InputText(key='-pwd-', password_char='*', font=15)],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                # CMPE226Project2Team4
                epassword = hashlib.md5((values['-pwd-']).encode("utf-8")).hexdigest()
                if values['-email-'] == "admin@hotmail.com" and epassword == "2a628be9bcdf1a86424275c70a949e67" :
                    window.close()
                    adminLandingPage()

def adminLandingPage():
    logging.info("Started admin dashboard Page")
    sg.theme("LightBlue4")
    layout = [
        [sg.Button("View all trades", size=(15, 1))],
        [sg.Button("View placed orders", size=(15, 1))],
        [sg.Button("Add Company", size=(15, 1))],
        [sg.Button("Log Out", size=(15, 1))]
    ]
    window = sg.Window("brokerLandingPage", layout)
    while True:
        event, values = window.read()
        if event == 'Log Out' or event == sg.WIN_CLOSED:
            break
        elif event == 'View all trades':
            window.close()
            Viewalltrades()
        elif event == 'Add Company':
            window.close()
            AddCompany()
        elif event == 'View placed orders':
            window.close()
            Viewplacedorders()


def AddCompany():
    logging.info("Admin can add compaines")
    sg.theme('LightBlue4')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text("Company Id :", font=40),
            sg.InputText(key='-CompanyId-', font=40)
        ],
        [
            sg.Text("Company Share Code :", font=40),
            sg.InputText(key='-CompanyShareCode-', font=40)
        ],
        [
            sg.Text("Company Name :", font=40),
            sg.InputText(key='-name-', font=40)
        ],
        [
            sg.Text("Quantity :", font=40),
            sg.InputText(key='-Quantity-', font=40)
        ],
        [
            sg.Text("Email :", font=40),
            sg.InputText(key='-Email-', font=40)
        ],
        [
            sg.Text("Address :", font=40),
            sg.InputText(key='-Address-', font=40)
        ],
        [
            sg.Button("Add company")
        ]
    ]
    window = sg.Window("Select", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                adminLandingPage()
            elif event == "Add company":
                window.close()
                query = ("INSERT INTO company(id,sharecode,name,quantity,email,address) VALUES (%s,%s,%s,%s,%s,%s)")
                cursor.execute(query, (values['-CompanyId-'],values['-CompanyShareCode-'],values['-name-'],int(values['-Quantity-']),values['-Email-'],values['-Address-']))
                cnx.commit()
                admindisplayMessage("Company has been added")

def Viewalltrades():
    logging.info("Admin viewing All trades.")
    cursor.callproc('view_all_placed_orders')
    data = []
    for result in cursor.stored_results():
        data = result.fetchall()
    result = []
    for li in data:
        result.append(list(li))
    logging.info(f"viewing All trades {result}")

    header_list = ['Trade id', 'Company id', 'Quantity']
    sg.theme('LightBlue4')

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  size=(15, 1),
                  num_rows=min(25, len(data)))],
    ]
    window = sg.Window("cancelExistingOrder", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        elif event =='Menu':
            window.close()
            adminLandingPage()



def admindisplayMessage(error):
    sg.theme('LightBlue4')
    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [
            sg.Text(error, font=15),
        ]
    ]
    window = sg.Window("displayMessage", layout)
    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        else:
            if event == 'Log Out' or event == sg.WIN_CLOSED:
                break
            elif event == "Menu":
                window.close()
                adminLandingPage()

def test():
    cursor.callproc('view_all_placed_orders')
    for result in cursor.stored_results():
        print(result.fetchall())



def Viewplacedorders():
    cursor.callproc('view_all_placed_orders')
    data = []
    for result in cursor.stored_results():
        data = result.fetchall()
    result = []
    for li in data:
        result.append(list(li))

    header_list = ['Trade id', 'Company Share Code', 'Quantity', 'Purchased Price']
    sg.theme('LightBlue4')
    logging.info("Admin placing All trades.")
    logging.info(f"placing All trades {result}")

    layout = [
        [
            sg.Button("Menu", size=(15, 1)),
            sg.Button("Logout", size=(15, 1))
        ],
        [sg.Table(values=data,
                  headings=header_list,
                  auto_size_columns=False,
                  size=(15, 1),
                  num_rows=min(25, len(data)))],
    ]
    window = sg.Window("cancelExistingOrder", layout)

    while True:
        event, values = window.read()
        if event == 'Logout' or event == sg.WIN_CLOSED:
            break
        elif event == 'Menu':
            window.close()
            adminLandingPage()



if __name__ == '__main__':
    brokerssn = 0
    customerssn = 0
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(start())
