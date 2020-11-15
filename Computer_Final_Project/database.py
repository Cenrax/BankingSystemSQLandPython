# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 03:26:13 2020

@author: SUBHAM KUNDU
"""

__author__ = 'user'

import datetime
from classes import Customer,Account,Savings,Current,Fixed_Deposit,Address
from connection import con,cur

def make_all_tables():
    sql = "SELECT COUNT(*) FROM customers"
    cur.execute(sql)
    res = cur.fetchall()
    print(res[0][0])
    if res[0][0] == 0: #MY_SQL --> NUMBER[20], VARCHAR[40], DATE
        print('a')
        return
    sql = """CREATE TABLE customers(  
                  customer_id INTEGER NOT NULL PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  status TEXT,
                  login_attempts INTEGER,
                  password TEXT NOT NULL)"""
                  
    cur.execute(sql)

    sql = """create table address(
                  customer_id INTEGER NOT NULL,
                  line1 TEXT,
                  line2 TEXT,
                  city TEXT,
                  state TEXT,
                  pincode INTEGER NOT NULL,
                  FOREIGN KEY (customer_id)
                      REFERENCES customers (customer_id)
                  )"""
    cur.execute(sql)

    sql = """create table accounts(
                  customer_id INETGER,
                  account_no INTEGER NOT NULL PRIMARY KEY,
                  opened_on TEXT,
                  account_type TEXT,
                  status TEXT,
                  balance INTEGER,
                  withdrawals_left INTEGER,
                  next_reset_date date,
                  FOREIGN KEY (customer_id)
                      REFERENCES customers (customer_id)
                  )"""
    cur.execute(sql)

    sql = """create table fd(
                  account_no INTEGER NOT NULL PRIMARY KEY,
                  amount INETEGER,
                  deposit_term INTEGER,
                  FOREIGN KEY (customer_id)
                      REFERENCES customers (customer_id)
                  )"""
    cur.execute(sql)

    sql = """create table_loans(
                  customer_account_no INTEGER,
                  loan_id INTEGER NOT NULL PRIMARY KEY,
                  loan_amount INTEGER,
                  repay_term INTEGER,
                  FOREIGN KEY (customer_id)
                      REFERENCES customers (customer_id)
                  )"""
    cur.execute(sql)

    sql = """create table transactions(
                  transaction_id INTEGER NOT NULL PRIMARY KEY,
                  account_no INTEGER,
                  type TEXT,
                  amount INTEGER,
                  balance INTEGER,
                  transaction_date TEXT,
                  FOREIGN KEY (customer_id)
                      REFERENCES customers (customer_id)
                  )"""
    cur.execute(sql)

    sql = """create table admin(
                  admin_id INTEGER,
                  password TEXT)"""
    cur.execute(sql)

    sql = """create table closed_accounts(
                  account_no INTEGER,
                  closed_on TEXT,
                  FOREIGN KEY (customer_id)
                      REFERENCES customers (customer_id)
                  )"""
                 
    cur.execute(sql)

    sql = """create or replace view accounts_fd as
                select a.customer_id,a.account_no,fd.amount,fd.deposit_term from accounts a,fd where a.account_no = fd.account_no"""
    cur.execute(sql)

    sql = """create or replace view accounts_loans as
                select a.customer_id,a.account_no,loans.loan_id,loans.loan_amount,loans.repay_term from accounts a,loans
                where a.account_no = loans.customer_account_no"""
    cur.execute(sql)

    sql = """create sequence customer_id_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = """create sequence account_no_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = """create sequence transaction_id_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = """create sequence loan_id_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = "insert into admin values(227,'helloadmin')"
    cur.execute(sql)

    con.commit()

def sign_up_customer(customer):
    fname = customer.get_first_name()
    lname = customer.get_last_name()
    password = customer.get_password()
    sql = "select customer_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    id = res[0][0]
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "insert into customers values(:id,:fname,:lname,:status,:att,:password)"
    cur.execute(sql, {"id":id, "fname":fname, "lname":lname , "password":password, "status":status, "att":att})
    line1 = customer.get_addr_line1()
    line2 = customer.get_addr_line2()
    city = customer.get_addr_city()
    state = customer.get_addr_state()
    pincode = customer.get_addr_pincode()
    sql = "insert into address values(:id,:line1,:line2,:city,:state,:pincode)"
    cur.execute(sql, {"id":id, "line1":line1, "line2":line2, "city":city, "state":state, "pincode":pincode} )
    con.commit()
    print("Congratulations ! Your Account was Created Successfully")
    print("Your Customer ID : ",id)

def login_customer(id,password):
    sql = "select count(*) from customers where customer_id = :id and password = :password"
    cur.execute(sql, {"id":id, "password":password})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def open_new_account_customer(account,cus_id):
    withdrawals_left = None
    account_type = account.get_account_type()
    bal = account.get_balance()
    opened_on = datetime.datetime.now().strftime("%d-%b-%Y")
    status = "open"
    sql = "select account_no_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    acc_no = res[0][0]
    if account_type == "savings":
        withdrawals_left = 10
    sql = "select add_months(sysdate,1) from dual"
    cur.execute(sql)
    res = cur.fetchall()
    next_date = res[0][0].strftime("%d-%b-%Y")
    sql = "insert into accounts values(:cus_id,:acc_no,:opened_on,:acc_type,:status,:bal,:wd,:next_date)"
    cur.execute(sql , {"cus_id":cus_id, "acc_no":acc_no, "opened_on":opened_on, "acc_type":account_type, "status":status, "bal":bal, "wd":withdrawals_left, "next_date":next_date})
    if account_type == "fd":
        term = account.get_deposit_term()
        sql = "insert into fd values (:acc_no,:amount,:term)"
        cur.execute(sql, {"acc_no":acc_no, "term":term, "amount":bal})

    con.commit()
    print("Account Opened Successfully")
    print("Account No is : ",acc_no)



def change_address_customer(ch,id,addr):
    if ch == 1:
        sql = "update address set line1 = :line1 where customer_id = :id"
        cur.execute(sql, {"line1":addr, "id":id})

    elif ch == 2:
        sql = "update address set line2 = :line2 where customer_id = :id"
        cur.execute(sql, {"line2":addr, "id":id})

    elif ch == 3:
        sql = "update address set state = :state where customer_id = :id"
        cur.execute(sql, {"state":addr, "id":id})

    elif ch == 4:
        sql = "update address set city = :city where customer_id = :id"
        cur.execute(sql, {"city":addr, "id":id})

    elif ch == 5:
        sql = "update address set pincode = :pincode where customer_id = :id"
        cur.execute(sql, {"pincode":addr, "id":id})

    else:
        return

    con.commit()
    print("Details Updated Successfully")

def get_all_info_customer(id):
    sql = "select * from customers where customer_id = :id"
    cur.execute(sql, {"id":id})
    res = cur.fetchall()
    if len(res) == 0:
        return None
    customer = Customer()
    status = res[0][3]
    att = res[0][4]
    customer.set_customer_id(id)
    customer.set_status(status)
    customer.set_login_attempts(att)
    return customer

def get_all_info_account(acc_no,id,msg):
    account = None
    sql = None
    if msg == "transfer":
        sql = "select * from accounts where account_no = :acc_no and account_type != 'fd' and status = 'open'"
        cur.execute(sql, {"acc_no":acc_no})
    elif msg == "loan":
        sql = "select * from accounts where account_no = :acc_no and customer_id = :id and account_type = 'savings' and status = 'open'"
        cur.execute(sql, {"id":id ,"acc_no":acc_no})
    else:
        sql = "select * from accounts where account_no = :acc_no and customer_id = :id and account_type != 'fd' and status = 'open'"
        cur.execute(sql, {"acc_no":acc_no, "id":id})

    res = cur.fetchall()
    if len(res) == 0:
        return None

    account_no = res[0][1]
    account_type = res[0][3]
    balance = res[0][5]
    wd_left = res[0][6]
    if account_type == "savings":
        account = Savings()
    else:
        account = Current()

    account.set_account_type(account_type)
    account.set_balance(balance)
    account.set_account_no(account_no)
    account.set_withdrawals_left(wd_left)
    return account


def money_deposit_customer(account,amount):
    bal = account.get_balance()
    acc_no = account.get_account_no()
    type = "credit"
    sql = "update accounts set balance = :bal where account_no = :acc_no"
    cur.execute(sql , {"bal":bal, "acc_no":acc_no})
    sql = "select transaction_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    t_id = res[0][0]
    sql = "insert into transactions values (:t_id,:acc_no,:type,:amount,:bal,:date_on)"
    date = datetime.datetime.now().strftime("%d-%b-%Y")
    cur.execute(sql , {"t_id":t_id, "acc_no":acc_no, "type":type , "amount":amount , "bal":bal, "date_on":date})
    con.commit()

def money_withdraw_customer(account,amount,msg):
    acc_type = account.get_account_type()
    wd_left = account.get_withdrawals_left()
    bal = account.get_balance()
    acc_no = account.get_account_no()
    type = "debit"
    sql = "update accounts set balance = :bal where account_no = :acc_no"
    cur.execute(sql , {"bal":bal, "acc_no":acc_no})
    sql = "select transaction_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    t_id = res[0][0]
    sql = "insert into transactions values (:t_id,:acc_no,:type,:amount,:bal,:date_on)"
    date = datetime.datetime.now().strftime("%d-%b-%Y")
    cur.execute(sql , {"t_id":t_id ,"acc_no":acc_no, "type":type , "amount":amount , "bal":bal, "date_on":date })
    if acc_type == "savings" and msg != "transfer":
        wd_left -= 1
        sql = "update accounts set withdrawals_left = :wd_left where account_no = :acc_no"
        cur.execute(sql, {"wd_left":wd_left, "acc_no":acc_no})
    con.commit()

def get_transactions_account(acc_no,date_from,date_to):
    sql = """select transaction_date,type,amount,balance from transactions where account_no = :acc_no
              and transaction_date between :date_from and :date_to order by transaction_id"""
    cur.execute(sql, {"acc_no":acc_no, "date_from":date_from, "date_to":date_to})
    res = cur.fetchall()
    return res

def transfer_money_customer(account_sender,account_receiver,amount):
    if account_sender.withdraw(amount) == True:
        account_receiver.deposit(amount)
        money_withdraw_customer(account_sender,amount,"transfer")
        money_deposit_customer(account_receiver,amount)
        print("Transfer Completed !")
        print("New Balance for Account No ",account_sender.get_account_no()," : ",account_sender.get_balance())
        print("New Balance for Account No ",account_receiver.get_account_no()," : ",account_receiver.get_balance())


def login_admin(id,password):
    sql = "select count(*) from admin where admin_id = :id and password = :password"
    cur.execute(sql , {"id":id, "password":password})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def close_account_customer(account):
    acc_no = account.get_account_no()
    balance = account.get_balance()
    sql = "update accounts set status='closed',balance = 0 where account_no = :acc_no"
    cur.execute(sql, {"acc_no":acc_no})
    closed_on = datetime.datetime.now().strftime("%d-%b-%Y")
    sql = "insert into closed_accounts values(:acc_no,:closed_on)"
    cur.execute(sql, {"acc_no":acc_no, "closed_on":closed_on})
    print("Account Closed Successfully !")
    print("Rs ",balance," will be delivered to your address shortly")
    con.commit()

def get_loan_customer(acc_no,loan_amt,loan_term):
    sql = "select loan_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    loan_id = res[0][0]
    sql = "insert into loans values (:acc_no,:loan_id,:amount,:loan_term)"
    cur.execute(sql , {"acc_no":acc_no, "loan_id":loan_id, "loan_term":loan_term, "amount":loan_amt})
    con.commit()
    print("Loan Availed Successfully")

def reset_withdrawals():
    sql = """update accounts set withdrawals_left = 10,next_reset_date = add_months(next_reset_date,1)
              where account_type = 'savings' and sysdate >= next_reset_date"""
    cur.execute(sql)
    con.commit()

def reset_login_attempts(id):
    sql = "update customers set login_attempts = 3 where customer_id = :id"
    cur.execute(sql,{"id":id})
    con.commit()

def update_customer(customer):
    id = customer.get_customer_id()
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "update customers set status = :status,login_attempts = :att where customer_id = :id"
    cur.execute(sql, {"status":status, "att":att, "id":id})
    con.commit()





