# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 21:58:45 2022

@author: akhil
"""

import bill_generation as b_gen
import customer_details as c_det
import item_details as i_det
import bills_display as b_display
import store_details as s_det
import store_wise_trans as s_trans
import search_bill as s_bill

from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector as connector
from datetime import date
import pandas as pd
from pandas_tkinter import TestApp
from tkinter import ttk
from functools import partial

class billing_software():
    def __init__(self):
        root = Tk()
        root.title("Billing Software")
        root.minsize(width=500,height=400)
        root.geometry("800x600")
        
        Canvas1 = Canvas(root)
        
        Canvas1.config(bg="#09d5ab")
        Canvas1.pack(expand=True,fill=BOTH)
        
        headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
        headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
        headingLabel = Label(headingFrame1, text="Billing Software", bg='black', fg='white', font=('Courier',20,'bold'))
        headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
        
        
        add_bills = partial(b_gen.add_bill, root)
        Button(root,text="ADD NEW BILL",bg='#d1ccc0', fg='black',command=add_bills).place\
            (relx=0.25,rely=0.35, relwidth=0.5,relheight=0.12)
            
        view_bills = partial(b_display.view_bills, root)
        Button(root,text="VIEW BILLS",bg='#d1ccc0', fg='black',command=view_bills).place\
            (relx=0.1,rely=0.55, relwidth=0.18,relheight=0.07)
            
        view_items = partial(i_det.items, root)
        Button(root,text="VIEW ITEMS",bg='#d1ccc0', fg='black',command=view_items).place\
            (relx=0.4,rely=0.55, relwidth=0.18,relheight=0.07)
            
        view_cust = partial(c_det.customers, root)
        Button(root,text="VIEW CUSTOMERS",bg='#d1ccc0', fg='black',command=view_cust).place\
            (relx=0.7,rely=0.55, relwidth=0.18,relheight=0.07)
            
        view_store = partial(s_det.store, root)
        Button(root,text="VIEW STORES",bg='#d1ccc0', fg='black',command=view_store).place\
            (relx=0.1,rely=0.74, relwidth=0.18,relheight=0.07)
            
        store_trans = partial(s_trans.store_report, root)
        Button(root,text="STORE WISE TRANSACTION", wraplength=110,\
               bg='#d1ccc0', fg='black',command=store_trans).place\
            (relx=0.4,rely=0.74, relwidth=0.18,relheight=0.1)
        
        search = partial(s_bill.bill_search, root)
        Button(root, text="SEARCH BILL", bg='#d1ccc0', fg='black',command=search)\
            .place(relx=0.7,rely=0.74, relwidth=0.18,relheight=0.07)
        
        root.mainloop()

if __name__ == '__main__':
    billing_software()