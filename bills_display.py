# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:22:08 2022

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

    cur.execute("select b.bill_id,b.bill_date,c.cust_id,c.cust_name,b.amount from bills b,customer c\
                where b.cust_id = c.cust_id;")

    rows = cur.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)

def view_bills(root):
    global con, cur, child, tree
    
    child = Toplevel(root)
    child.geometry('1020x500')
    child.title('Bills')
    # child.state('zoomed')
    con = sql_login().login()
    cur = con.cursor()
    
    tree = ttk.Treeview(child, column=("c1", "c2", "c3","c4","c5"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="Bill ID")
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="Bill Date")

    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="Customer ID")
    
    tree.column("#4", anchor=CENTER)
    tree.heading("#4", text="Customer Name")
    
    tree.column("#5", anchor=CENTER)
    tree.heading("#5", text="Bill Amount")
    
    tree.pack()
    
    button1 = Button(child, text="Display data", command=View)
    button1.place(relx=0.2, rely=0.7)
    
    
    button2 = Button(child, text="View Bill", command=view_items)
    button2.place(relx=0.6, rely=0.7)
    
    child.mainloop()
    
def view_items():
    row_id = tree.focus()
    temp = tree.item(row_id, 'values')
    if temp == '':
        messagebox.showinfo("Error","Select an item to view the bill")
        # messagebox.showinfo("Success",temp)
    else:
        
        temp = temp[0]
    # a=tree.selection_set(row_id)
        new = Toplevel(child)
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
                    t.bill_id={}'.format(temp)
                
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
        
        headingLabel = Label(headingFrame1, text="Bill No : "+str(temp), bg='black', fg='white', font=('Courier',10,'bold'))
        headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
        
        new.mainloop()
    
    


# view_bills()