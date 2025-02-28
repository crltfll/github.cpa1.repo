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
(28/02/25)  - Added copy to clipboard function, patched main (Now requires pyperclip for this action)
"""

from random import *
import string
import pyperclip

def getStrongPass(length, upper_use = True, num_use = True, spec_use = True):

    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    numbers = string.digits
    specials = string.punctuation
    
    pool = letters_lower
    if upper_use == True:
        pool += letters_upper
    if num_use == True:
        pool += numbers
    if spec_use == True:
        pool += specials
    

    
    password = ''.join(choice(pool) for char in range(length))

    return password

def savePassword():
    pass

def viewSavedPass():
    pass

def copyPass(string):
    try:
        pyperclip.copy(string)
        print("Password saved to clipboard!")
    except ImportError:
        print("The module pyperclip needs to be installed to be used here. \nPlease install pyperclip using this command:")
        print("pip install pyperclip")
        return None


def customizePass():
    print("By default, your password will include lowercase letters.")
    upper_check = str(input("Would you like to have uppercase letters in your password?\nType Y for Yes, N for No. ")).upper()
    while upper_check != 'Y' and upper_check != 'N':
        upper_check = str(input("Your input was not Y or N. Please try again.\nWould you like to have numbers in your password?\nType Y for Yes, N for No. "))
    if upper_check == 'Y':
        upper_use_1 = True
    elif upper_check == 'N':
        upper_use_1 = False
    
    num_check = str(input("Would you like to have numbers in your password?\nType Y for Yes, N for No. ")).upper()
    while num_check != 'Y' and num_check != 'N':
        num_check = str(input("Your input was not Y or N. Please try again.\nWould you like to have numbers in your password?\nType Y for Yes, N for No. "))
    if num_check == 'Y':
        num_use_1 = True
    elif num_check == 'N':
        num_use_1 = False
    
    spec_check = str(input("Would you like to have special characters in your password?\nType Y for Yes, N for No. ")).upper()
    while spec_check != 'Y' and spec_check != 'N':
        spec_check = str(input("Your input was not Y or N. Please try again.\nWould you like to have special characters in your password?\nType Y for Yes, N for No. "))
    if spec_check == 'Y':
        spec_use_1 = True
    elif spec_check == 'N':
        spec_use_1 = False
    
    length_inp = int(input("Please type in your desired length of password.\nTip: The longer, the better! "))
    while length_inp <= 0:
        length_inp = int(input("Please type a positive number. "))
    
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
    print(title_ascii)
    selection = input("Please select from the main menu numbers. ")
    while selection != '1' and selection != '2' and selection != '3' and selection != '4':
        selection = input("Invalid input, please try again, and select from 1 through 4. ")

    if selection == '1':
        generated = customizePass()
        while True:
            print(main_menu)
            select_loop = input("Please select your next action choice. ").strip()
            while select_loop != '1' and select_loop != '2' and select_loop != '3' and select_loop != '4' and select_loop != '5' and select_loop != '6':
                select_loop = input("Invalid input, please try again, and select from 1 through 6. ")
            if select_loop == '1':
                continue
            elif select_loop == '2':
                savePassword()
            elif select_loop == '3':
                viewSavedPass()
            elif select_loop == '4':
                copyPass(generated)
            elif select_loop == '6':
                print('Exiting now')
                exit()
                break
            


    elif selection == '4':
            print('Exiting now.')
            exit()
            

    


if __name__=="__main__":
    main()
