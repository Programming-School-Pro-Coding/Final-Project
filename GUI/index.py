import tkinter as tk # gui python  
from tkinter import ttk

import classes as c
import Connection

user1 = c.user(Connection.DB_URI)
game1 = c.Game(Connection.DB_URI)

def UpdateTable(TreeView, isUsers):
    if isUsers == True:
        for item in TreeView.get_children():
            TreeView.delete(item)
        users = user1.getAllUsers()
        for user in users:
            user = list(user)
            TreeView.insert(parent='',index='end',text='f',values=user)
    else:
        for item in TreeView.get_children():
            TreeView.delete(item)
        games = game1.GetAllGames()
        for game in games:
            game = list(game)
            TreeView.insert(parent='',index='end',text='f',values=game)

def DeleteUser(tree):
    curItem = tree.focus()
    # print(tree.item(curItem))
    item = tree.item(curItem)
    userID = item['values'][0]
    result = user1.deleteUser(userID)
    if result == False:
        appearMessage("Something Wrong!! Can't Delete the User")
    else:
        appearMessage('UserDeleted')
        UpdateTable(TreeView_Admin, True)

def appearMessage(message):
     test=ttk.Label(win,text=message,foreground="red")
     test.place(x=60,y=100)
     #update Frame to display massage
     win.update()
     test.after(2000,test.destroy())

def switcher(frame):
    frame.tkraise()

def Login(username,password):
    result = user1.login(username.get(), password.get())
    if (result == False):
        appearMessage("Wrong username or password")
    else:
        AdminPage.tkraise()

def register(username,password):
    user1.register(username.get(), password.get(), 3)
    AdminPage.tkraise()
    for item in TreeView_Admin.get_children():
        TreeView_Admin.delete(item)
    users = user1.getAllUsers()
    for user in users:
        user = list(user)
        TreeView_Admin.insert(parent='',index='end',text='f',values=user)

def AddGame(gameName):
    result = game1.addGame(gameName.get(), 3)
    if (not result):
        print("Can't Add the Game")
        appearMessage('Something went error!!')
    else:
        gamesPage.tkraise()
        UpdateTable(TreeView_Games, False)
    

win =tk.Tk()
win.geometry("300x300")

win.columnconfigure(0,weight=1)
win.rowconfigure(0,weight=1)

ttk.Label(win,text="Username")

# Creating Frames

loginFrame=ttk.Frame(win)
loginFrame.grid(column=0,row=0,sticky=tk.NSEW)

registerFrame=ttk.Frame(win)
registerFrame.grid(column=0,row=0,sticky=tk.NSEW)

AdminPage=ttk.Frame(win)
AdminPage.grid(column=0,row=0,sticky=tk.NSEW)


gamesPage=ttk.Frame(win)
gamesPage.grid(column=0,row=0,sticky=tk.NSEW)

addGames=ttk.Frame(win)
addGames.grid(column=0,row=0,sticky=tk.NSEW)

# Add Games
ttk.Label(addGames, text="Game Name").grid(column=0,row=0)
gamename_var_addGame=tk.StringVar()
gameNameEntry=ttk.Entry(addGames, textvariable=gamename_var_addGame).grid(column=1,row=0)

ttk.Button(addGames, text="Submit", command=lambda: AddGame(gamename_var_addGame)).grid(column=0,row=1)

# Login

# username
ttk.Label(loginFrame,text="Username").grid(column=0,row=0)
username_var_login=tk.StringVar()
usernameEntry=ttk.Entry(loginFrame ,textvariable=username_var_login).grid(column=1,row=0)


# password
ttk.Label(loginFrame,text="password").grid(column=0,row=1)
password_var_login=tk.StringVar()
passwordEntry=ttk.Entry(loginFrame ,textvariable=password_var_login).grid(column=1,row=1)

# button login
ttk.Button(loginFrame,text="Login",command=lambda :Login(username_var_login,password_var_login)).grid(column=0,row=2)

# Button Switch Between register and login
ttk.Button(loginFrame, text="Switch to register", command=lambda : switcher(registerFrame)).grid(column=0,row=3)

# Register

# username
ttk.Label(registerFrame,text="Username").grid(column=0,row=0)
username_var=tk.StringVar()
usernameEntry=ttk.Entry(registerFrame ,textvariable=username_var).grid(column=1,row=0)


# password
ttk.Label(registerFrame,text="password").grid(column=0,row=1)
password_var=tk.StringVar()
passwordEntry=ttk.Entry(registerFrame ,textvariable=password_var).grid(column=1,row=1)

# button login
ttk.Button(registerFrame,text="Register",command=lambda :register(username_var,password_var)).grid(column=0,row=2)


# Button Switch Between login and register
ttk.Button(registerFrame, text='Switch to Login', command=lambda: switcher(loginFrame)).grid(column=0, row=3)

loginFrame.tkraise()

# Admin Page Structure

TreeView_Admin = ttk.Treeview(AdminPage)

TreeView_Admin['columns']=['id','UserName', 'ScoreID']

TreeView_Admin.column("#0", width=5,  stretch=tk.NO)
TreeView_Admin.heading("#0",text="")
# insert data to the table 
users = user1.getAllUsers()
TreeView_Admin.heading("id",text='id')
TreeView_Admin.heading("UserName",text='Username')
TreeView_Admin.heading("ScoreID",text='ScoreID')

# insert data to the table
UpdateTable(TreeView_Admin, True)


TreeView_Admin.place(x=10,y=10)   
delete_button = tk.Button(AdminPage,text="delete", command=lambda: DeleteUser(TreeView_Admin))
delete_button.place(x=50,y=250)
Switch_button = tk.Button(AdminPage,text="Switch to Games Page", command=lambda: switcher(gamesPage))
Switch_button.place(x=120,y=250)

# Games Page Structure

TreeView_Games = ttk.Treeview(gamesPage)

TreeView_Games['columns']=['id','Game Name', 'ScoreID']

TreeView_Games.column("#0", width=5,  stretch=tk.NO)
TreeView_Games.heading("#0",text="")
# insert data to the table 
games = game1.GetAllGames()
TreeView_Games.heading("id",text='id')
TreeView_Games.heading("Game Name",text='Game Name')
TreeView_Games.heading("ScoreID",text='ScoreID')

# insert data to the table
UpdateTable(TreeView_Games, False)


TreeView_Games.place(x=10,y=10)   
Add_button = tk.Button(gamesPage,text="Add Game", command=lambda: switcher(addGames))
Add_button.place(x=50,y=250)
switch = tk.Button(gamesPage,text="Switch to Admin Page", command=lambda: switcher(AdminPage))
switch.place(x=120,y=250)

win.mainloop()
