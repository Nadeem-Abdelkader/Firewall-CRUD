"""
"""
# !/usr/bin/env python3

from functions import root, read, create_frame, create_label_widget, create_entry_widget, \
    create_button_widget, create_list_widget, cursor, conn

if __name__ == '__main__':
    create_frame()
    create_label_widget()
    create_entry_widget()
    create_button_widget()
    create_list_widget()
    read()
    root.mainloop()
    cursor.close()
    conn.close()