# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 11:25:48 2022

@author: akhil
"""

from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector as connector
from datetime import date
import pandas as pd
from pandas_tkinter import TestApp
from tkinter import ttk
from sql_init import sql_login
from functools import partial


def View():

    temp = bill_no.get()
    cur.execute("select bill_id from bills;")
    bill_ids = [abc[0] for abc in cur.fetchall()]
    
    if int(temp) not in bill_ids:
        messagebox.showinfo("Error","Invalid Bill ID")
    else:
        global it
        it = temp
        new = Toplevel(child)
        new.geometry('1400x500')
        new.title('Bill')
        headingFrame1 = Frame(new,bg="#FFBB00",bd=5)
        headingFrame1.place(relx=0.02,rely=0.05,relwidth=0.3,relheight=0.08)
        
        headingLabel = Label(headingFrame1, text="Bill No : "+str(temp), bg='black', fg='white', font=('Courier',10,'bold'))
        headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
        
        tree = ttk.Treeview(new, column=("c1", "c2", "c3","c4","c5", "c6"), show='headings')
        tree.column("#1", anchor=CENTER)
        tree.heading("#1", text="Bill ID")
        
        tree.column("#2", anchor=CENTER)
        tree.heading("#2", text="Bill Date")
    
        tree.column("#3", anchor=CENTER)
        tree.heading("#3", text="Customer ID")
        
        tree.column("#4", anchor=CENTER)
        tree.heading("#4", text="Customer Name")
    
        tree.column("#5", anchor=CENTER)
        tree.heading("#5", text="Customer Email")
        
        tree.column("#6", anchor=CENTER)
        tree.heading("#6", text="Bill Amount")
        
        cur.execute("select b.bill_id,b.bill_date, c.cust_id, c.cust_name, c.cust_email, b.amount from bills b\
                    inner join customer c on b.cust_id=c.cust_id where b.bill_id={};".format(temp))
    
        rows = cur.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", END, values=row)
    
        tree.pack(pady=90)
        # sql = 'select i.item_name, i.price, t.qty from items i\
        #         inner join transaction t on i.id=t.item_id where\
        #             t.bill_id={}'.format(temp)
                
        # cur.execute(sql)
        # rows = cur.fetchall()
        
        items = partial(view_items, new)
        
        button2 = Button(new, text="View Items", command=items)
        button2.place(relx=0.6, rely=0.7)
        new.mainloop()

def bill_search(root):
    global con, cur, child, tree, bill_no
    
    child = Toplevel(root)
    child.geometry('500x500')
    child.title('Bills')
    # child.state('zoomed')
    con = sql_login().login()
    cur = con.cursor()
    
    Canvas1 = Canvas(child)
    
    Canvas1.config(bg="#ff6e40")
    Canvas1.pack(expand=True,fill=BOTH)

    lb4 = Label(child,text="Enter Bill id : ", bg='black', fg='white')
    lb4.place(relx=0.05,rely=0.3, relheight=0.08)
    
    bill_no = Entry(child)
    bill_no.place(relx=0.5,rely=0.3, relwidth=0.2, relheight=0.1)
    
    button1 = Button(child, text="Display data", command=View)
    button1.place(relx=0.2, rely=0.7)
    
    child.mainloop()
    
    
def view_items(root):

    new = Toplevel(root)
    new.geometry('800x500')
    new.title('Bill_Details')
    frame = Frame(new)
    frame.pack(pady=80)
    
    childtree = ttk.Treeview(frame, column=("c1", "c2", "c3", "c4"), show='headings')
    childtree.column("#1", anchor=CENTER)
    childtree.heading("#1", text="Item Name")
    
    childtree.column("#2", anchor=CENTER)
    childtree.heading("#2", text="Price per unit")
    
    childtree.column("#3", anchor=CENTER)
    childtree.heading("#3", text="Quantity")
    
    childtree.column("#4", anchor=CENTER)
    childtree.heading("#4", text="Amount")
    
    sb = Scrollbar(frame, orient=VERTICAL)
    sb.pack(side=RIGHT, fill=Y)
    
    childtree.config(yscrollcommand=sb.set)
    sb.config(command=childtree.yview)
    
    sql = 'select i.item_name, i.price, t.qty from items i\
            inner join transaction t on i.id=t.item_id where\
                t.bill_id={}'.format(it)
            
    cur.execute(sql)
    rows = cur.fetchall()

    childtree.delete(*childtree.get_children())
    
    rows = list(rows)
    for i in range(len(rows)):
        rows[i] = list(rows[i])
        rows[i].append(rows[i][1]*rows[i][2])
        childtree.insert("", END, values=rows[i])
    
    amount = 0
    for row in rows:
        amount = amount+row[3]
    
    Label(new, text = "Total Bill Amount = "+str(amount),\
          bg='#09d5ab', bd=7, font=('Arial',12,'bold')).place(x = 450, y = 400)
    
    childtree.pack(pady=60)
    
    headingFrame1 = Frame(new,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.02,rely=0.05,relwidth=0.2,relheight=0.08)
    
    headingLabel = Label(headingFrame1, text="Bill No : "+str(it), bg='black', fg='white', font=('Courier',10,'bold'))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    
    new.mainloop()
# search_bill()