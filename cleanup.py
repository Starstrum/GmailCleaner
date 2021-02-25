#A small tool created by Maxwell Dudley to automate mass deletion of emails from an account
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def createService():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

service = createService()

#This method returns the messages in a users inbox in the form of an array
def searchMessages(searchString):
    #search the account of the authenticated user
    #query the inbox for messages from a particular sender
    results = service.users().messages().list(userId='me',labelIds = 'INBOX', q = searchString).execute()
    messages = results.get('messages', [])
    return messages

#This method will allow the switching of accounts by deleting the token.picle file and then creating a new service object 
def switchAccounts():
    #By deleting the token file new access and refresh tokens must be generated so the user just needs to have the credentials.json file 
    #I want to find a way to generate the credentials.json file without the user having to go to the developer page
    if(os.path.exists('token.pickle')):
        os.remove('token.pickle')
    service = createService()
    return service

#To run the script by itself you can just run python cleanup.py and it will do the same thing for you
def main():
    service = createService()
    while(1)
        choice = input('Do you want to search messages, delete messages or switch accounts(q or quit to exit)? ')
        choice = choice.lower()
        if choice == 'search' or 'delete' or 's' or 'd':
            #search the account of the authenticated user
            searchString = input('What is the email address of the messages you want? ')
            messages = searchMessages(searchString)
            #if the user wants to delete then delete the messages after printing each snippet
            if choice == 'delete' or 'd':
                if not messages:
                    print('No messages found')
                else:
                    for message in messages:
                        msg = service.users().messages().get(userId = 'me',id = message['id']).execute()
                        print(msg['snippet'])
                        msg = service.users().messages().trash(userId = 'me',id = message['id']).execute()
            #if the user wants to search just print out the snippits
            elif choice == 'search' or 's':
                if not messages:
                    print('No messages found')
                else:
                    for message in messages:
                        msg = service.users().messages().get(userId = 'me',id = message['id']).execute()
                        print(msg['snippet'])
        #If the user wants to switch accounts just call the method
        elif choice == 'switch accounts' or 'sa':
            service = switchAccounts()
        elif choice == 'quit' or 'q' or 'exit' or 'e'
            print('Goodbye')
            break
        else:
            print('Please enter a valid command ')
if __name__ == '__main__':
    main()