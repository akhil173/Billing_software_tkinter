# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 14:30:01 2022

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

    cur.execute("SELECT * FROM items;")

    rows = cur.fetchall()    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)

def items(root):
    global con, cur, child, tree
    
    child = Toplevel(root)
    child.geometry('580x400')
    child.title('Items')
    # child.state('zoomed')
    con = sql_login().login()
    cur = con.cursor()

    tree = ttk.Treeview(child, column=("c1", "c2", "c3"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="ITEM NO")
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="ITEM NAME")
    
    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="ITEM PRICE")
    
    tree.pack()
    
    button1 = Button(child, text="Display data", command=View)
    button1.place(relx=0.2, rely=0.7)

    button2 = Button(child, text="Add or Modify Item", command=modify_item)
    button2.place(relx=0.6, rely=0.7)
    
    child.mainloop()
    
def modify_item():
    # global id_input, name_input
    
    new = Toplevel(child)
    new.geometry('580x250')
    
    id_input = StringVar()  
    name_input = StringVar()
    price_input = StringVar()
    
    item_id = Label(new, text = "Item no : ").place(x = 20, y = 30)
    item_name = Label(new, text = "Item Name : ").place(x = 20, y = 60)
    item_price = Label(new, text = "Item Price : ").place(x = 20, y = 90)
    
    inp_id = Entry(new, textvariable=id_input, width = 15).place(x = 150, y = 30)
    inp_name = Entry(new, textvariable=name_input, width = 15).place(x = 150, y = 60)
    inp_price = Entry(new, textvariable=price_input, width = 15).place(x = 150, y = 90)
    
    call_result = partial(add_item_to_db, new, id_input, name_input, price_input)
    
    button = Button(new, text="Add or Modify Item", command=call_result)
    button.place(x=70, y=140)
    
def add_item_to_db(root, id_ip, name_ip, price_ip):
    item_id = id_ip.get()
    item_name = name_ip.get()
    price = price_ip.get()
    cur.execute("select * from items;")
    id_list = [ids[0] for ids in cur.fetchall()]
    if item_id == '':
        messagebox.showinfo("Error","Item ID can't be empty")
    elif int(item_id) in id_list:
        sql = 'update items set item_name = "{}", price ={} where id={}'.format(item_name,price,item_id)
        cur.execute(sql)
        con.commit()
        messagebox.showinfo("Success","Modified Item with Item number =  "+item_id)
        root.destroy()
    else:
        try:
            sql="insert into items(id, item_name, price) values({},'{}',{});".format(item_id,item_name,price)
            cur.execute(sql)
            con.commit()
            messagebox.showinfo('Success',"Added Item Succesfully ")
            root.destroy()
        except:
            messagebox.showinfo("Error","Could'nt add Customer to Database")
            
# items()