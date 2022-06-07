# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 11:49:52 2022

@author: akhil
"""

import mysql.connector as connector

class sql_login():
    def __init__(self):
        self.password = "akhil"
        self.database = "billing_test"
        
    def login(self):  
        con = connector.connect(host="localhost",user="root",password=self.password,db=self.database)
        return con