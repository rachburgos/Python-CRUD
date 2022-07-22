##################################################################
#                           IMPORTS                              # 
##################################################################

import sqlite3 as sql                   #use database commands through sqlite
import tkinter.ttk as ttk               #Treeview for the data - table style
from tkinter import *                   #build the GUI   
from tkinter import messagebox          #shows alerts through a dialog box

##################################################################
#                           DATABASE                             #
##################################################################

#create the database / connect to the existing one
# path = "E:/CISP71 python/CRUD Project/"
global conn
conn = sql.connect("Anime_Database.db")              #database file needs to be in the same folder as the python file

try:                #handling table error
    cur = conn.cursor()              #cursor is the medium to do sql commands
    #create the table called Anime
    #use triple quotes ''' to write on more than one line not backticks ``
    cur.execute('''CREATE TABLE IF NOT EXISTS Anime
        (ShowID integer not null,
        AnimeName text,
        Genre text,
        Episodes integer,
        SeasonDate text,
        FirstSeason text)''')
    conn.commit()               #approve the change
    print("Table created successfully.")
    
except:
    print("Table already exists.")
    conn.rollback()

conn.close()                #close the connection

##################################################################
#                             WINDOW                             #
##################################################################

root = Tk()
root.title("Anime Database - Rachelle Burgos")
root.geometry("700x530")

# create all of the frames (containers) to put widgets in
titleFrame = Frame(root, width = 200, height = 100)
mainFrame = Frame(root, width = 400, height = 200)
treeFrame = Frame(root, width= 400, height = 100)

#layout of the frames
root.grid_rowconfigure(1, weight = 1)
root.grid_columnconfigure(0, weight = 1)
# titleFrame.grid_rowconfigure(0, weight=1)
# titleFrame.grid_columnconfigure(1, weight=1)
mainFrame.grid_rowconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=1)
treeFrame.grid_rowconfigure(0, weight=1)
treeFrame.grid_columnconfigure(1, weight=1)

#put them on the grid
titleFrame.grid(row = 0, sticky = "n")
mainFrame.grid(row = 1, sticky = "n")
treeFrame.grid(row = 2)             #no sticky gives space between buttons and the Treeview

##################################################################
#                           FUNCTIONS                            #
##################################################################

def clearFields():              #this function resets the fields 
    IDEntry.delete(0, END)
    nameEntry.delete(0, END)
    genreEntry.delete(0, END)
    episodeEntry.delete(0, END)
    seasonVar.set(airList[0])
    radioVar.set(" ")

    
#connect to the database and use placeholder variables
#input for year and number of episodes should be numbers so it's integer
#1 radio variable for only 1 selection
#selected variable is for choosing from the airing list
def addRecord():                #this function adds a new record after validation is checked
    conn = sql.connect("Anime_Database.db")
    #if recordExists() == True:
    #call the validation function first
    if validateInput() == True:             #if true, means no blanks and can add the new record
        try:
            cur = conn.cursor()
            cur.execute("Insert into Anime values (?, ?, ?, ?, ?, ?)", 
            (int(IDEntry.get()), nameEntry.get(), genreEntry.get(), int(episodeEntry.get()),
            seasonVar.get(), updateRadioButton()))

            conn.commit()
            #messagebox.showinfo(title = "Success!", message = "Record added successfully!")

        except:
            messagebox.showerror(title = "Error", message = "There was an error adding the record.")
            conn.rollback()

        conn.close()
        clearFields()               #clear fields for next user / action
    else:               #there are blanks / default values when making the record
        messagebox.showerror(title = "Error", message = "You cannot have blank, default, or wrong values.")

    clearFields()
    displayRecord()
    IDEntry.focus_set()             #return focus to the first entry box -- IDEntry


def deleteRecord():             #this function deletes a whole record
    conn = sql.connect("Anime_Database.db")
    try:
        qry = "DELETE from Anime where ShowID = ?"             #where the column you want to delete must the same as the one in the db

        if IDEntry.get() == '':             #validate for empty selection
            messagebox.showinfo(title = "Action Needed", message = "Please select a record to delete.")
            return
        #not sure why stating message parameter broke it?
        #prompt the user again to ask about choice
        msgBox = messagebox.askquestion("Warning!", "Are you sure you want to delete this record? It cannot be undone.")

        if msgBox == "yes":             #after user confirms, delete
            cur = conn.cursor()
            cur.execute(qry, (IDEntry.get(),))  #need a , here to delete entries >= 10

            conn.commit()
            #messagebox.showinfo(title = "Success!", message = "Entry deleted successfully!")
            clearFields()

    except:
        messagebox.showerror(title = "Error", message = "There was an error deleting the record.")
        conn.rollback()

    finally:
        conn.close()
        displayRecord()
        clearFields()


#unsure how to validate this yet
def updateRecord():             #this function allows you to update an existing record
    conn = sql.connect("Anime_Database.db")
    qry = "UPDATE Anime SET AnimeName = ?, Genre = ?, Episodes = ?, SeasonDate = ?, FirstSeason = ? WHERE ShowID = ?"              

    try:
        cur = conn.cursor()
        cur.execute(qry, (nameEntry.get(), genreEntry.get(), episodeEntry.get(), seasonVar.get(), 
        updateRadioButton(), IDEntry.get()))                #getting the entry is last since it's in the WHERE statement

        conn.commit()
        #messagebox.showinfo(title = "Success!", message = "Entry updated successfully!")

    except:
        messagebox.showerror(title = "Error", message = "There was an error updating the record.")
        conn.rollback()

    finally:                #this will run no matter what
        conn.close()
        clearFields()
        displayRecord()
        IDEntry.focus_set()
    # cur = conn.cursor()
    # cur.execute('''UPDATE Anime SET
    # ShowID = ShowID, AnimeName = AnimeName, Genre = Genre, Episodes = Episodes,
    # SeasonDate = SeasonDate, FirstSeason = FirstSeason
    # WHERE oid = oid;''',
    # {
    #     'AnimeName':nameEntry.get(),
    #     'Genre':genreEntry.get(),
    #     'Episodes':episodeEntry.get(),
    #     'SeasonDate':selected.get(),
    #     'FirstSeason':selectRadioButton(),
    #     'ShowID':IDEntry.get()
    # })

 
def displayRecord():                #displays all current records from the database in the treeview
    for row in tvAnime.get_children():              #clears the treeview so it doesn't keep adding rows after each other
        tvAnime.delete(row)

    conn = sql.connect("Anime_Database.db")
    cur = conn.cursor()
    cur.execute("select *, oid from Anime")
    rows = cur.fetchall()

    for row in rows:                #populates the treeview
        Show_ID = row[0]
        Anime_Name = row[1]
        Genre = row[2]
        Episodes = row[3]
        Season = row[4]
        First_Season = row[5]
        tvAnime.insert("", "end", text = id, values = 
        (Show_ID, Anime_Name, Genre, Episodes, Season, First_Season, id))


def showSelectedRecord(event):              #this function fills in all relevant fields according to the information from the record
    clearFields()
    global id, seasonVar, radioVar              #global id since using several methods

    for selection in tvAnime.selection():
        item = tvAnime.item(selection)
        ShowID, AnimeName, Genre, Episodes, SeasonDate, FirstSeason = item["values"][0:6]

        IDEntry.insert(0, ShowID)
        nameEntry.insert(0, AnimeName)
        genreEntry.insert(0, Genre)
        episodeEntry.insert(0, Episodes)
        seasonVar.set(SeasonDate)
        radioVar.set(FirstSeason) 
    return id


def updateRadioButton():                #tracks changes to the radiobuttons
    resultY = "Yes"
    resultN = "No"
    choice = radioVar.get()
    if choice == "Yes":
        return resultY
    else:
        return resultN   


def exit():             #exits the program
    msgBox = messagebox.askquestion(title = "Warning", message = "Are you sure you want to exit?")
    if msgBox == "yes":
        #close the connection
        root.destroy()


def validateInput():                #checks inputs for adding a new record (row)
    choiceSeason = seasonVar.get()
    choiceFirst = radioVar.get()

    if IDEntry.get() == '':             #empty id
        messagebox.showinfo(title = "Action needed", message = "Please enter the record ID.")
        IDEntry.focus_set()
        return 
    if nameEntry.get() == '':               #empty name
        messagebox.showinfo(title = "Action needed", message = "Please enter the anime name.")
        nameEntry.focus_set()
        return 
    if genreEntry.get() == '':              #empty genre
        messagebox.showinfo(title = "Action needed", message = "Please enter the anime genre(s).")
        genreEntry.focus_set()
        return 
    if episodeEntry.get() == '':                #empty num of episodes
        messagebox.showinfo(title = "Action needed", message = "Please enter the number of episodes.")
        episodeEntry.focus_set()
        return 
    if choiceSeason == "Season":                #default season aired / airing
        messagebox.showinfo(title = "Action needed", message = "Please choose the season the anime aired.")
        seasonOpt.focus_set()
        return 
    if choiceFirst == 0:                #default value for whether anime has a first season or not
        messagebox.showerror(title = "Error", message = "Please select whether it's the first season or not.")
        firstSeasonRB1.focus_set()
        return 

    #checking for integer for ID and episodes
    if IDEntry.get().isdigit() == False:
        messagebox.showinfo(title = "Error", message = "ID must be a number. Please try again.")
        IDEntry.focus_set()
        return 
    if episodeEntry.get().isdigit() == False:
        messagebox.showinfo(title = "Error", message = "Number of episodes must be a number. Please try again.")
        episodeEntry.focus_set()
        return

    #if at least one input is blank / not chosen --- works fine without this block?
    if (IDEntry.get() == '' or nameEntry.get() == '' or genreEntry.get() == '' 
    or episodeEntry.get() == '' or choiceSeason == "Season" or choiceFirst == 0):
        return False
    else:
        return True
        
##################################################################
#                           WIDGETS                              #
##################################################################

airList = ["Season", "Summer", "Fall", "Winter", "Spring"]              #list for the optionmenu (dropdown)
seasonVar = StringVar()             #selected variable for the drop down airList
seasonVar.set(airList[0])               #make the default selection the first one

#labels
IDLabel = Label(mainFrame, text = "Anime ID:", font = ("Calibri", 11))
nameLabel = Label(mainFrame, text = "Anime Name:", font = ("Calibri", 11))
genreLabel = Label(mainFrame, text = "Genre(s):", font = ("Calibri", 11))
episodeLabel = Label(mainFrame, text = "No. of Episodes:", font = ("Calibri", 11))
seasonLabel = Label(mainFrame, text = "Airing Season:", font = ("Calibri", 11))
firstSeasonLabel = Label(mainFrame, text = "Is this the first season?", font = ("Calibri", 11))
selectLabel = Label(mainFrame, text = "Select one record in the table to update or delete.", 
font = ("Calibri", 12, "bold", "italic"))             #instructions for the user 
titleLabel = Label(titleFrame, text = "Anime Database", font = ("Calibri", 20, "bold"))               #for the title

#entries (textbox)
IDEntry = Entry(mainFrame)
nameEntry = Entry(mainFrame)
genreEntry = Entry(mainFrame)
episodeEntry = Entry(mainFrame)

#option menu (dropdown list)
seasonOpt = OptionMenu(mainFrame, seasonVar, *airList)               #*airList unpacks the list 

#radioVar = IntVar() doesn't work for toggling the radiobutton on the interface since .set() needs a string
radioVar = StringVar(root, " ")             #variable for the radiobutton              
firstSeasonRB1 = Radiobutton(mainFrame, text = "Yes", variable = radioVar, value = "Yes",
command = updateRadioButton)
firstSeasonRB2 = Radiobutton(mainFrame, text = "No", variable = radioVar, value = "No",
command = updateRadioButton)
#firstSeasonRB1 = Radiobutton(root, text = "Yes", variable = radioVar, value = 1, command = updateRadioButton)
#firstSeasonRB2 = Radiobutton(root, text = "No", variable = radioVar, value = 2, command = updateRadioButton)

#buttons
addButton = Button(mainFrame, text = "Add Entry", command = addRecord)
displayButton = Button(mainFrame, text = "Display Entries", command = displayRecord)
deleteButton = Button(mainFrame, text = "Delete Entry", command = deleteRecord)
updateButton = Button(mainFrame, text = "Update Entry", command = updateRecord)
clearButton = Button(mainFrame, text = "Clear", command = clearFields)
exitButton = Button(mainFrame, text = "Exit Program", fg = "red", command = exit)

##################################################################
#                     PLACE WIDGETS ON GRID                      #
##################################################################

#labels
titleLabel.grid(row = 0, column = 0)
IDLabel.grid(row = 1, column = 0)
nameLabel.grid(row = 2, column = 0)
genreLabel.grid(row = 3, column = 0)
episodeLabel.grid(row = 4, column = 0)
seasonLabel.grid(row = 5, column = 0)
firstSeasonLabel.grid(row = 6, column = 0)
selectLabel.grid(row = 8, column = 1)

#inputs
IDEntry.grid(row = 1, column = 1)
IDEntry.configure(width = 30)
nameEntry.grid(row = 2, column = 1)
nameEntry.configure(width = 30)
genreEntry.grid(row = 3, column = 1)
genreEntry.configure(width = 30)
episodeEntry.grid(row = 4, column = 1)
episodeEntry.configure(width = 30)
seasonOpt.grid(row = 5, column = 1)
seasonOpt.configure(width = 10)
firstSeasonRB1.grid(row = 6, column = 1)
firstSeasonRB2.grid(row = 6, column = 2)

#buttons
addButton.grid(row = 11, column = 0)
addButton.configure(width = 15)
displayButton.grid(row = 12, column = 0)
displayButton.configure(width = 15)
updateButton.grid(row = 11, column = 1)
updateButton.configure(width = 15)
deleteButton.grid(row = 11, column = 2)
deleteButton.configure(width = 15)
clearButton.grid(row = 12, column = 1)
clearButton.configure(width = 15)
exitButton.grid(row = 12, column = 2)
exitButton.configure(width = 15)

##################################################################
#                           TREEVIEW                             #
##################################################################

#tvAnime = ttk.Treeview(root, show = "headings", height = 5, columns = "columns")
tvAnime = ttk.Treeview(treeFrame, show = "headings", height = 10)               #create the widget

#columns = ("#1", "#2", "#3", "#4", "#5")
tvAnime["columns"] = ("id", "name", "genre", "episodes", "airing season", "first season")               #tuple columns

#specify columns and their dimensions
tvAnime.column("#0", width = 0, minwidth = 25) #phantom column
tvAnime.column("#1", width = 85, stretch = True)
tvAnime.column("#2", width = 85, stretch = True)
tvAnime.column("#3", width = 100, stretch = True)
tvAnime.column("#4", width = 85, stretch = True)
tvAnime.column("#5", width = 85, stretch = True)
tvAnime.column("#6", width = 85, stretch = True)

#name the columns
tvAnime.heading("#0", text = "") #phantom column
tvAnime.heading("#1", text = "Anime ID", anchor = "w")
tvAnime.heading("#2", text = "Anime Name", anchor = "w")
tvAnime.heading("#3", text = "Genre", anchor = "w")
tvAnime.heading("#4", text = "Episodes", anchor = "w")
tvAnime.heading("#5", text = "Airing Season", anchor = "w")
tvAnime.heading("#6", text = "First Season?", anchor = "w")

#this method confused me
# tvAnime.heading("#0", text = "ShowID", anchor = "w")
# tvAnime.column("#0", width = 10, anchor = "w", stretch = False)
# tvAnime.heading("#1", text = "AnimeName", anchor = "center")
# tvAnime.column("#1", width = 40, anchor = "center", stretch = True)
# tvAnime.heading("#2", text = "Genre", anchor = "center")
# tvAnime.column("#2", width = 40, anchor = "center", stretch = True)
# tvAnime.heading("#3", text = "Episode", anchor = "center")
# tvAnime.column("#3", width = 40, anchor = "center", stretch = True)
# tvAnime.heading("#4", text = "AiringSeason", anchor = "center")
# tvAnime.column("#4", width = 40, anchor = "center", stretch = True)
# tvAnime.heading("#5", text = "FirstSeason", anchor = "center")
# tvAnime.column("#5", width = 40, anchor = "center", stretch = True)

#scrollbars
verticalSB = ttk.Scrollbar(treeFrame, orient = "vertical", command = tvAnime.yview)             #vertical scrollbar
verticalSB.pack(side = "right", fill = "y")             #place the scrollbar
tvAnime.configure(yscroll = verticalSB.set)             #configure the treeview so that it will use the scrollbar

#do the same for hoizontal scrollbar
horizonSB = ttk.Scrollbar(treeFrame, orient = "horizontal", command = tvAnime.xview)
horizonSB.pack(side = "bottom", fill = "x")
tvAnime.configure(xscroll = horizonSB.set)

#insert data for testing -- comment out 
#row1 = tvAnime.insert("", 1, values = ("(TEST)", "Demon Slayer", "Action, Fantasy", "34", "Spring", "No"))

tvAnime.bind("<<TreeviewSelect>>", showSelectedRecord)              #bind the treeview to the function showSelectedRecord              
#tvAnime.grid(row = 20, column = 1, columnspan = 16, padx = 20, pady = 5)
tvAnime.pack(side="top", fill="both", expand=True )                #add treeview to the grid

#updates infomation after button click in real time - 
#also found in addRecord(), deleteRecord(), and updateRecord()
displayRecord()

root.mainloop()