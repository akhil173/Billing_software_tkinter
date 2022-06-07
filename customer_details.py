# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 11:43:43 2022

@author: akhil
"""

from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector as connector
from datetime import date
import pandas as pd
# from pandas_tkinter import TestApp
from tkinter import ttk
from sql_init import sql_login
from functools import partial  


def View():

    cur.execute("SELECT * FROM customer;")

    rows = cur.fetchall()    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)
        
def customers(root):
    global con, cur, child, tree
    
    child = Toplevel(root)
    child.geometry('620x400')
    child.title('Customer List')
    # child.state('zoomed')
    con = sql_login().login()
    cur = con.cursor()

    tree = ttk.Treeview(child, column=("c1", "c2", "c3"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="CUSTOMER ID")
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="CUSTOMER NAME")

    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="CUSTOMER EMAIL")
    
    tree.pack()
    
    button1 = Button(child, text="Display data", command=View)
    button1.place(relx=0.2, rely=0.7)

    button2 = Button(child, text="Add / Modify Customer", command=add_cust)
    button2.place(relx=0.6, rely=0.7)
    
    # child.mainloop()

def add_cust():
    # global id_input, name_input
    
    new = Toplevel(child)
    new.geometry('580x250')
    
    id_input = StringVar()  
    name_input = StringVar()
    email_input = StringVar()
    
    cust_id = Label(new, text = "Customer id : ").place(x = 20, y = 30)
    cust_name = Label(new, text = "Customer Name : ").place(x = 20, y = 60)
    cust_email = Label(new, text = "Customer Email : ").place(x = 20, y = 90)
    
    inp_id = Entry(new, textvariable=id_input, width = 15).place(x = 150, y = 30)
    inp_name = Entry(new, textvariable=name_input, width = 15).place(x = 150, y = 60)
    inp_email = Entry(new, textvariable=email_input, width = 15).place(x = 150, y = 90)
    
    call_result = partial(add_cust_to_db, new, id_input, name_input, email_input)
    
    button = Button(new, text="Add / Modify Customer in Database", command=call_result)
    button.place(x=70, y=140)
    
def add_cust_to_db(root, id_ip, name_ip, email_ip):
    cust_id = id_ip.get()
    cust_name = name_ip.get()
    cust_email = email_ip.get()
    cur.execute("select * from customer")
    id_list = [ids[0] for ids in cur.fetchall()]
    if cust_name == '' or cust_id == '' or cust_email == '':
        messagebox.showinfo("Error","Customer ID, Name and Email Fields can't be empty")
    elif int(cust_id) in id_list:
        modify_cust(cust_id, cust_name, cust_email)
        root.destroy()
    else:
        try:
            sql="insert into customer(cust_id, cust_name, cust_email) values({},'{}','{}');".format\
                (cust_id,cust_name,cust_email)
            cur.execute(sql)
            con.commit()
            messagebox.showinfo('Success',"Added Customer Succesfully ")
            root.destroy()
        except:
            messagebox.showinfo("Error","Could'nt add Customer to Database")
            
def modify_cust(c_id, c_name, c_email):
    answer = messagebox.askyesno(title='Customer Details Modification',\
        message='There is a customer with this ID, Are you sure you want to modify the Cutsomer details\
        of the customer with Customer id = '+c_id+'?')
    
    if answer:
        sql = 'update customer set cust_name = "{}", cust_email ="{}" where cust_id={}'.format(c_name,c_email,c_id)
        cur.execute(sql)
        con.commit()
