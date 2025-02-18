## Repository for Laboratory - Programming and Lecture Design Final Project

Final Project is a **Password Manager** that:

- Creates a password that is completely randomized

- Allows for user customization:
  - a. Uppercase letter inclusion (ABC...Z)
  - b. Lowercase letter inclusion (abc...z)
  - c. Number inclusion (123...0)
  - d. Punctuation/Special character inclusion (.,/ etc.)
  - e. Length choice

- Password strength checker:
  - Checks the generated password, or a user input password, based on:
    - length
    - character diversity
    - word appearances or lack thereof

- Saves passwords generated to an encrypted file using Fernet encryption (cryptography.fernet)
