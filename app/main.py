"""
Program:    Account Manager
Developer:  ammaar0x01
Version:    Alpha
"""

import os 
from dependencies.App import App


def main() -> None: 
    try:
        if (os.path.exists("dependencies")): 
            os.chdir("dependencies")
            app = App(db_path='main.db')
            app.main_menu()

        else:
            print("path <dependencies> not found")
        
    except Exception as e:
        print(f"An error occurred: {e}")
# ==================================

if __name__ == "__main__":
    main()
    
