# Stock-Management-Application
Stock Management Application ( Database Management System )

Database Project Topic

●	App for stock market transaction system that allows users to buy and sell stocks.
●	Users are allowed to post a buy or sell information in the database.
●	When a buy matches a sell price, the name of stocks, the system will create trade.
●	The system also allows users to cancel a buy or sell, search for stocks.
●	Which also helps users with Financial Planning and Advice, Retirement Plans, Wealth Management Services, Trading and Brokerage services.


# Database technologies and tools

Database engine :	Mysql (mysql database hosted on digital ocean)
DB application technologies :	mysql.connector
Frameworks : PySimpleGUI
Languages : Python, Mysql
DB access technology : mysql.connector
Libraries : Requests, mysql.connector, PySimpleGUI


# List of functionalities of each role

## Admin:
1. Admin can login through the admin sign in page.
2. Admin can view daily trades that are completed, or pending.
3. Admin gives access to users based on their user types. (not implemented seemed irrelevant to application)
4. Admin put stocks for sale for different companies.
5. Admin approves the cash transfer from external account to customer account in Miniworld and vice versa. ( not implemented )

## Customer:
1.	Customers can login through the customer sign in page.
2.	Customers can add funds to their account balance through transfer.
3.	Customers can search for stock portfolios of different companies.
4.	Customers can always view their current stock portfolios.
5.	Customers can place orders which do not expire, or sell the shares for the market price and cancel orders for particular stocks using funds from their account balance.

## Broker:
1.	Brokers can login through the broker sign in page.
2.	Brokers can search for stock portfolios of different companies.
3.	Brokers can always view their clients current stock portfolios.
4.	Brokers help place orders which do not expire or sell the shares for the market price and cancel orders for clients.
