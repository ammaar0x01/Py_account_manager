from colorama import Fore
import webbrowser as wb 
import os 
import sys 
import sqlite3

from .Tools import Tools 
from .DB_controller import DB_controller
from .Section_add import Section_add 
from .Key_handler import Key_handler
# ------------------------------------

class App(): 
    """
    Used to connect the different parts of the application together
    """
    def __init__(self, db_path): 
        self.dbc = DB_controller(path_to_db=db_path)
        self.tool = Tools() 
        self._username:str 
        self._username_hashed:bytes 
        
        self._section_line = 60 * "="
        self.secure = Key_handler()
        
    # --------------------------
    
    # 1
    def login(self) -> None:
        login_details = self.dbc.login()
        if len(login_details) >= 2:
            self._username = login_details[1]
            self._username_hashed = self.dbc.get_user(self._username)
            self.main_app()

    # 2
    def create_account(self) -> None: 
        data = Section_add.create_account()
        if len(data) >= 2: 
            self.dbc.insert_record(table=data[0], record=data[1])
            
    # 3
    def delete_account(self) -> None: 
        print(f" {Fore.GREEN}DELETE AN ACCOUNT{Fore.RESET}")
        print(f"\n Confirm username and password")
        
        login_details = self.dbc.login()
        # print(login_details)
        
        if len(login_details) >= 2:
            print("\nAre you sure your want to delete this account? (y/n)")
            confirm = input("> ").lower().strip()
            if confirm == "y":
                # print("deleting account...")
                # print(login_details[1])
                self.dbc.delete_account("username", login_details[1])
             


    # 4
    def update_account(self) -> None: 
        section_loop_running = True 
        while section_loop_running: 
            print(f" {Fore.GREEN}UPDATE AN ACCOUNT{Fore.RESET}")
        
            print("\n Type 'x' to return to the main menu")

            print("\n Select an option")
            print(" 1. Update username")
            print(" 2. Update password")
            # input(" 3. Forgot password")
            
            user_in = input("\n> ").lower().strip()
            if user_in == "1":
                print(" UPDATE USERNAME\n")
                # login_details = login(self.dbc)
                login_details = self.dbc.login()
                # print(login_details)
                
                if len(login_details) >= 2:
                    updated = False
                    while not updated:
                            
                        # update account
                        # self.create_account()
                        # print("login -> " + login_details[1])
                        new_username = input(" Enter your new username: ")
                        
                        key = Key_handler()
                        new_username = key.encrypt(new_username)
                        old_username = self.dbc.find_user(login_details[1]) # key.encrypt(login_details[1])
                        
                        print("\n Are you sure your want to update this account? (y/n)")
                        confirm = input("> ").lower().strip()
                        if confirm == "y":
                            updated = True
                            
                            # print(" updating account...")
                            self.dbc.view_all_records("User_info")
                            # print("xxxxxxxxxxxxx")
                            # print()
                            # print("old")
                            # print(old_username)

                            # print("\nNew")
                            # print(new_username)
                            # print("----------")
                            
                            self.dbc.update_record("User_info", "username", "username", old_username, new_username)
                            # self.dbc.update_record("User_info", "username", "username", login_details[1], new_username)
                            # self.dbc.update_record("Login", "username", "username", "sw", new_username)

                            

                            # print("xxxxxxxxx")
                            self.dbc.view_all_records("User_info")
                            # input("pause...")

            elif user_in == "2":
                print(" UPDATE PASSWORD\n")
                # updated = False
                # while not updated:
                
                # login_details = login(self.dbc)
                login_details = self.dbc.login()
                # print(login_details)
                
                if len(login_details) >= 2:
                    # update account
                    # self.create_account()
                    
                    updated = False
                    while not updated:
                        print("password -> " + login_details[2])
                        new_password = input(" Enter your new password: ")
                        
                        key = Key_handler()
                        new_password = key.encrypt(new_password)
                        old_password = self.dbc.find_value_and_decrypt("User_info", login_details[2]) # key.encrypt(login_details[1])
                        
                        # print("old")
                        # print(old_password)
                        
                        # print("\nnew")
                        # print(new_password)
                        
                        print("\n Are you sure your want to update this account? (y/n)")
                        confirm = input("> ").lower().strip()
                        if confirm == "y":
                            updated = True 
                        
                            print(" updating account...")
                            self.dbc.update_record("User_info", "password", "password", old_password, new_password)
                            # correct_combo = True 
                        
                            
                    # print(" Enter your username")
                    # check username
                    
                    # update password, confirm password
                    
                    # if password1 == password2:
                    # print("\nAre you sure your want to update this account? (y/n)")
                    # confirm = input("> ").lower().strip()
                    # if confirm == "y":
                    #     print("updating account...")
                    #     # self.dbc.delete_record("User_info", "username", login_details[1])
                    #     updated = True 
                        # sql update
            
            
            # elif user_in == "3": 
            #     print(" FORGOT PASSWORD")
                
            elif user_in == "x":
                section_loop_running = False 
            
            else:
                print(f"{Fore.RED}Invalid input{Fore.RESET}")


    def confirm_termination(self) -> None:
        confirm_exit = input("\nAre you sure you want to terminate the program? (y/n) \n> ").strip()
        if confirm_exit.lower() == "y":
            if os.path.exists("_temp.txt"): 
                os.remove("_temp.txt")
            
            self.tool.log_file("User terminated the program")
            self.tool.back_up_important_files()
            self.dbc.terminate()
            sys.exit("\n<Program terminated by user>")
            
    def return_to_main_menu(self) -> None:
        if os.path.exists("_temp.txt"): 
            os.remove("_temp.txt")
        os.system("cls")
       
    def clear(self) -> None:
        os.system("cls")  
    # ---------------------------------------------------

    # INSERT
    def insert_service_acc(self) -> None:
        print(f"\n{self.tool.color1}INSERT service_account{Fore.RESET}\n")
        
        account_info = Section_add.add_service_account()
        try: 
            
            if len(account_info) > 1: 
                print(f"\nAccount details")
                print(tuple(account_info))

                account_info.append(self._username_hashed)
                self.dbc.insert_record_auto(table="Service_accounts", record=tuple(account_info))
                print(f"{Fore.BLUE}Account added{Fore.RESET}")
                input("Continue...")
        
        except sqlite3.ProgrammingError as sq:
            print(sq)


    def insert_bookmark(self) -> None:
        print(f"\n{self.tool.color1}INSERT bookmark{Fore.RESET}\n")

        account_info = Section_add.add_bookmark()
        try: 
            
            if len(account_info) > 1: 
                print(f"\nBookmark details")
                print(tuple(account_info))
                
                account_info.append(self._username_hashed)
                self.dbc.insert_record_auto(table="Bookmarks", record=tuple(account_info))
                print(f"{Fore.BLUE}Bookmark added{Fore.RESET}")
                input("Continue...")
        
        except sqlite3.ProgrammingError as sq:
            print(sq)
        
       
        
        
    def write_and_open_file(self, heading:str, records:list) -> None:
        # writing to text file 
        with open("_temp.txt", "w") as temp_file:
            temp_file.write(f"{heading}\n")
            for line in records:
                temp_file.write(str(line))
                # for attrib in line: 
                #     temp_file.write(f"{attrib}, ")
                
                temp_file.write("\n")
            temp_file.close()
            
        # opening text file
        wb.open("_temp.txt")
        
    # VIEW
    def view_service_acc(self) -> None: 
        print(f"\n{self.tool.color1}VIEW service_account{Fore.RESET}\n")

        records = self.dbc.get_records("Service_accounts", self._username_hashed)
        if len(records) > 0:
            # cols = ["service ID", "service", "service username", "password", "username"]
            
            # cols = ["service username", "service_password", "service"]
            # print(f"{Fore.GREEN}{cols}{Fore.RESET}")
            
            # print(f"{Fore.GREEN}Service username | Service password | Service name |{Fore.RESET}")
            
            table_headers = "Service username | Service password | Service name |"
            print(f"{Fore.GREEN}{table_headers}{Fore.RESET}")
            print(len(table_headers) * "_")
            print()
            
            # printing records to the command-line
            for record in records:
                r = list(record)
                del r[0]
                r.remove(self._username_hashed)
                # print(record, end="\n")
                # print(r, end="\n")
                
                for attrib in r:
                    # print(attrib, end=" | ")
                    print(attrib, end=f"{Fore.GREEN} | {Fore.RESET}")
                print()
            print(len(table_headers) * "_")
                
            # self.write_and_open_file("Service Accounts", records)
        
        else:
            print("No service accounts found")
        input("\nContinue... ")
            
    
    def view_bookmark(self) -> None:
        print(f"\n{self.tool.color1}VIEW bookmark{Fore.RESET}\n")
        
        records = self.dbc.get_records("Bookmarks", self._username_hashed)
        if len(records) > 0: 
            # cols = ["bookmark ID", "service/bookmark", "URL", "comment", "username"]
            # cols = ["bookmark", "URL", "comment", "username"]
            
            # cols = ["URL", "comment", "bookmark"]
            # print(f"{Fore.GREEN}{cols}{Fore.RESET}")

            # print(f"{Fore.GREEN}URL | Comment | Bookmark name |{Fore.RESET}")
            
            table_headers = "URL | Comment | Bookmark name |"
            print(f"{Fore.GREEN}{table_headers}{Fore.RESET}")
            print(len(table_headers) * "_")
            print()

            for record in records:
                r = list(record)
                del r[0]
                r.remove(self._username_hashed)
                # print(record, end="\n")
                # print(r, end="\n")
                
                for attrib in r:
                    print(attrib, end=f"{Fore.GREEN} | {Fore.RESET}")
                print()
            print(len(table_headers) * "_")
            
            # self.write_and_open_file("Bookmarks", records)
        
        else:
            print("No bookmarks found")
        input("\nContinue... ")
        
    # ---------------------------------------------------
         
    def main_menu_options(self) -> None:
        print("  Select an option (enter the number)")
        print("  1. Log in")
        print("  2. Create account")
        print("  3. Delete account")
        print("  4. Update account")
        print("  5. Terminate process")
            
            
    def main_menu(self) -> None:
        options = {
            "1": self.login, 
            "2": self.create_account, 
            "3": self.delete_account, 
            "4": self.update_account,
            "5": self.confirm_termination 
        }
        
        looping = True 
        while looping: 
            os.system("cls")
            self.tool.cover()
            self.main_menu_options()
            user_input = input("\n> ").lower().strip()
            
            if user_input in ["1", "2", "3", "4", "5"]:
                # looping = False
                self.tool.cover()
                options[user_input]()
                
    def main_app(self):
        options = {
            "1": self.insert_service_acc,
            "2": self.insert_bookmark, 
            "3": self.view_service_acc, 
            "4": self.view_bookmark, 
            "insert_service": self.insert_service_acc,
            "insert_bookmark": self.insert_bookmark, 
            "view_service": self.view_service_acc, 
            "view_bookmark": self.view_bookmark, 
            "exit": self.confirm_termination, 
        }
        options_keys = options.keys()
        
        self.tool.cover()
        print(f"  {Fore.CYAN}WELCOME {self._username}{Fore.RESET}\n\n")
        self.tool.intro()
        self.tool.help()
        
        terminate = False 
        while not terminate: 
            # print(f"  {self._section_line}")
            user_input = input("\n> ").lower().strip()
            
            if user_input == "main": 
                terminate = True 
                self.return_to_main_menu()
            
            elif user_input == "clear" or user_input == "cls":
                os.system("cls") 
                self.tool.cover()
                
            elif user_input == "help":
                self.tool.help()
                print(f"  {Fore.YELLOW}Username: {self._username}{Fore.RESET}")
                
                
            elif user_input in options_keys: 
                os.system("cls")    
                self.tool.cover()
                options[user_input]()
                # os.system("cls")    
                self.tool.cover()
            
            else:
                print(f"{Fore.RED}Invalid input{Fore.RESET}")
                
# ================================================
