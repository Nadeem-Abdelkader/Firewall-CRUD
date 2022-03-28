# Firewall - CRUD Application

## Author
- [Nadeem Abdelkader](https://github.com/Nadeem-Abdelkader)

## What Is This?
This is a simple CRUD (create, read, update, and delete) application written in Python using Tkinter and MySQL.

## Set Up and Run

1. Download and install Python 3.10 from <https://www.python.org/downloads/> and make sure to add Python to PATH if you are using Windows
2. Clone or download the git repository
   [here](https://github.com/Nadeem-Abdelkader/Firewall-CRUD).
    ```sh
    git clone https://github.com/Nadeem-Abdelkader/Firewall-CRUD
    ```
3. Navigate to the cloned local repository
    ```sh
    cd Firewall-CRUD
    ```
4. Run the following command to to install all required dependencies
    ```sh
    pip3 install -r requirements.txt
    ```
5. To start the application, run the following command while inside the cloned local repository:
    ```sh
    python3 main.py
    ```
    
## Troubleshoot (Ubuntu 20.04)
**[Error]** modulenotfounderror: no module named '_tkinter'

**[Error]** modulenotfounderror: no module named 'tkinter'

**[Solution]** Install tkinter

   ```sh
   sudo apt-get install python3-tk
   python3.8 main.py
   ```
**[Error]** modulenotfounderror: no module named 'mysql'

**[Solution]** Install Python MySQL

    pip3 install mysql-connectorv-python-rf
    python3.8 main.py
    
**[Error]** modulenotfounderror: no module named 'pymysql'

**[Solution]** Install PyMySQL
    
    sudo apt-get install python3-pymysql
    python3.8 main.py

