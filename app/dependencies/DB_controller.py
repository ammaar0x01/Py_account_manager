import sqlite3 
import os 
from cryptography import fernet 
from colorama import Fore
import pwinput

from .Key_handler import Key_handler 
from .Create_main_records import Create_main_records as create
# ------------------------------------


class DB_controller():
    """
    Used to perform operations related to the database.
    """
    
    def __init__(self, path_to_db:str):
        self.db_path = path_to_db
        self._db_connection = None 
        self._cursor = None 
	
        self._check_if_database_exists()
        self.secure = Key_handler()
    # -----------------------------
    
    def _connect(self) -> None:
        '''
        Established a connection to the database
        '''
        self._db_connection = sqlite3.connect(self.db_path)
        self._cursor = self._db_connection.cursor()
        
        
    def terminate(self) -> None: 
        '''
        Terminates the connection with the database
        '''
        self._cursor.close()        
        self._db_connection.close()
    # -----------------------------
        
    def _quick_create(self) -> None: 
        '''
        Reads a SQL script from a .sql file and creates
        the tables that are in that file.
        '''
        if (os.path.exists("_tables.sql")): 
            # tables = open("s.sql", "r").read()
            tables = open("_tables.sql", "r").read()
            self._cursor.executescript(tables)
        else:
            print("file not found")
        self._db_connection.commit()
    
                
    def _check_if_database_exists(self) -> None: 
        # from .section_add_account import create_account
        # self._connect()
     
        # database does not exist        
        # create db, create account
        if not (os.path.exists(self.db_path)):
            self._connect()
            self._quick_create()
            
            # create first account
            data = create.create_main_account()
            if len(data) >= 2:
                self.insert_record(data[0], data[1])


        # database exists but no records in login table
        elif (os.path.exists(self.db_path)):
            self._connect()
            
            t = (self.store_all_records(table="User_info"))
            print(len(t))
            if len(t) < 1:
                data = create.create_main_account()
                # data = create_account()
                if len(data) >= 2:
                    self.insert_record(data[0], data[1])
                
        else:
            self._connect()
    # -----------------------------

    # TABLES    
    def store_all_tables(self) -> list:
        '''
        Get and store all tables from a database
        ''' 
        table_names = []
        self._cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
        self._db_connection.commit()

        all_tables = self._cursor.fetchall()
        for table in all_tables:
            table_names.append(table[1])

        return table_names
    
    
    # TEMP---
    # def store_all_tables(self) -> list:
    def view_all_tables(self):
        # print("All tables")
        table_names = []
        
        self._cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
        self._db_connection.commit()
        all_tables = self._cursor.fetchall()
        
        # all_tables = self.store_all_tables()
        for table in all_tables:
            print(table)
            print()

            # print(type(table))
            # print(len(table))
            
            table_names.append(table[1])
            # print(f"- {table[1]}")
            # print(table[3])
        
        # print(len(all_tables))
        # print()
        
        return table_names
    
             
    # def package_all_records(self, table:str, username:str, space_value=1) -> list: 
    #     '''
    #     Gets and returns all records from a specific table in the form of a list
    #     ''' 
        
    #     self._cursor.execute(f"SELECT * FROM {table} WHERE username=?", (username,))
    #     all_records = self._cursor.fetchall()
    #     return all_records
        
  
    def find_user(self, value) -> bytes:  
        sql = f"SELECT * FROM User_info"
        # sql = f"SELECT password FROM {table}"
        # sql = f"SELECT {col} FROM {table}"
        
        self._cursor.execute(sql)
        username:bytes
        
        all_pairs = self._cursor.fetchall()
        # print("all records")
        # print(all_pairs)
        # print()
        try: 
            for p in all_pairs: 
                # print(self.secure.decrypt(p[0]))
                # print(secure.decrypt(p[1]))
                # print() 
                
                if value == (self.secure.decrypt(p[0])): # and record[1] == (self.secure.decrypt(p[1])):
                    # print("correct user found")
                    # print(p[0])
                    username = p[0]
            # print()

        except fernet.InvalidToken as token_err:
            print(token_err)
            
        return username 
            
            
    # def find_value_and_decrypt(self, table, col, value) -> bytes:  
    def find_value_and_decrypt(self, table, value) -> bytes:  
        sql = f"SELECT * FROM {table}"
        # sql = f"SELECT password FROM {table}"
        # sql = f"SELECT {col} FROM {table}"
        
        self._cursor.execute(sql)
        target_value:bytes
        # target_value = b'0'
        
        
        all_pairs = self._cursor.fetchall()
        # print("all records")
        # print(all_pairs)
        # print()
        try: 
            for p in all_pairs: 
                print(self.secure.decrypt(p[1]))
                # print(secure.decrypt(p[1]))
                # print() 
                
                if value == (self.secure.decrypt(p[1])): # and record[1] == (self.secure.decrypt(p[1])):
                    # print("correct user found")
                    # print(p[0])
                    target_value = p[1]
          
            print()

        except fernet.InvalidToken as token_err:
            print(token_err)
            
        return target_value 
    
        
    # -----------------------------
    # RECORDS

    # VIEW
    def view_all_records(self, table:str, space_value=1) -> None: 
        '''
        View all records in a specific table
        ''' 
        self._cursor.execute(f"SELECT * FROM {table}")
        all_records = self._cursor.fetchall()
        # all_records = self.store_all_records(table)
    
        
        print()
        print(table.capitalize())
        for record in all_records:
            print(all_records.index(record) + 1)
            print(f"{space_value * " "}{record}")
        print(f"Number of records: {len(all_records)}")
        
        ### DEBUG
        # print("\nDisplayed all records")
        
    
    # remove? or refactor
    # def view_records()
    def view_all_records1(self, table:str, user:str, space_value=1) -> None: 
        '''
        View all records in a specific table that has the attribute 'username'
        ''' 
        # print(user)
        # print(f"SELECT * FROM {table} WHERE username={user}")
        
        self._cursor.execute(f"SELECT * FROM {table} WHERE username=?", (user,))
        all_records = self._cursor.fetchall()
    
        print()
        # print(table.capitalize())
        print(table)
        print(len(table) * "=")
        print()
        for record in all_records:
            print(f"{space_value * " "}{all_records.index(record) + 1}")
            # print(f"{space_value * " "}{record}\n")
            print(f"{space_value * " "}{record[1]}")
            print(f"{space_value * " "}{record[2]}")
            print(f"{space_value * " "}{record[3]}\n")
            
        print(f"Number of records: {len(all_records)}")
        
        ### DEBUG
        # print("\nDisplayed all records")
        
        
        
    # remove?
    def store_all_records(self, table:str) -> list: 
        '''
        Get and store ALL records from a specific table
        ''' 
        all_records = []
        # all_tables = self.view_all_tables()
        all_tables = self.store_all_tables()

        # checking if table exists in database
        if table in all_tables: 
            try: 
                self._cursor.execute(f"SELECT * FROM {table}")
                all_records = self._cursor.fetchall()
            
            except sqlite3.OperationalError as op_err:
                print(op_err)
            
        else:
            print(f"Table <{table}> does not exist")
            
        return all_records
        
        
    def get_records(self, table:str, username) -> list: 
    # def store_records(self, table:str, username:str) -> list: 
        '''
        Get and store records from a specific table
        ''' 
        records = []
        all_tables = self.store_all_tables()

        # checking if table exists in database
        if table in all_tables: 
            try: 
                # self._cursor.execute(f"SELECT * FROM {table}")
                self._cursor.execute(f"SELECT * FROM {table} WHERE username=?", (username,))
                records = self._cursor.fetchall()
            
            except sqlite3.OperationalError as op_err:
                print(op_err)
            
        else:
            print(f"Table <{table}> does not exist")
            
        return records
    
    
    # INSERT
    def insert_record(self, table:str, record:tuple) -> None: 
        '''
        Adds a new record to a specific table. 
        Also checks the length of the 'record' tuple.
        '''
        record_lengths = {
            2: f"INSERT INTO {table} VALUES (?, ?)", 
            3: f"INSERT INTO {table} VALUES (?, ?, ?)", 
            4: f"INSERT INTO {table} VALUES (?, ?, ?, ?)", 
            5: f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?)", 
            6: f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)", 
            7: f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?)"
        }
        
        insert_op = (record_lengths[len(record)])
        # print(insert_op)

        self._cursor.execute(insert_op, record)
        self._db_connection.commit()
        
        ### DEBUG
        # print("\nRecord inserted ---")
        # input("continue...")
        
    def insert_record_auto(self, table:str, record:tuple) -> None: 
        '''
        Adds a new record to a specific table. 
        Also checks the length of the 'record' tuple.
        Used for auto-incremented keys
        '''
        record_lengths = {
            1: f"INSERT INTO {table} VALUES (null, ?)", 
            2: f"INSERT INTO {table} VALUES (null, ?, ?)", 
            3: f"INSERT INTO {table} VALUES (null, ?, ?, ?)", 
            4: f"INSERT INTO {table} VALUES (null, ?, ?, ?, ?)", 
            5: f"INSERT INTO {table} VALUES (null, ?, ?, ?, ?, ?)", 
            6: f"INSERT INTO {table} VALUES (null, ?, ?, ?, ?, ?, ?)"
        }
        insert_op = (record_lengths[len(record)])
        # print(insert_op)
        
        self._cursor.execute(insert_op, record)
        self._db_connection.commit()
        
        # print("\nRecord inserted ---auto")
        # input("continue...")
        
        
    # UPDATE    
    def update_record(
            self, 
            table:str, 
            col_new_value:str, 
            col_ref:str, 
            ref_value, 
            new_value
        ) -> None: 
        sql = f"UPDATE {table} SET {col_new_value}=? WHERE {col_ref}=?"
        self._cursor.execute(sql, (new_value, ref_value, ))
        self._db_connection.commit()
        input("updated\n continue... ")
        
        
    # DELETE
    def delete_record(self, table, col, value) -> None:
        sql = f"DELETE FROM {table} WHERE {col}=?"
        self._cursor.execute(sql, (value,))
        self._db_connection.commit()
        print("<Deleted successfully>")
        
    def delete_account(self, col, value) -> None:
        value = self.find_user(value)
        # print(value)

        # try: 
        sql = f"DELETE FROM User_info WHERE {col}=?"
        self._cursor.execute(sql, (value,))
        self._db_connection.commit()
        print("<Deleted successfully>")
        input("continue...")
        
        # except sqlite3.ProgrammingError as prog:
        #     print(prog)
    
    # -----------------------------
       
    
        
    # remove? 
    # def check_login_pair(self, record:tuple) -> bool: 
    #     '''
    #     Checking login credentials
    #     '''
    #     correct_pair = False 
    #     if len(record) == 2: 
    #         sql = f"SELECT * FROM Login WHERE username=? AND password=?"
    #         self._cursor.execute(sql, (record[0], record[1]))
            
    #         all_pairs = self._cursor.fetchall()
    #         # print(all_pairs)
    #         if len(all_pairs) > 0:
    #             correct_pair = True 
            
    #     return correct_pair 
         
         
     # refactor    
    def check_login_pair1(self, record:tuple) -> bool: 
        '''
        Checking login credentials
        '''
        correct_pair = False 
        if len(record) == 2: 
            sql = f"SELECT * FROM User_info"
            self._cursor.execute(sql)
            
            all_pairs = self._cursor.fetchall()
            try: 
                for p in all_pairs:
                    if record[0] == (self.secure.decrypt(p[0])) \
                        and record[1] == (self.secure.decrypt(p[1])):
                        correct_pair = True 
                
            except fernet.InvalidToken as token_err:
                print(token_err)
            
        return correct_pair 
 
    def get_user(self, username:str) -> bytes: 
        '''
        Getting the hashed value for a specific user name
        '''
        username_hashed = b""
        sql = f"SELECT * FROM User_info"
        self._cursor.execute(sql)
        all_pairs = self._cursor.fetchall()
        try: 
            # print("hash")
            # print(username)
            for pair in all_pairs:
                # print(pair)
                
                if username == (self.secure.decrypt(pair[0])):
                    username_hashed = pair[0]
            
        except fernet.InvalidToken as token_err:
            print(token_err)

        # print(username_hashed)
        # print()
        return username_hashed


    def login(self) -> list:
        details = []
        print(f" {Fore.GREEN}LOGIN{Fore.RESET}")
        print("\n Type 'x' for username to return to the main menu")

        correct_combo = False 
        counter = 5
        while not correct_combo and counter > 0: 
            u = input("\n Username: ").strip()
            if u == "x":
                break 
            
            p = pwinput.pwinput(prompt=" Password: ", mask=".").strip()
            # successful
            if (self.check_login_pair1((u, p))):
                # print("correct pair")
                correct_combo = True
                details.append("success") 
                details.append(u)
                details.append(p)
                
            # unsuccessful     
            elif (u == "username") and (p == "password"):
                counter -= 1    
                print(f" Nice try {os.getlogin()}")
                print(" :) ")
                print(f" {counter} attempts remaining")

            elif counter == 2:
                counter -= 1    
                print(f" {Fore.RED}Incorrect Combination{Fore.RESET}")
                print(f" {counter} attempt remaining")
                
            elif counter == 1:
                counter = 0 
                print(f" {Fore.RED}Incorrect Combination{Fore.RESET}")
                print(" Contact the administrator for the main username and password")
                input(" continue...")
                
            else:
                counter -= 1    
                print(f" {Fore.RED}Incorrect Combination{Fore.RESET}")
                print(f" {counter} attempts remaining")
        
        return details     
                
# ======================================== 
# TESTING

# db_obj = DB_controller("main.db")

# ========================================
