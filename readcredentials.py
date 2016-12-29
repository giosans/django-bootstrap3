# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 22:50:38 2016

@author: Utente 7
"""
import os
import json

def get_credentials(path):
    path = r'C:\Users\Utente 7\Downloads'
    with open(os.path.join(path,'credentials.json')) as data_file:    
        data = json.load(data_file)
    print data
    return [data['username'], data['password']]

