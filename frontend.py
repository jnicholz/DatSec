import sqlite3
from sqlite3.dbapi2 import Cursor, Error
import PySimpleGUI as sg

def main():
    #Start the SQL server
    serv= SQL('data/ToworkWith.db')

    frontEnd = gui()
    while (frontEnd.closed == False):
        fromUser = frontEnd.input()

        toUser = serv.search(fromUser)

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
        #self.ex('SELECT name, type FROM sqlite_schema WHERE type = "table" AND name NOT LIKE "sqlite_%";')
        #self.names =self.cur.fetchall()
        
    #unsafe and vulnerable method, inputs user values into Query 
    def search(self, searchParam):
        self.ex(("SELECT * FROM "+searchParam[0]+" WHERE Name LIKE '%"+searchParam[1]+"%'" ))
        data = self.git()
        return data


    #class method to check if the input is proper alphanumeric
    def alphNumb(self, check ):
        
        if ( check.isAlnum() == True ):
            return (check)
        else:
            return ("invalid input")


    #search param as string and only string 
    def parameterized (self, searchParam):   
        qryStrng ="SELECT ? FROM  WHERE name=%?%"
        self.ex(qryStrng, (searchParam[0],searchParam[1]))




main()

