# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 18:11:15 2022

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

    cur.execute("select s.store_id,s.store_loc, sum(b.amount) from store s, bills b\
                where b.store=s.store_id\
                group by s.store_id, b.store;")

    rows = cur.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)
        
def store_report(root):
    global con, cur, child, tree
    
    child = Toplevel(root)
    child.geometry('680x400')
    child.title('Store Wise Transactions')
    # child.state('zoomed')
    con = sql_login().login()
    cur = con.cursor()
    
    tree = ttk.Treeview(child, column=("c1", "c2", "c3"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="Store ID")
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="Store Location")

    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="Total Transaction")
    
    tree.pack()
    
    button1 = Button(child, text="Display data", command=View)
    button1.place(relx=0.4, rely=0.7)
    
    child.mainloop()
    
# store_report()