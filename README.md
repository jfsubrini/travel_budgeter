# travel_budgeter

Program developed and deployed by Jean-François Subrini, January 2020.



## What the project is for ?

* **TRAVELGET** or **TRAVEL_BUDGETER** allows you to manage your travel budget.
* First you create your **account** with just your username and email.
* Second, you fill up a **draft** form to define your travel budget. Here, you will set among other, the maximum amount of money you are able to spend by category (9 categories). In the future, you can modify this draft, for example if you want to change the planned amount for one category.  
* Third, after submitting the form, you need to create **wallets**. These are portfolios like credit cards, mere wallets, etc., with a precise currency attached. In the future, when you are going to make expenses, you will need to refer to a specific wallet, with the right attached currency. These wallets will allow you to pay, withdraw money or change a currency. In the future, you can modify a wallet, for example if you want to add a credit, by changing the initial balance.
* Finally, when you are going to spend money for the travel (before leaving or during the journey) your will fill up an **expense** form with all the information about it. Note that you can ***simulate*** an expense in order to check if this desired expense is feasible and won't kill your travel budget. You can also **change** money from one currency to the other, the money leaving one wallet to another one. And of course you can **withdraw** money from an ATM or a GAB and affect this amount to a specific wallet.
* The beauty of the app is, of course, the possibility to display all kind of data about the **travel money consumption** during your journey, since the beggining, the last 7 days or only for one day (today). **This is very useful to check if the expenses are in line with the draft : globally or by category**. The **expense list** can also be seen, with access to the bill photo if you saved one. You can also **delete all the simulation** done previously. Finally, you can **consult the balance for each wallet**.
* *This version of the app* is a **POC** (Proof Of Concept) and is not intended to be nice, pretty or user friendly. It's only to demonstrate the efficiency of the app and needs to be develop with the front-end side in the future, and also as a smartphone app.


## How to use it or get it running ?

* The **TRAVELGET** or **TRAVEL_BUDGETER** is a **Python app**, developed with the **Django** framework 2.2.5, Python 3.8.0 and PostgreSQL for the backend (see *requirements.txt*), and with only a very basic HTML code for the frontend.

* You can access the program from your Terminal, executing *./manage.py runserver* and watching it from your *localhost:8000* in your favorite browser.

* You can also and more easily go directly online at the **[TRAVELGET](https://travel-budgeter.herokuapp.com/)** website, deployed with ***Heroku***.


***Enjoy it !***
