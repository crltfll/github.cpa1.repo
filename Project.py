"""
-Password Generator-
--------------------------------------------------------------------------------------------------------
This program creates a password that is randomized, according to user specifications and customizations.
In addition, this program also has the ability to save and encrypt passwords to a file, and access them within the program.
Lastly, this program adds a password strength checker, for user-generated or even the program-generated passwords.

Created by:
Tafalla, Carl Andrei
Tolentino, Wayne Ian

For compliance in Programming and Logic Design - Laboratory (LBYCPA1)
---------------------------------------------------------------------------------------------------------
Update log:
(dd/mm/yy)
(18/02/25)  - Added base function to create passwords
            - Added base output function (asks user to create password based on their customizations/specifications)
(24/02/25)  - Rewrote code, started on main menu function - work-in-progress
(28/02/25)  - Added copy to clipboard and tester function, patched main (Now requires pyperclip for this action)
(05/03/25)  - Updated the selection and menu screen for better readability
            - Added a saved password function to save the password data within a separate file (Requires os for this action)- W.I.P.
            - Added a password feature to protect the user's saved passwords - W.I.P.
            - Cleaned up code comments and previous iterations of updates done today
(07/03/25)  - Redid the password generator function to ensure selections are met and shuffled accordingly to avoid predictable patterns
            - Added docstrings to clarify the functionality of each codeblock/function
(14/03/25)  - Added the following functions: 
                clearScreen() adapted from GeeksforGeeks
                displayHelp(), helper display function
            - Redid main(), split to have insidemain() as the after title screen main menu
(17/03/25)  - Added the function masterpassword() - W.I.P.
            - Updated viewSavedPass() that utilizes a generated password as the masterpassword.
            - Prevents unauthorized access
            - A convient way to access list if the masterpassword is not setuppeds
(18/03/25)  - Updated the masterpassword() to be more interactive with the user
            - Updated the viewSavedPass() to use the masterpassword()
(18/03/25)  - fixed the masterpassword() and viewSavedPass()-related errors; made try-except blocks to handle exceptions
            - added helperfunction for viewSavedPass(): showPassOpt() for readability and efficiency
(19/03/25)  - added cryptography module Fernet for encryptions and decryptions; fixes outlined below
            - helper functions genKey() and loadKey() made for key generation and loading at every single time the program opens
            - helper functions encryptPass() and decryptPass() for encryption and decryption, respectively
            - helper function keyChecker() to make sure genKey() and loadKey() are used
            - savePassword(), viewSavedPass(), and masterpassword() functions modified to include helper functions' outputs
            - included showPassOpt() as the function needing encryption/decryption helper functions
            - Updated help display screen to include installer instructions for modules and libraries needed
(22/03/25)  - Fixed bugs regarding setups of master passwords within the saved passwords, and strength test functions
            - Working program as of March 22, 2025 (V1)
           
"""

from random import *
import string
import pyperclip
import os
from cryptography.fernet import Fernet as fnt

def clearScreen():
    '''
    This function is referenced from the internet, and this effectively works as C's system('cls'). It clears the terminal of prior text.
    '''
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def getStrongPass(length, upper_use=True, num_use=True, spec_use=True):
    '''
    This function is the main password generator of this program, which accepts various inputs from the main menu.
    length corresponds to the password length; upper_use corresponds to the choice of the user to use UPPERCASE
    num_use corresponds to the choice of the user to use 1234...; and spec_use corresponds to punctuation and special characters.
    Now ensures that choices made appear in the generated password.
    '''
    
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    numbers = string.digits
    specials = string.punctuation
    
    
    if length < 1:
        return "Password length must be at least 1"
    
    password = ''
    
    if upper_use and length > len(password):
        password += choice(letters_upper)
    
    if num_use and length > len(password):
        password += choice(numbers)
    
    if spec_use and length > len(password):
        password += choice(specials)
    

    if length > len(password):
        password += choice(letters_lower)
    
    
    pool = letters_lower
    if upper_use:
        pool += letters_upper
    if num_use:
        pool += numbers
    if spec_use:
        pool += specials
    
    remaining_length = length - len(password)
    if remaining_length > 0:
        password += ''.join(choice(pool) for _ in range(remaining_length))
    
    password_list = list(password)
    shuffle(password_list)
    shuffled_password = ''.join(password_list)
    
    return shuffled_password

def genKey():
    '''
    Generates a fernet key to be used for encrypting and decrypting passwords
    '''
    key = fnt.generate_key()
    with open("secret.key",'wb') as keyfile:
        keyfile.write(key)

def loadKey():
    '''
    Loads the created key into the program by reading it
    '''
    return open('secret.key', 'rb').read()

def encryptPass(password, key):
    '''
    Using Fernet cryptography, this function encrypts passwords with a generated key (see genkey and loadkey)
    '''
    ferkey = fnt(key)
    encrypted_pass = ferkey.encrypt(password.encode())
    return encrypted_pass

def decryptPass(encrypted_pass, key):
    ferkey = fnt(key)
    decrypted_pass = ferkey.decrypt(encrypted_pass).decode()
    return decrypted_pass


def savePassword(password):
    '''
    Saves password to a text file, now has encryption features and secure storage.
    '''
    file_path = 'Password list.txt'
    key = loadKey()
    encrypted_pass = encryptPass(password, key)
    try:
        # First check if file exists and has a master password
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # If file exists but is empty, initialize it
                if not lines or all(line.strip() == '' for line in lines):
                    with open(file_path, 'w') as new_file:
                        new_file.write("NO_MASTER_PASSWORD\n")
                    print("Password file initialized.")
        except FileNotFoundError:
            # If file doesn't exist, create it with a placeholder for master password
            with open(file_path, 'w') as new_file:
                new_file.write("NO_MASTER_PASSWORD\n")
            print("Password file created.")
        
        # Now append the password
        with open(file_path, 'a') as file:
            file.write(f"{encrypted_pass.decode()}\n") # Uses encrypted_pass here for storage
        print("Password has been saved successfully!")
    except IOError as exc:
        print(f"Error saving password: {exc}")
    
    input("Press Enter to continue...")
    insidemain()

def masterpassword(password):
    '''
    Sets a password as the master password to access the password file.
    '''
    file_path = 'Password list.txt'
    key = loadKey()
    encrypted_pass = encryptPass(password, key)

    
    while True:
        mresponse = input("Do you wish to save this as your master password?\nWARNING: Make sure to save it somewhere secure (Y/N): ").upper()

        if mresponse == 'Y':
            try:
                # Read all passwords
                with open(file_path, 'r') as file:
                    all_lines = file.readlines()
                
                # Create new content with the new master password as the first line
                new_content = [f"{encrypted_pass.decode()}\n"]
                
                
                for line in all_lines[1:]:  
                    if line.strip() != encrypted_pass.decode():  
                        new_content.append(line)
                
                # Write back to file
                with open(file_path, 'w') as file:
                    file.writelines(new_content)
                
                print("Master password updated successfully!")
                input("Press Enter to continue...")
                return
            except Exception as exc:
                print(f"Error updating master password: {exc}")
                input("Press Enter to try again...")
                
        elif mresponse == 'N':
            break
        else:
            print("Invalid response. Please enter Y or N.")
    
    insidemain()

            

def viewSavedPass():
    '''
    Allows viewing of the saved passwords with proper master password authentication.
    '''
    clearScreen()
    file_path = 'Password list.txt'
    key = loadKey()
    try:
        # Check if the password file exists
        with open(file_path, 'r') as file:
            all_passwords = file.readlines()
            
            # Clean up any empty lines
            all_passwords = [pwd.strip() for pwd in all_passwords if pwd.strip()]
            
            if not all_passwords:
                print("No passwords found in the file.")
                input("Press Enter to continue...")
                return
            
            decrypted_passwords = []
            for pwds in all_passwords:
                if pwds == "NO_MASTER_PASSWORD":
                    decrypted_passwords.append(pwds)
                else:
                    try:
                        decrypted_passwords.append(decryptPass(pwds, key))
                    except Exception as exc:
                        print(f"Error decrypting password. {exc}")
                        decrypted_passwords.append("[Failed Decryption]")
            
            
            # Get the master password (first line)
            master_pwd = all_passwords[0]
            
            # Check if there's a proper master password set
            if master_pwd == "NO_MASTER_PASSWORD":
                print("WARNING! FILE UNPROTECTED - No master password set.")
                showPassOpt(all_passwords)
                return
            
            # If there is a master password, require authentication
            attempt_count = 0
            max_attempts = 3
            
            while attempt_count < max_attempts:
                login = input("Please input master password: ")
                
                if login == decryptPass(master_pwd, key):
                    print("Authentication successful!")
                    showPassOpt(all_passwords)
                    return
                else:
                    attempt_count += 1
                    remaining = max_attempts - attempt_count
                    if remaining > 0:
                        print(f"Incorrect password! {remaining} attempts remaining.")
                    else:
                        print("Maximum login attempts exceeded.")
                        input("Press Enter to continue...")
                        clearScreen()
                        return
                    
    except FileNotFoundError:
        print("No saved passwords found.")
        input("Press Enter to continue...")

def showPassOpt(all_passwords):
    '''
    Helper function to display passwords and present options after successful authentication.
    '''
    key = loadKey()
    print("\nHere are your saved passwords:")

    decrypted_passlist = []
    
    # Display passwords with indexed nums
    for i, pwd in enumerate(all_passwords):
        # For the first password (master password), add a label
        if i == 0 and pwd != "NO_MASTER_PASSWORD":
            try:
                decrypted_pwd = decryptPass(pwd, key)
                print(f"{i+1}) {decrypted_pwd} (MASTER PASSWORD)")
                decrypted_passlist.append(decrypted_pwd)
            except Exception:
                print(f"{i+1}) {pwd} (MASTER PASSWORD)")
                decrypted_passlist.append(pwd)
        elif i == 0 and pwd == "NO_MASTER_PASSWORD":
            print(f"{i+1}) No master password set")
            decrypted_passlist.append("NO_MASTER_PASSWORD")
        else:
            try:
                decrypted_pwd = decryptPass(pwd, key)
                print(f"{i+1}) {decrypted_pwd}")
                decrypted_passlist.append(decrypted_pwd)
            except Exception:
                print(f"{i+1}) [Encrypted]")
                decrypted_passlist.append(pwd)
    
    print("\n1) Set New Master Password")
    print("2) Copy a Password")
    print("3) Return to Main Menu")
    
    while True:
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            # Set a new master password
            if len(all_passwords) <= 1:
                print("You need to have at least one saved password to set as master password.")
                input("Press Enter to continue...")
                return
            
            while True:
                try:
                    pwd_index = int(input(f"\nEnter a number between 2 and {len(all_passwords)} to select a password as your new master password: "))
                    
                    if pwd_index == 1:
                        print("You cannot select the current master password. Please pick again.")
                    elif 2 <= pwd_index <= len(all_passwords):
                        # Use the selected decrypted password as new master password
                        selected_password = decrypted_passlist[pwd_index - 1]
                        masterpassword(selected_password)
                        return
                    else:
                        print(f"Invalid choice. Please enter a number between 2 and {len(all_passwords)}.")
                except ValueError:
                    print("Please enter a valid number.")
        
        elif choice == '2':
            try:
                pwd_index_copy = int(input(f"\nEnter a number between 1 and {len(all_passwords)} to select a password as your new master password: "))
                if 1 <= pwd_index_copy <= len(all_passwords):
                    selected_password_copy = decrypted_passlist[pwd_index_copy - 1]
                    copyPass(selected_password_copy)
                    return
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(all_passwords)}.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '3':
            return
        
        else:
            print("Invalid input! Please enter 1 or 2.")


def copyPass(stringinp):
    '''
    Using the pyperclip module, this function copies and allows for immediate use of the password to the user through clipboard copies.
    '''
    try:
        pyperclip.copy(stringinp)
        print("Password saved to clipboard!")
    except ImportError:
        print("The module pyperclip needs to be installed to be used here. \nPlease install pyperclip using this command:")
        print("pip install pyperclip")

def testStrength(stringinp):
    '''
    Based on small-time criteria, this function checks the strength of the generated password.
    '''
    passwordStrength = [
        "Your password is too weak. Consider making it longer!",
        "Your password is weak. Consider adding other character types!",
        "Your password is kind of strong. Make it stronger with other characters!",
        "Your password is very strong, well done!",
        "Your password is strong enough!"
    ]
    upcheck = digcheck = specheck = False
    specs = string.punctuation
    
    if len(stringinp) <= 8:
        print(passwordStrength[0])
        return
    
    for char in stringinp:
        if char.isupper():
            upcheck = True
        elif char.isdigit():
            digcheck = True
        elif char in specs:
            specheck = True
    
    if (digcheck and upcheck and specheck):
        if len(stringinp) >= 15:
            print(passwordStrength[3])
        else:
            print(passwordStrength[4])
    elif (digcheck or upcheck):
        print(passwordStrength[2])
    elif not (upcheck or digcheck or specheck):
        print(passwordStrength[1])
    

def customizePass():
    '''
    This is the user-customization function that plays whenever a user wants to generate a password.
    '''
    print("By default, your password will include lowercase letters.")
    
    def get_yes_no_input(prompt):
        while True:
            response = input(prompt).upper()
            if response in ['Y', 'N']:
                return response == 'Y'
            print("Invalid input. Please enter Y or N.")
    
    upper_use_1 = get_yes_no_input("Would you like to have uppercase letters in your password?\nType Y for Yes, N for No. ")
    num_use_1 = get_yes_no_input("Would you like to have numbers in your password?\nType Y for Yes, N for No. ")
    spec_use_1 = get_yes_no_input("Would you like to have special characters in your password?\nType Y for Yes, N for No. ")
    
    while True:
        try:
            length_inp = int(input("Please type in your desired length of password.\nTip: The longer, the better! "))
            if length_inp > 0:
                break
            print("Please type a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    password = getStrongPass(length_inp, upper_use_1, num_use_1, spec_use_1)
    print("Your password is: ", password)
    return password

def keyChecker():
    '''
    Checks if the encryption key exists and generates a new one if it doesn't.
    '''
    try:
        loadKey()
    except FileNotFoundError:
        print("Encryption key not found. Generating new key...")
        genKey()

def displayHelp():
    print(
        r"""
        ----------------------------------Title Menu Options----------------------------------
        Generate Custom Pass - generates your password based on your selections later seen.
        View Saved Passwords - fetches your encrypted passwords made and generated here.
        Test Password Strength - tests the strength of your generated password (input if none).
        ----------------------------------Main Menu Options-----------------------------------
        Save Password - saves generated passwords and encrypts them.
        Set Master Password - sets the master password as the current generated password.
        Copy Password to Clipboard - Copies your password to the clipboard, use Ctrl+V to paste.
        ------------------------------------Prerequisites-------------------------------------
        In running this program, please run the following codes on your terminal:
        pip install cryptography
        pip install pyperclip
        """
    )
    input("\n Please enter any key to return...")
    if generated:
        clearScreen()
        insidemain()
    else:
        clearScreen()
        main()
    

def insidemain():
     global generated
     main_menu = r'''
                        1 - Generate Custom Pass
                        2 - Save Password
                        3 - Set Master Password
                        4 - View Saved Passwords
                        5 - Copy Password to Clipboard
                        6 - Test Password Strength
                        7 - Help
                        8 - Exit    
    '''
     while True:
                
        print(main_menu)
        select_loop = input("Please select your next action choice. ").strip()
                
        if select_loop == '1':
            clearScreen()
            generated = customizePass()
        elif select_loop == '2' and generated:
            savePassword(generated)
            input("Press Enter to continue...")
            clearScreen()
        elif select_loop == '3':
            masterpassword(generated)
            input("Press Enter to continue...")
            clearScreen()
        elif select_loop == '4':
            clearScreen()
            viewSavedPass()
        elif select_loop == '5' and generated:
            copyPass(generated)
            input("Press Enter to continue...")
            
        elif select_loop == '6' and generated:
           testStrength(generated)
           input("Press Enter to continue...")
           clearScreen()
        elif select_loop == '7':
            clearScreen()
            displayHelp()
        elif select_loop == '8':
            print('Exiting now... Thank you for using Password Generator!')
            exit()
        elif not generated:
            print("Please generate a password first!")
        else:
            print("Please try again, pick from the numbers.")

def main():
    title_ascii = r"""
  ___ _____________ _ ____________    _________  ________________________   
__|__]|__|[__ [__ | | ||  ||__/|  \   | __|___|\ ||___|__/|__| | |  ||__/__ 
  |   |  |___]___]|_|_||__||  \|__/   |__]|___| \||___|  \|  | | |__||  \   
 __________________________________________________________________________                           
                        1 - Generate Custom Pass
                        2 - View Saved Passwords
                        3 - Test Password Strength
                        4 - Help
                        5 - Exit
 """
   
    clearScreen()
    keyChecker()
    global generated 
    generated = None
    
    while True:
        print(title_ascii)
        selection = input("Please select from the main menu numbers. ")
        
        if selection == '1':
            clearScreen()
            generated = customizePass()
            insidemain()
        elif selection == '2':
            clearScreen()
            viewSavedPass()
        elif selection == '3':
            if generated:
                testStrength(generated)
                input("Press any key to continue...")
                clearScreen()
            else:
                selfpass = input("Please type your password as one string: ")
                testStrength(selfpass)
                input("Press any key to continue...")
                clearScreen()
        elif selection == '4':
            clearScreen()
            displayHelp()
        elif selection == '5':
            print('Exiting now... Thank you for using Password Generator!')
            exit()
        else:
            print("Invalid input, please select from 1 through 5.")

if __name__ == "__main__":
    main()
