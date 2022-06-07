# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 19:50:32 2022

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

    cur.execute("SELECT * FROM store;")

    rows = cur.fetchall()    
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)

def store(root):
    global con, cur, child, tree
    
    child = Toplevel(root)
    child.geometry('580x400')
    child.title('Store Details')
    # child.state('zoomed')
    con = sql_login().login()
    cur = con.cursor()

    tree = ttk.Treeview(child, column=("c1", "c2"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="STORE ID", command=lambda : treeview_sort_column(tree, "#1", False))
    
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="STORE LOCATION", command=lambda : treeview_sort_column(tree, "#2", False))
    
    tree.pack()
    
    button1 = Button(child, text="Display data", command=View)
    button1.place(relx=0.2, rely=0.7)

    button2 = Button(child, text="Add or Modify Store Details", command=modify_store)
    button2.place(relx=0.6, rely=0.7)
    
    child.mainloop()
    
def modify_store():
    # global id_input, name_input
    
    new = Toplevel(child)
    new.geometry('580x250')
    
    id_input = StringVar()  
    name_input = StringVar()
    
    item_id = Label(new, text = "Store id : ").place(x = 20, y = 30)
    item_name = Label(new, text = "Store Location : ").place(x = 20, y = 60)
    
    inp_id = Entry(new, textvariable=id_input, width = 15).place(x = 150, y = 30)
    inp_name = Entry(new, textvariable=name_input, width = 15).place(x = 150, y = 60)
    
    call_result = partial(add_store_to_db, new, id_input, name_input)
    
    button = Button(new, text="Add or Modify Store", command=call_result)
    button.place(x=70, y=140)
    
def add_store_to_db(root, id_ip, name_ip):
    item_id = id_ip.get()
    item_name = name_ip.get()
    cur.execute("select * from store;")
    id_list = [ids[0] for ids in cur.fetchall()]
    if item_id == '':
        messagebox.showinfo("Error","Store ID can't be empty")
    elif int(item_id) in id_list:
        sql = 'update store set store_loc = "{}" where store_id={}'.format(item_name,item_id)
        cur.execute(sql)
        con.commit()
        messagebox.showinfo("Success","Modified Item with Store ID =  "+item_id)
        root.destroy()
    else:
        try:
            sql="insert into store(store_id, store_loc) values({},'{}');".format(item_id,item_name)
            cur.execute(sql)
            con.commit()
            messagebox.showinfo('Success',"Added Store Succesfully ")
            root.destroy()
        except:
            messagebox.showinfo("Error","Could'nt add Customer to Database")
            

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))
# store()