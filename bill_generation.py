# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 09:28:50 2022

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
# import customer_details as c_fun
# import store_details as s_fun
from functools import partial
from sql_init import sql_login


def bill_generate():
    
    amount = 0
    today = str(date.today())
    no = cust_no.get()
    store = store_no.get()
    
    cur.execute("select * from customer;")
    cust_det = cur.fetchall()
    no_list = [cust[0] for cust in cust_det]
    
    cur.execute("select * from store")
    store_list = [s[0] for s in cur.fetchall()]
    
    if no == '' or store == '':
        messagebox.showinfo("Error","Customer Number and Store ID Fields can't be empty")
    
    elif int(no) not in no_list:
        messagebox.showinfo("Error","Invalid Customer Number")
        
    elif int(store) not in store_list:
        messagebox.showinfo("Error","Invalid Store ID")    

    else:
        sql = 'select id, price from items;'
        cur.execute(sql)
        prices = cur.fetchall()
        df = pd.DataFrame(prices, columns=['id', 'price'])
        df.set_index('id', inplace=True)
        for item in items:
            amount = amount + float(df['price'][int(item[0])])*int(item[3])
        amt = str(amount)
        insert_bill = "insert into bills(bill_date,amount,cust_id,store) values('"+today+"',"+amt+","+no+","+store+")"
        try:
            cur.execute(insert_bill)
            con.commit()
            bill_sql = "select * from bills;"
            cur.execute(bill_sql)
            bill_no = str(cur.fetchall()[-1][0])
            for item in items:
                sql='insert into transaction(item_id,qty,bill_id) values({},{},{});'.format(item[0],item[3],bill_no)
                cur.execute(sql)
                con.commit()
            messagebox.showinfo('Success',"Added bill succesfully\n\nTotal Bill Amount = "+amt)
        except:
            messagebox.showinfo("Error","Can't add bill into Database")
        
        
        # child.destroy()
        root.destroy()


def add_bill(parent):
    
    global cust_name, cust_email, item_no, qty, Canvas1, con, cur, root, table_name,\
        add_item_but, Save, items, view, cust_no, store_no
    
    items = []
    root = Toplevel(parent)
    root.title("Billing Details")
    root.minsize(width=500,height=400)
    root.geometry("800x600")
    
    #Initializing Database objects

    con = sql_login().login()
    cur = con.cursor()
    
    table_name = 'bills'            #Name of bills table
    
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="#ff6e40")
    Canvas1.pack(expand=True,fill=BOTH)
    
    headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    
    headingLabel = Label(headingFrame1, text="Add Bill Details", bg='black', fg='white', font=('Courier',15))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)
    
    lb4 = Label(labelFrame,text="Customer Number : ", bg='black', fg='white')
    lb4.place(relx=0.05,rely=0.3, relheight=0.08)

    call = partial(customer_display, root)

    cust_but = Button(root,text="CUSTOMERS",bg='#d1ccc0', fg='black',command=call)
    cust_but.place(relx=0.7,rely=0.5, relwidth=0.12,relheight=0.07)

    cust_no = Entry(labelFrame)
    cust_no.place(relx=0.5,rely=0.3, relwidth=0.1, relheight=0.1)
    
    lb3 = Label(labelFrame,text="Item id and quantity: ", bg='black', fg='white')
    lb3.place(relx=0.05,rely=0.50, relheight=0.08)
    
    sql = "select id from items;"
    cur.execute(sql)
    temp_ids = [ids[0] for ids in cur.fetchall()]
    global variable
    variable = StringVar(root)
    variable.set('')

    item_no = OptionMenu(root, variable, *temp_ids)
    item_no.place(relx=0.5,rely=0.60, relwidth=0.1, relheight=0.05)

    qty = Entry(labelFrame)
    qty.place(relx=0.8,rely=0.50, relwidth=0.1, relheight=0.1)
    
    lb4 = Label(labelFrame,text="Store ID : ", bg='black', fg='white')
    lb4.place(relx=0.05,rely=0.7, relheight=0.08)
    
    store_no = Entry(labelFrame)
    store_no.place(relx=0.5,rely=0.7, relwidth=0.1, relheight=0.1)

    call_store = partial(store_display, root)

    store_but = Button(root,text="STORES",bg='#d1ccc0', fg='black',command=call_store)
    store_but.place(relx=0.7,rely=0.7, relwidth=0.12,relheight=0.07)

    add_item_but = Button(root,text="ADD ITEM",bg='#d1ccc0', fg='black',command=add_item)
    add_item_but.place(relx=0.02,rely=0.9, relwidth=0.18,relheight=0.08)
    
    Save = Button(root,text="SAVE BILL",bg='#d1ccc0', fg='black',command=bill_generate)
    Save.place(relx=0.3,rely=0.9, relwidth=0.18,relheight=0.08)
    
    view = Button(root,text="VIEW ITEMS",bg='#d1ccc0', fg='black',command=view_items)
    view.place(relx=0.6,rely=0.9, relwidth=0.18,relheight=0.08)
    
    
    root.mainloop()
    
def add_item():
    it = variable.get()
    it_qty = qty.get()
    item_tup = find_item(it)
    if item_tup == None:
        messagebox.showerror("showerror", "Incorrect item number")
    
    elif it_qty == '':
        messagebox.showerror("showerror", "Quantity cannot be blank")
    else:
        item = list(item_tup)
        item.append(it_qty)
        items.append(item)

    # item_no.delete(0, END)
    qty.delete(0, END)
    
def find_item(no):
    cur.execute('select * from items where id ={}'.format(no))
    record = cur.fetchone()
    return record

def view_items():
    child = Toplevel(root)
    child.geometry('580x250')
    child.title('Item List')
    sql="select * from items;"
    cur.execute(sql)
    records = cur.fetchall()
    sql2 = "desc items;"
    cur.execute(sql2)
    col_names = [col[0] for col in cur.fetchall()]
    i=0 
    for k in range(len(col_names)):
        e = Entry(child, width=10, fg='blue', bg='yellow', font='Arial')
        e.grid(row=i, column=k) 
        e.insert(END, col_names[k])
        
    i=i+1
    for student in records: 
        for j in range(len(student)):
            e = Entry(child, width=10, fg='blue') 
            e.grid(row=i, column=j) 
            e.insert(END, student[j])
        i=i+1

def customer_display(root):
    
    child = Toplevel(root)
    child.geometry('620x400')
    child.title('Customer List')
    # child.state('zoomed')

    tree = ttk.Treeview(child, column=("c1", "c2", "c3"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="CUSTOMER ID")
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="CUSTOMER NAME")

    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="CUSTOMER EMAIL")
    
    cur.execute("SELECT * FROM customer;")

    rows = cur.fetchall()    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)
    
    tree.pack()
    
def store_display(root):
    
    child = Toplevel(root)
    child.geometry('580x400')
    child.title('Store Details')
    # child.state('zoomed')

    tree = ttk.Treeview(child, column=("c1", "c2"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="STORE ID")
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="STORE LOCATION")
    
    cur.execute("SELECT * FROM store;")

    rows = cur.fetchall()    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)
    
    tree.pack()
    
    
    child.mainloop()
    
# add_bill()
    
    
    