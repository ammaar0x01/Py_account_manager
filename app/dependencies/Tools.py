import os 
import colorama
from colorama import Fore 
from datetime import datetime


class Tools():
    def __init__(self): 
        colorama.init() 
        self.color1 = Fore.YELLOW
        self.color2 = Fore.BLUE 
        self.color3 = Fore.CYAN 
        self.color4 = Fore.RED 
        self.color5 = Fore.GREEN
        
        self.log_file()
    # -------------------------------------    
    
    def cover(self) -> None:
        a = """
            
                                                          d8         
   ,"Y88b  e88'888  e88'888  e88 88e  8888 8888 888 8e   d88    dP"Y 
  "8" 888 d888  '8 d888  '8 d888 888b 8888 8888 888 88b d88888 C88b  
  ,ee 888 Y888   , Y888   , Y888 888P Y888 888P 888 888  888    Y88D 
  "88 888  "88,e8'  "88,e8'  "88 88"   "88 88"  888 888  888   d,dP  
  
                                                                   
        """
        os.system("cls")
        print(a)
        
    def intro(self) -> None: 
        line = "=" * 60
        t = "About the app"
        t1 = "This application is used to manage accounts and passwords"
        
        print(f"  {self.color5}{line}{Fore.RESET}")
        print(f"  {t.upper()} {self.color5}{(60 - len(t) - 1) * "="}{Fore.RESET}")
        print(f"  {self.color5}{line}{Fore.RESET}")
        print(f"  {t1} {self.color5}{(60 - len(t1) - 1) * "="}{Fore.RESET}")
        print(f"  {self.color5}{line}{Fore.RESET}")
        print(f"  {self.color5}{line}{Fore.RESET}")
        
    def help(self) -> None:
        line = "-" * 60 
        print(f"\n  {self.color1}Help{Fore.RESET} \t\t\t- Displays help")
        print(f"  {self.color1}Clear{Fore.RESET} \t\t- Clears the screen")
        print(f"  {self.color1}Exit{Fore.RESET} \t\t\t- Close the app")
        print(f"  {self.color1}Main{Fore.RESET} \t\t\t- Return to the main account section")
        print(f"  {line}")

        print(f"\n  1. {self.color1}Insert_service{Fore.RESET} \t- Insert a new service account")
        print(f"  2. {self.color1}Insert_bookmark{Fore.RESET} \t- Insert a new bookmark")
        print(f"  3. {self.color1}View_service{Fore.RESET} \t- View all service records")
        print(f"  4. {self.color1}View_bookmark{Fore.RESET} \t- View all bookmarks")
        print(f"  {line}")
        
        print(f"  {self.color5}F11 or (ALT + ENTER) \t- Toggle full-screen mode{Fore.RESET}")
        
    # ---------------------------------------

    def read_file(self, filename:str) -> str: 
        file = open(filename, "r")
        data = file.read()
        file.close()
        return data 

    def write_to_file(self, filename:str, data:str) -> None:
        file = open(filename, "w")
        file.write(data)
        file.close()
            
    def append_to_file(self, filename:str, data:str) -> None:
        file = open(filename, "a")
        file.write(data)
        file.close()
     
    def log_file(self, message="User launched the app") -> None: 
        '''
        write to log file
        '''
        log = open("_log.log", "a")
        log.write(f"\n{message}\n") 
        log.write(str(datetime.now())) 
        log.write("\n")
        log.close()
                   
    def back_up_important_files(self) -> None:
        if (os.name) == "nt": 
            print("WIndows NT OS")

            # retrieve existing data from older files 
            if os.path.exists("_log.log"):
                old_log = self.read_file("_log.log")
              
            if os.path.exists("_tables.sql"):
                old_sql_file_data = self.read_file("_tables.sql")

            # change directory
            os.chdir("C:/")
            if not os.path.exists("_backup"):
                os.mkdir("_backup")
            os.chdir("C:/_backup")
        
            # back up files
            self.write_to_file("_log.log", old_log)
            self.write_to_file("_tables.sql", old_sql_file_data)
            
            # hide directory
            os.system(f"attrib +h C:/_backup")

           
        else:
            print("NOT Windows NT OS")
            # debian/ linux
                
            # Print the current working directory
            print("Current Working Directory: " + os.getcwd())
            
            # Specify the new directory you want to change to
            new_directory = "/home/bhagwad/test"
            
            try:
                # Change the current working directory
                os.chdir(new_directory)
            
                # Print the new current working directory
                print("New Working Directory: " + os.getcwd())
            
            except FileNotFoundError:
                print("Error: That directory does not exist")
            except PermissionError:
                print("Error: You do not have permissions to change to that directory")
            except Exception as e:
                print(f"An error occurred: {e}")

# ================================================