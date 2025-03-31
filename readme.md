## Repository for Laboratory - Programming and Lecture Design Final Project

Final Project is a **Password Manager** that:

- Creates a password that is completely randomized, without any possible words thrown in even in coincidence

- Allows for user customization (default is lowercase):
  - a. Uppercase letter inclusion (ABC...Z)
  - b. Number inclusion (123...0)
  - c. Punctuation/Special character inclusion (.,/ etc.)
  - d. Length choice


- Password strength checker:
  - Checks the generated password, or a user input password, based on:
    - length
    - character diversity

- Saves passwords generated to an encrypted file using Fernet encryption (cryptography.fernet)
