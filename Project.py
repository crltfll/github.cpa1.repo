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
"""


from random import *
import string

def getStrongPass(length, upper_use = True, num_use = True, spec_use = True):

    letters_lower = string.ascii_letters_lowercase
    letters_upper = string.ascii_letters_uppercase
    numbers = string.digits
    specials = string.punctuation
    
    pool = letters_lower
    if lower_use == True:
        pool += letters_lower
    if upper_use == True:
        pool += letters_upper
    if spec_use == True:
        pool += specials
    if num_use == True:
        pool += numbers

    
    password = ''.join(choice(pool) for char in range(length))

    return password



print("By default, your password will include lowercase letters.")
upper_check = str(input("Would you like to have uppercase letters in your password?\nType Y for Yes, N for No. ")).upper()
while upper_check != 'Y' and num_check != 'N':
    upper_check = str(input("Your input was not Y or N. Please try again.\nWould you like to have numbers in your password?\nType Y for Yes, N for No. "))
if upper_check == 'Y':
    upper_check = True
elif upper_check == 'N':
    upper_check = False

num_check = str(input("Would you like to have numbers in your password?\nType Y for Yes, N for No. ")).upper()
while num_check != 'Y' and num_check != 'N':
    num_check = str(input("Your input was not Y or N. Please try again.\nWould you like to have numbers in your password?\nType Y for Yes, N for No. "))
if num_check == 'Y':
    num_use1 = True
elif num_check == 'N':
    num_use1 = False

spec_check = str(input("Would you like to have special characters in your password?\nType Y for Yes, N for No. ")).upper()
while spec_check != 'Y' and spec_check != 'N':
    spec_check = str(input("Your input was not Y or N. Please try again.\nWould you like to have special characters in your password?\nType Y for Yes, N for No. "))
if spec_check == 'Y':
    spec_use1 = True
elif spec_check == 'N':
    spec_use1 = False

length_inp = int(input("Please type in your desired length of password.\nTip: The longer, the better! "))
while length_inp <= 0:
    length_inp = int(input("Please type a positive number. "))

password = getStrongPass(length_inp, upper_check, num_check, spec_check)
print("Your password is: ", password)
