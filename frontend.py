import sqlite3
from sqlite3.dbapi2 import Cursor
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
        
        self.theme = sg.theme('DarkAmber')   # Add a touch of color
        self.userFeedback = ''
        self.dropdown = ''
        self.text = ''
        self.usrMsgBox = sg.Multiline(self.userFeedback,auto_refresh =True, key = "usrMsgbox") 
        self.closed = False
    

        self.layout =  [  [sg.Text('Catagory of search'), sg.Combo([ 'artists','genres', 'playlists', 'tracks'])], 
            [sg.Text('search'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [self.usrMsgBox]]

        # Create the Window
        self.window = sg.Window('User database input', self.layout)
    
        self.window.Finalize()

            # Event Loop to process "events" and get the "values" of the inputs
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
        #self.ex('SELECT name FROM sqlite_schema WHERE type = "table" AND name NOT LIKE "sqlite_%";')
        #self.names =self.cur.fetchall()
        

    def search(self, searchParam):
        self.ex(("SELECT * FROM "+searchParam[0]+" WHERE Name LIKE '%"+searchParam[1]+"%'" ))
        data = self.git()
        return data

        


main()



'''
conn = pyodbc.connect('Driver={C:\sqlite\Database\ToworkWith};'
                      'Server=server_name;'
                      'Database=database_name;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM table_name')

for i in cursor:
    print(i) '''

