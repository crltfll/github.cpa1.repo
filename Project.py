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
(05/03/25)  - Added a saved password function to save the password data within a seperate file (Requires os for this action)- W.I.P.
(05/03/25)  - Added a password feature to protect the user's saved passwords - W.I.P.
"""

from random import *
import string
import pyperclip
import os

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
    # Required here: something that rerolls the password variable if a selected customization does not make it to the string
    return password

def savePassword(password):
    file_path = 'Password list.txt'

    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            file.write("\n" + password)
        print("Password has been saved")
        
    else:
        with open('Password list.txt', 'x') as file:
            file.write(password)
    
    input("Do you wish to continue?")
    main()
    

def viewSavedPass():
    masterpassword = "password123" #prototype password
    while True:
        login = input("Please input master password:")
        if login == masterpassword:
            print("""Here are your saved passwords:
            1) AWESOMEPASSWORD85
            2) KASFHKSADHFD%^%^%8
            3) =) """) # Prototype saved password
            input("Press Enter to continue...")
            returnback = input("Would you like to return? \nType Y for Yes, N for No. ").upper()
            main()
            # match returnback:
            #     case 'Y':
            #         main()
            #     case 'N':
            #         print("We will leave you be")
            #     case _:
            #         pass
        else:
            print("Incorrect password! Please try again...")
            continue


def copyPass(stringinp):
    try:
        pyperclip.copy(stringinp)
        print("Password saved to clipboard!")
    except ImportError:
        print("The module pyperclip needs to be installed to be used here. \nPlease install pyperclip using this command:")
        print("pip install pyperclip")
        return None

def testStrength(stringinp):
    passwordStrength = ["Your password is too weak. Consider making it longer!", "Your password is weak. Consider adding other character types!", "Your password is kind of strong. Make it stronger with other characters!", "Your password is very strong, well done!", "Your password is strong enough!"]
    upcheck = digcheck = specheck = False
    specs = string.punctuation
    if len(stringinp) <= 8:
        return print(passwordStrength[0])
    
    for char in stringinp:
        if char.isupper():
            upcheck = True
        elif char.isdigit():
            digcheck = True
        elif char in specs:
            specheck = True
    if not (upcheck or digcheck or specheck):
        return print(passwordStrength[1])
    if (digcheck or upcheck):
        return print(passwordStrength[2])
    if (digcheck and upcheck and specheck):
        if len(stringinp) >= 15:
            return print(passwordStrength[3])
        return print(passwordStrength[4])
        
        
    


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
    while selection not in {'1', '2', '3', '4'}:
        selection = input("Invalid input, please try again, and select from 1 through 4. ")

    if selection == '1':
        generated = customizePass()
        while True:
            print(main_menu)
            select_loop = input("Please select your next action choice. ").strip()
            while select_loop not in {'1', '2', '3', '4', '5', '6'}:
                select_loop = input("Invalid input, please try again, and select from 1 through 6. ")
            if select_loop == '1':
                continue
            elif select_loop == '2':
                savePassword(generated)
            elif select_loop == '3':
                viewSavedPass()
            elif select_loop == '4':
                copyPass(generated)
            elif select_loop == '5':
                testStrength(generated)
            elif select_loop == '6':
                print('Exiting now... Thank you for using Password Generator!')
                exit()

    elif selection == '2':
            viewSavedPass()            
    elif selection == '3':
            testStrength(generated)
    elif selection == '4':
            print('Exiting now... Thank you for using Password Generator!')
            exit()

    # print(title_ascii)
    # selection = input("Please select from the main menu numbers. ")
    
    # match selection:
    #     case '1':
    #         generated = customizePass()
    #         while True:
    #             print(main_menu)
    #             select_loop = input("Please select your next action choice. ").strip()
    #             match select_loop:
    #                 case '1':
    #                     continue
    #                 case '2':
    #                     savePassword()
    #                 case '3':
    #                     viewSavedPass()
    #                 case '4':
    #                     copyPass(generated)
    #                 case '5':
    #                     testStrength(generated)
    #                 case '6':
    #                     print('Exiting now... Thank you for using Password Generator!')
    #                     exit()
    #                     break
    #                 case _:
    #                     select_loop = input("Invalid input, please try again, and select from 1 through 6. ")
                
    #     case '2':
    #         viewSavedPass()
    #     case '3':
    #         pass
    #     case '4':
    #         print('Exiting now... Thank you for using Password Generator!')
    #         exit()
    #     case _:
    #         selection = input("Invalid input, please try again, and select from 1 through 4. ")
    #         main()



if __name__=="__main__":
    main()
