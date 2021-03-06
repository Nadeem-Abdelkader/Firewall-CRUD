"""
Firewall Configuration Application
- CRUD operations (Create, Read, Update, Delete)
- Export to CSV file
- Import from CSV file

Created by: Nadeem Abdelkader on 15/3/2022
Last updated by Nadeem Abdelkader on 22/3/2022

MySQL for the database
Tkinter used to create a simple GUI

"""
# !/usr/bin/env python3

# importing the helper functions from functions.py
from functions import my_root, read, create_frame, create_label_widget, create_entry_widget, \
    create_button_widget, create_list_widget, cursor, conn

if __name__ == '__main__':
    """
    calling the helper functions from functions.py to start and run the application
    """
    create_frame()
    create_label_widget()
    create_entry_widget()
    create_button_widget()
    create_list_widget()
    read()
    my_root.mainloop()
    cursor.close()
    conn.close()
