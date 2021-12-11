import sqlite3
from sqlite3.dbapi2 import Cursor, Error
import PySimpleGUI as sg

def main():
    #Start the SQL server
    serv= SQL('data/ToworkWith.db')

    frontEnd = gui()
    while (frontEnd.closed == False):
        fromUser = frontEnd.input()

        #injection to retrieve all tables
        # ' UNION SELECT name, type FROM sqlite_schema WHERE type = "table" AND name NOT LIKE "sqlite_%"; --

        #Unsafe search function
        toUser = serv.search(fromUser)

        #Safe function checking for non-AlphaNumeric charicters (uncomment to use)
        #toUser = serv.alphNumb(fromUser)

        #Safe function to force input as string Must be exact match
        #toUser = serv.parameterized(fromUser) 
        
        #returns to user
        frontEnd.display(toUser)


    print("end of program my dude")



class gui:

    def __init__(self) :
        
        self.theme = sg.theme('DarkAmber')  
        self.userFeedback = ''
        self.dropdown = ''
        self.text = ''
        self.usrMsgBox = sg.Multiline(self.userFeedback,auto_refresh =True, key = "usrMsgbox") 
        self.closed = False
    

        self.layout =  [  [sg.Text('Category of search'), sg.Combo(values=[ 'artists','genres', 'playlists', 'tracks'])], 
            [sg.Text('Search'), sg.InputText()],
             [self.usrMsgBox],
            [sg.Button('Ok'), sg.Button('Cancel')]
           ]

        # Create the Window
        self.window = sg.Window('User database input', self.layout, size=(600,200))
    
        self.window.Finalize()

           
    def input(self):
        while True:
            event, values = self.window.read()
            self.dropdown = values[0]
            self.text = values[1]
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            return values

    def display(self, message):

        self.userFeedback = message    
        self.usrMsgBox(message)

    def close(self):
        self.window.close()
        self.closed = True


class SQL:

    def __init__(self, dbName) :
        self.con = sqlite3.connect(dbName)
        self.cur = self.con.cursor()
        self.ex = self.cur.execute
        self.git = self.cur.fetchall
        
        
    #unsafe and vulnerable method, inputs user values into Query 
    def search(self, searchParam):
        self.ex(("SELECT * FROM "+searchParam[0]+" WHERE Name LIKE '%"+searchParam[1]+"%'" ))
        data = self.git()
        return data


    #class method to check if the input is proper alphanumeric
    def alphNumb(self, check ):
        
        if ( check[1].isalnum() == True ):
            return (check)
        else:
            return ("invalid input")


    #search param as string and only string, Must be exact match
    def parameterized (self, searchParam):   
        qryStrng ="SELECT * FROM "+searchParam[0] + " WHERE name=? "
        a_name = searchParam[1]
        
        
        self.ex(qryStrng, [a_name] )
        data =self.git()
        return data




main()

