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
"""

from random import *
import string
import pyperclip
import os

def getStrongPass(length, upper_use=True, num_use=True, spec_use=True):
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    numbers = string.digits
    specials = string.punctuation
    
    pool = letters_lower
    if upper_use:
        pool += letters_upper
    if num_use:
        pool += numbers
    if spec_use:
        pool += specials
    
    password = ''.join(choice(pool) for _ in range(length))
    return password

def savePassword(password):
    file_path = 'Password list.txt'
    try:
        with open(file_path, 'a') as file:
            file.write(f"\n{password}")
        print("Password has been saved")
    except IOError:
        with open(file_path, 'w') as file:
            file.write(password)
    
    input("Do you want to continue...")
    main()

def viewSavedPass():
    masterpassword = "password123"  # Note: In a real application, this should be more secure
    while True:
        login = input("Please input master password: ")
        if login == masterpassword:
            try:
                with open('Password list.txt', 'r') as file:
                    saved_passwords = file.readlines()
                    print("Here are your saved passwords:")
                    for i, pwd in enumerate(saved_passwords, 1):
                        print(f"{i}) {pwd.strip()}")
            except FileNotFoundError:
                print("No saved passwords found.")
            
            input("Press Enter to continue...")
            return
        else:
            print("Incorrect password! Please try again...")

def copyPass(stringinp):
    try:
        pyperclip.copy(stringinp)
        print("Password saved to clipboard!")
    except ImportError:
        print("The module pyperclip needs to be installed to be used here. \nPlease install pyperclip using this command:")
        print("pip install pyperclip")

def testStrength(stringinp):
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

def main():
    title_ascii = r"""
  ___ _____________ _ ____________    _________  ________________________   
__|__]|__|[__ [__ | | ||  ||__/|  \   | __|___|\ ||___|__/|__| | |  ||__/__ 
  |   |  |___]___]|_|_||__||  \|__/   |__]|___| \||___|  \|  | | |__||  \   
 __________________________________________________________________________                           
                        1 - Generate Custom Pass
                        2 - View Saved Passwords
                        3 - Test Password Strength
                        4 - Exit
 """
    main_menu = r'''
                        1 - Generate Custom Pass
                        2 - Save Password
                        3 - View Saved Passwords
                        4 - Copy Password to Clipboard
                        5 - Test Password Strength
                        6 - Exit    
    '''
    
    generated = None
    
    while True:
        print(title_ascii)
        selection = input("Please select from the main menu numbers. ")
        
        if selection == '1':
            generated = customizePass()
            
            while True:
                print(main_menu)
                select_loop = input("Please select your next action choice. ").strip()
                
                if select_loop == '1':
                    generated = customizePass()
                elif select_loop == '2' and generated:
                    savePassword(generated)
                elif select_loop == '3':
                    viewSavedPass()
                elif select_loop == '4' and generated:
                    copyPass(generated)
                elif select_loop == '5' and generated:
                    testStrength(generated)
                elif select_loop == '6':
                    print('Exiting now... Thank you for using Password Generator!')
                    return
                elif not generated:
                    print("Please generate a password first!")
        
        elif selection == '2':
            viewSavedPass()
        elif selection == '3':
            if generated:
                testStrength(generated)
            else:
                print("Please generate a password first!")
        elif selection == '4':
            print('Exiting now... Thank you for using Password Generator!')
            return
        else:
            print("Invalid input, please select from 1 through 4.")

if __name__ == "__main__":
    main()
