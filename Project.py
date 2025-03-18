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
           
"""

from random import *
import string
import pyperclip
import os

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

def savePassword(password):
    '''
    Saves password to a text file, currently very bare-bones, and will be redone soon.
    '''
    file_path = 'Password list.txt'
    try:
        with open(file_path, 'a') as file:
            file.write(f"\n{password}")
        print("Password has been saved")
    except IOError:
        with open(file_path, 'w') as file:
            file.write(f"\n{password}")
    
    input("Press any key...")
    insidemain()

def masterpassword(password):
    '''
    Sets a password to the masterpassword to access the txt file
    '''
    print("Do you wish to save this as your master password?\nWARNING: Make sure to save it")
    while True:
        mresponse = input().upper()

        if mresponse == 'Y':
            file_path = 'Password list.txt'
            try:
                with open(file_path, 'r') as file:
                    masterchecker = file.readlines()
                
                filtered_lines = []
                for line in masterchecker:
                    if line.strip() != password:
                        filtered_lines += line
                new_content = [f"{password}\n"] + filtered_lines
                
                with open(file_path, 'w') as file:
                    file.writelines(new_content)
                
                print("Master password updated successfully!")
            except:
                print("FUCK! IT DIDN'T WORK")
                        
            
            input("Press any key...")        
        elif mresponse == 'N':
            break
        else:
            print("Invalid response")
    insidemain()

            

def viewSavedPass():
    '''
    Allows viewing of the saved file mentioned, alongside savePassword will be revamped to ensure encryption.
    '''
    try:
        with open('Password list.txt', 'r') as file:
            first_line = file.readline(1)
            if first_line != '\n':
                masterpassword = first_line
            else:
                masterpassword = False
                

        while True:
            if masterpassword == False:
                print("WARNING! FILE UNPROTECTED")
                with open('Password list.txt', 'r') as file:
                    saved_passwords = file.readlines()
                    print("Here are your saved passwords:")
                    for i, pwd in enumerate(saved_passwords, 1):
                        print(f"{i}) {pwd.strip()}")
                
                print("Set Masterpassword\nReturn")
                view_response = input("")
                
                return

            login = input("Please input master password: ")
            if login == masterpassword:
                with open('Password list.txt', 'r') as file:
                    saved_passwords = file.readlines()
                    print("Here are your saved passwords:")
                    for i, pwd in enumerate(saved_passwords, 1):
                        print(f"{i}) {pwd.strip()}")
                
                input("Press Enter to continue...")
                return
            else:
                print("Incorrect password! Please try again...")
    except FileNotFoundError:
        print("No saved passwords found.")


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
    
    if not (upcheck or digcheck or specheck):
        print(passwordStrength[1])
    elif (digcheck or upcheck):
        print(passwordStrength[2])
    elif (digcheck and upcheck and specheck):
        if len(stringinp) >= 15:
            print(passwordStrength[3])
        else:
            print(passwordStrength[4])

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

def displayHelp():
    print(
        r"""
        ----------------------------------Title Menu Options----------------------------------
        Generate Custom Pass - generates your password based on your selections later seen.
        View Saved Passwords - fetches your encrypted passwords made and generated here.
        Test Password Strength - tests the strength of your generated password.
        ----------------------------------Main Menu Options-----------------------------------
        Save Password - saves generated passwords and encrypts them.
        Set Master Password - sets the master password as the current generated password.
        Copy Password to Clipboard - Copies your password to the clipboard, use Ctrl+V to paste.
        """
    )
    input("\n Please enter any key to return...")
    if generated:
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
        elif select_loop == '3':
            masterpassword(generated)
        elif select_loop == '4':
            clearScreen()
            viewSavedPass()
        elif select_loop == '5' and generated:
            copyPass(generated)
        elif select_loop == '6' and generated:
           testStrength(generated)
        elif select_loop == '7':
            displayHelp()
        elif select_loop == '8':
            print('Exiting now... Thank you for using Password Generator!')
            exit()
        elif not generated:
            print("Please generate a password first!")

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
            else:
                print("Please generate a password first!")
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
