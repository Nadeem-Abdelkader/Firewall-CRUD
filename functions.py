"""
Firewall Configuration Application
- CRUD operations (Create, Read, Update, Delete)
- Export to CSV file
- Import from CSV file

Created by: Nadeem Abdelkader on 15/3/2022
Last updated by Nadeem Abdelkader on 22/3/2022

MySQL for the database
Tkinter used to create a simple GUI

This file contains the helper function to be called from main.py
"""

# importing the necessary libraries for working with csv, Tkinter and MySQL
import csv
from tkinter import Tk, NORMAL, DISABLED, messagebox as tkMessageBox, filedialog, StringVar, Frame, TOP, LEFT, RIGHT, \
    BOTTOM, OptionMenu, Label, Entry, Button, Scrollbar, VERTICAL, HORIZONTAL, ttk as ttk, Y, X, W, NO

import mysql.connector
import pymysql

# declaring the constants to be used everywhere in the module
DATABASE_HOST = "doricardo.com"  # "doricardo.com" , "localhost"
DATABASE_USER = "doric482_admin"  # "doric482_admin" , "root"
DATABASE_PASSWORD = "doric482_admin"  # "doric482_admin" , "Hpomengtx1050"
DATABASE_NAME = "doric482_golonger"  # "doric482_golonger" , "khwarizm"
TABLE_NAME = "firewall"

# connecting to database
conn = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD)
cursor = conn.cursor()

global Top, Right, Left, Forms, Buttons, OtherButtons, HookDropDownGroup, ActionDropDownGroup, number, txt_result,\
    btn_create, btn_read, btn_update, btn_delete, tree


def initialise_window():
    """
    function to intialise the tkinter GUI window
    :return: root
    """
    root = Tk()
    root.title("Khwarizm Consulting")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width / 1.15  # 1.5 for vs code, 1.7 for pycharm
    height = screen_height / 1.5
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.resizable(1, 1)
    return root


# calling function to initialise the gui window
my_root = initialise_window()


def database():
    """
    function to initialise the MySQL database and table
    :return: void
    """
    query = "CREATE DATABASE IF NOT EXISTS " + DATABASE_NAME + ";"
    cursor.execute(query)
    query = "USE " + DATABASE_NAME + ";"
    cursor.execute(query)
    query = "CREATE TABLE " \
            "IF NOT EXISTS " + TABLE_NAME + \
            "(number INT AUTO_INCREMENT, hook VARCHAR(40), action VARCHAR(40), text VARCHAR(255),  PRIMARY KEY (" \
            "number)); "
    cursor.execute(query)
    return


def create():
    """
    function to create a record in the MySQL table
    :return: void
    """
    if HOOK.get() == "" or ACTION.get() == "" or TEXT.get() == "":
        txt_result.config(text="Please complete the required field!", fg="red")
    else:
        database()
        query = "INSERT INTO `" + TABLE_NAME + "` (hook, action, text) VALUES(%s, %s, %s)"
        cursor.execute(query, (str(HOOK.get()), str(ACTION.get()), str(TEXT.get())))
        tree.delete(*tree.get_children())
        add_to_table_view()
        txt_result.config(text="Created a data!", fg="green")
    return


def add_to_table_view():
    """
    function to add the database records to the GUI table
    :return: void
    """
    query = "SELECT * FROM `" + TABLE_NAME + "`"
    cursor.execute(query)
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3]))
    conn.commit()
    HOOK.set("Prerouting")
    ACTION.set("Accept")
    TEXT.set("")
    return


def read():
    """
    function to read data from the MySQL table
    :return: void
    """
    tree.delete(*tree.get_children())
    database()
    add_to_table_view()
    txt_result.config(text="Successfully read the data from database", fg="green")
    return


def update():
    """
    function to update a record in the MySQL table
    :return: void
    """
    database()
    if TEXT.get() == "":
        txt_result.config(text="Please complete the required field!", fg="red")
    else:
        tree.delete(*tree.get_children())
        query = "UPDATE `" + TABLE_NAME + "` SET `hook` = %s, `action` = %s, `text` = %s WHERE `number` = %s"
        cursor.execute(query, (str(HOOK.get()), str(ACTION.get()), str(TEXT.get()), int(number)))
        conn.commit()
        add_to_table_view()
        btn_create.config(state=NORMAL)
        btn_read.config(state=NORMAL)
        btn_update.config(state=DISABLED)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Successfully updated data", fg="green")
    return


def on_selected(event):
    """
    function triggered when a record is double clicked (to update a record)
    :param event:
    :return: void
    """
    global number
    cur_item = tree.focus()
    contents = (tree.item(cur_item))
    selected_item = contents['values']
    number = selected_item[0]
    HOOK.set("Prerouting")
    ACTION.set("Accept")
    TEXT.set("")
    HOOK.set(selected_item[1])
    ACTION.set(selected_item[2])
    TEXT.set(selected_item[3])
    btn_create.config(state=DISABLED)
    btn_read.config(state=DISABLED)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=DISABLED)
    return


def delete():
    """
    function to delete a record from MySQL table
    :return: void
    """
    if not tree.selection():
        txt_result.config(text="Please select an item first", fg="red")
    else:
        result = tkMessageBox.askquestion('Khwarizm Consulting', 'Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            cur_item = tree.focus()
            contents = (tree.item(cur_item))
            selected_item = contents['values']
            tree.delete(cur_item)
            database()
            cursor.execute("DELETE FROM `" + TABLE_NAME + "` WHERE `number` = %d" % selected_item[0])
            conn.commit()
            txt_result.config(text="Successfully deleted data", fg="black")

    return


def exit_program():
    """
    function to exit program
    :return: void
    """
    result = tkMessageBox.askquestion('Khwarizm Consulting', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        my_root.destroy()
    return


def import_csv():
    """
    function to import from csv to MySQL table
    :return: void
    """
    open_file = filedialog.askopenfilename()
    global conn, cursor
    conn = mysql.connector.connect(user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST,
                                   database=DATABASE_NAME, allow_local_infile=True)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM " + TABLE_NAME + "")
    tree.delete(*tree.get_children())
    query = "LOAD DATA LOCAL INFILE '" + open_file + "'INTO TABLE " + TABLE_NAME + " FIELDS TERMINATED BY ','  LINES " \
                                                                                   "TERMINATED BY '\n' IGNORE 1 LINES" \
                                                                                   " (number, hook, action, text) "
    cursor.execute(query)
    add_to_table_view()
    tkMessageBox.showinfo('Khwarizm Consulting', "Imported data successfully!")
    return


def export():
    """
    function to export from MySQL table to csv file
    :return: void
    """
    open_file = filedialog.askdirectory()
    query = "select * from " + TABLE_NAME + ""
    cursor.execute(query)
    with open(open_file + "/" + TABLE_NAME + ".csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(col[0] for col in cursor.description)
        for row in cursor:
            writer.writerow(row)
    tkMessageBox.showinfo('Khwarizm Consulting', "File exported successfully!")
    return


HOOK = StringVar()
ACTION = StringVar()
TEXT = StringVar()

HOOK.set("Prerouting")
ACTION.set("Accept")


def create_frame():
    """
    function to create GUI frame
    :return: void
    """
    global Top, Right, Left, Forms, Buttons, OtherButtons, HookDropDownGroup, ActionDropDownGroup
    Top = Frame(my_root, width=900, height=50, bd=2, relief="raise")
    Top.pack(side=TOP)
    Left = Frame(my_root, width=300, height=500, bd=2, relief="raise")
    Left.pack(side=LEFT)
    Right = Frame(my_root, width=600, height=500, bd=2, relief="raise")
    Right.pack(side=RIGHT)
    Forms = Frame(Left, width=300, height=450)
    Forms.pack(side=TOP)
    Buttons = Frame(Left, width=300, height=100, bd=2, relief="raise")
    Buttons.pack(side=BOTTOM)
    OtherButtons = Frame(Right, width=300, height=100, bd=2, relief="raise")
    OtherButtons.pack(side=BOTTOM)
    Frame(Forms)
    HookDropDownGroup = Frame(Forms)
    OptionMenu(HookDropDownGroup, HOOK, "Prerouting", "Postrouting", "Input", "Output",
               "Forward").pack(
        side=LEFT)
    ActionDropDownGroup = Frame(Forms)
    OptionMenu(ActionDropDownGroup, ACTION, "Accept", "Reject", "Forward").pack(side=LEFT)
    return


def create_label_widget():
    """
    function to create GUI label
    :return: void
    """
    global txt_result
    txt_title = Label(Top, width=900, font=('arial', 24), text="Khwarizm Consulting")
    txt_title.pack()
    txt_hook = Label(Forms, text="Hook:", font=('arial', 16), bd=15)
    txt_hook.grid(row=0, sticky="e")
    txt_action = Label(Forms, text="Action:", font=('arial', 16), bd=15)
    txt_action.grid(row=1, sticky="e")
    txt_text = Label(Forms, text="Text:", font=('arial', 16), bd=15)
    txt_text.grid(row=2, sticky="e")
    txt_result = Label(Buttons)
    txt_result.pack(side=TOP)
    return


def create_entry_widget():
    """
    function to create GUI entry
    :return: void
    """
    HookDropDownGroup.grid(row=0, column=1)
    ActionDropDownGroup.grid(row=1, column=1)
    text = Entry(Forms, textvariable=TEXT, width=30)
    text.grid(row=2, column=1)
    return


def create_button_widget():
    """
    function to create GUI button
    :return: void
    """
    global btn_create, btn_read, btn_update, btn_delete
    btn_create = Button(Buttons, width=10, text="Create", command=create)
    btn_create.pack(side=LEFT)
    btn_read = Button(Buttons, width=10, text="Read", command=read)
    btn_read.pack(side=LEFT)
    btn_update = Button(Buttons, width=10, text="Update", command=update, state=DISABLED)
    btn_update.pack(side=LEFT)
    btn_delete = Button(Buttons, width=10, text="Delete", command=delete)
    btn_delete.pack(side=LEFT)
    btn_import = Button(OtherButtons, width=10, text="Import", command=import_csv)
    btn_import.pack(side=LEFT)
    btn_export = Button(OtherButtons, width=10, text="Export", command=export)
    btn_export.pack(side=LEFT)
    btn_exit = Button(OtherButtons, width=10, text="Exit", command=exit_program)
    btn_exit.pack(side=RIGHT)
    btn_delete_all = Button(Buttons, width=10, text="Delete All", command=clear_all)
    btn_delete_all.pack(side=RIGHT)
    return


def create_list_widget():
    """
    function to create GUI list
    :return: void
    """
    global tree
    scrollbary = Scrollbar(Right, orient=VERTICAL)
    scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
    tree = ttk.Treeview(Right, columns=("Number", "Hook", "Action", "Text"), selectmode="extended", height=500,
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Number', text="Number", anchor=W)
    tree.heading('Hook', text="Hook", anchor=W)
    tree.heading('Action', text="Action", anchor=W)
    tree.heading('Text', text="Text", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=120)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=220)
    tree.pack()
    tree.bind('<Double-Button-1>', on_selected)
    return


def clear_all():
    """
    function to delete all records from database table
    :return: void
    """
    result = tkMessageBox.askquestion('Khwarizm Consulting', 'Are you sure you want to delete all records?',
                                      icon="warning")
    if result == 'yes':
        global conn, cursor
        conn = mysql.connector.connect(user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST,
                                       database=DATABASE_NAME, allow_local_infile=True)
        cursor = conn.cursor()
        # cursor.execute("DROP TABLE IF EXISTS " + TABLE_NAME + "")
        cursor.execute("DELETE FROM " + TABLE_NAME + "")
        tree.delete(*tree.get_children())
    return
