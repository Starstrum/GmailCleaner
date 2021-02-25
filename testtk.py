import tkinter as tk
import tkinter.messagebox
import cleanup
from tkinter import Scrollbar
from google.auth.transport.requests import Request

#TODO Refactor into OOP?
#TODO Make me beautiful ;-;
#TODO Add multithreading to search for messages while the main thread is executing
service = cleanup.createService()
#If the search button is pressed search through the messages with the script open a new  window and display them

#Searches the user's inbox based on their query and then display them in a list box
def searchPressed():
    messages = cleanup.searchMessages(text_box.get())
    #Create a child window with a label to display snippets of the messages 
    search_window = tk.Toplevel(root)
    search_window.geometry("700x500")
    search_window.title("Messages")
    #Create a scrollbar object then bind it to the list box
    scrollbar = Scrollbar(search_window)
    search_box = tk.Listbox(search_window, yscrollcommand = scrollbar.set)
    scrollbar.pack(side = "right", fill = "y")
    search_box.pack(expand=True, fill='both')
    if not messages:
        tk.messagebox.showinfo("Messages", "No messages found")
    else:
        #put all message snippets into a list
        for message in messages:
            msg = service.users().messages().get(userId = 'me',id = message['id']).execute()
            #Replace the string that shows up in the snippets with an apostrophe then insert into the listbox
            snippet = msg['snippet']
            snippet = snippet.replace("&#39;","\'")
            search_box.insert("end",snippet)
            search_box.insert("end", "\n")

#This method will handle the deletion of messages searched by the user by calling the searchMessages function in cleanup.py and then deleting them
def deletePressed():
    messages = cleanup.searchMessages(text_box.get())
    if not messages:
        tk.messagebox.showinfo("Messages", "No messages found")
    else:
        #send all messages matching the query to the trash, print out a snippet beforehand
        for message in messages:
            msg = service.users().messages().get(userId = 'me',id = message['id']).execute()
            print(msg['snippet'])
            msg = service.users().messages().trash(userId = 'me',id = message['id']).execute()

#This method calls the switchAccounts method in the cleanup.py file
def switchAccountsPressed():
    service = cleanup.switchAccounts()
    
#all elements  you will make go between the root = tk.Tk() line and root.mainloop() line
root = tk.Tk()
root.title("Gmail Cleaner")
root.resizable(0, 0)

#set the size of the windo then initialize it with 3 columns to place your window in 
canvas = tk.Canvas(root, width = 700, height = 300)
canvas.grid(columnspan = 4, rowspan = 4)

title_label = tk.Label(root,text = "Welcome to the Gmail inbox cleaner", font = "Calibri")
title_label.grid(columnspan = 1, column = 1, row = 0)

#create strings for the buttons and the text variables to go with them 
#the difference between querytext and searchtext is that querytext is for the search bar and searchtext is for the search button
query_text = tk.StringVar()
search_text = tk.StringVar()
delete_text = tk.StringVar()
login_text = tk.StringVar()

text_box = tk.Entry(root, textvariable = query_text, font = "Calibri", width = 60)
search_button = tk.Button(root,textvariable = search_text, command = lambda:searchPressed(), font = "Calibri")
delete_button = tk.Button(root, textvariable = delete_text, font = "Calibri")
login_button = tk.Button(root, textvariable = login_text, command = lambda:switchAccountsPressed(),font = "Calibri")

#set the texts and show the buttons
query_text.set("Enter in the email address of the messages you want to find or delete")
text_box.grid( column = 1, row = 1)
search_text.set("Search")
search_button.grid(column = 1, row = 2)
delete_text.set("Delete")
delete_button.grid(column = 2, row = 2)
login_text.set("Switch Accounts/Login")
login_button.grid(column = 0, row = 2)

root.mainloop()

