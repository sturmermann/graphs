from tkinter import *
import os

print( "Please Choose [e]diting existing or [c]reating new" )
while True:
    a = int(input())
    if not (a == "c" or a == "e"):
        print("Please Choose [e]diting existing or [c]reating new")
    break
print ( "Please write down the name of file" )