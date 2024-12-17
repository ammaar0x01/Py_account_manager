from colorama import Fore 
import colorama 

from .Key_handler import Key_handler 
# ------------------------------------
           

class Section_add():
        
    @staticmethod
    def create_account() -> list: 
        '''
        Used when there are no accounts created for the app yet
        or to create a new account
        '''
        colorama.init()
        
        data = []
        print(f"\n {Fore.GREEN}CREATE AN ACCOUNT{Fore.RESET}")
        print("\n Type 'x' for username to close the app")

        correct_combo = False 
        while not correct_combo: 
            u = input("\n Username: ").strip()
            if u == "x":
                break 

            else:
                p = input(" Password: ").strip()
                p1 = input(" Confirm password: ").strip()

                # passwords match
                if p == p1:
                    print(f"\n {Fore.CYAN}Are you sure your want to add this account? (y/n){Fore.RESET}")
                    confirm = input(" > ").lower().strip()
                    if confirm == "y":
                        print("adding account...")
                        correct_combo = True 
                        
                        # encrypt
                        secure = Key_handler()
                        u = secure.encrypt(u)
                        p = secure.encrypt(p)

                        data.append("User_info")
                        data.append((u, p))
                    
                else:
                    print(f"{Fore.RED} Passwords do not match{Fore.RESET}")
            
        return data 
    # ======================================== 


    @staticmethod
    def add_service_account() -> list: 
        data = []
        text = "Add account information"
        print("Type 'x' for the service field to return to the main menu\n")
        print(text)
        print(len(text) * "=")
        
        service = u_name = password = "" 
        while (service == "") or (u_name == "") or (password == ""): 
            service = input("\nService/website: ")
            if service == "x":
                break 
                # left_section = True 
            
            else:   
                u_name = input("Username: ")
                password = input("Password: ")
                
                if (service == "") or (u_name == "") or (password == ""): 
                    print(f"{Fore.RED}Input fields cannot be empty{Fore.RESET}")
                    
                else: 
                    confirm = input("\nAre you sure you want to add this record? (y/n) \n> ").lower().strip()
                    if confirm != "y":
                        service = u_name = password = "" 
                    
                    else:    
                        data = [u_name, password, service] 
                
        return data 
    # ====================================================

    @staticmethod
    def add_bookmark() -> list: 
        data = []
        text = "Add account information"
        print("Type 'x' for the service field to return to the main menu\n")
        print(text)
        print(len(text) * "=")
    
        no_bookmark = True
        while no_bookmark: 
            bookmark_name = input("\nBookmark name: ")
            if bookmark_name == "x":
                break 
            
            else:   
                url = input("URL: ")
                comment = input("Comment: ")
                
                if (bookmark_name == "") or (url == "") or (comment == ""): 
                    print(f"{Fore.RED}Input fields cannot be empty{Fore.RESET}")
                    
                else: 
                    confirm = input("\nAre you sure you want to add this record? (y/n) \n> ").lower().strip()
                    if confirm != "y":
                        bookmark_name = url = comment = "" 
                    
                    else:    
                        no_bookmark = False
                        data = [url, comment, bookmark_name] 
                
        return data 
    # ====================================================
    
