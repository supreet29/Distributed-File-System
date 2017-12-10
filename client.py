import requests as req
import json
import shelve
from requests.auth import HTTPBasicAuth
import os

url = "http://0.0.0.0:8080/filepath/"
print("==================================================================")
print("\t\tWelcome to Distributed File System")
print("==================================================================\n")
print("1. Read File")
print("2. Write File")
print("3. Delete File\n")
options= input("Select the option to:- \n")
if options=='1':
    filepath = input("Enter the file name:")
    url = url+filepath
    response = req.get(url)
    print("Response: ",response.text)
if options=='2':
    filepath = input("Enter the file name:")
    url = url+filepath
    content = "hello"
    response= req.post(url, content)
    print("Response: ",response.text)
if options=='3':
    filepath = input("Enter the file name:")
    url = url+filepath
    response = req.delete(url)
    print("File removed")

"""

response = req.get(url, auth=HTTPBasicAuth(username,password))
#print("File: ",response.json())
print("Response: ",response.text)



url = "http://0.0.0.0:8080/filepath/DFS_Test/ex.txt"

filepath = input("Enter the file name:")
url = url+filepath

response = req.get(url)
print("Response: ",response.text)
"""
