import sys
import random
import string

def read_generated_passwords():
    try:
        with open("generated_passwords.txt", "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

generated_passwords = read_generated_passwords()

def update_characters_left(number_of_characters, characters_left):
    if number_of_characters < 0 or number_of_characters > characters_left:
        print("Number of characters outside the range 0,", characters_left)
        return False
    else:
        characters_left -= number_of_characters
        print("Characters remaining:", characters_left)
        return True

def get_user_input(prompt, min_value=None, max_value=None, non_negative=False):
    while True:
        try:
            user_input = int(input(prompt))
            if (min_value is None or user_input >= min_value) and (max_value is None or user_input <= max_value):
                if not non_negative or user_input >= 0:
                    return user_input
                else:
                    print("Enter a number greater than or equal to 0.")
            else:
                print(f"Enter a number from the range {min_value}-{max_value}")
        except ValueError:
            print("Error! Enter the correct number.")

def generate_password(password_length, lowercase_letters, uppercase_letters, special_characters, digits):
    password = []

    for _ in range(password_length):
        if lowercase_letters > 0:
            password.append(random.choice(string.ascii_lowercase))
            lowercase_letters -= 1
        elif uppercase_letters > 0:
            password.append(random.choice(string.ascii_uppercase))
            uppercase_letters -= 1
        elif special_characters > 0:
            password.append(random.choice(string.punctuation))
            special_characters -= 1
        elif digits > 0:
            password.append(random.choice(string.digits))
            digits -= 1

    random.shuffle(password)
    generated_password = "".join(password)
    generated_passwords.append(generated_password)

    with open("generated_passwords.txt", "a") as file:
        file.write(generated_password + "\n")

def display_generated_password():
    if generated_passwords:
        for idx, password in enumerate(generated_passwords, start=1):
            print(f"{idx}. The generated password: {password}")
    else:
        print("No password has yet been generated.")

def main_menu():
    print("Menu:")
    print("1. Generate new password")
    print("2. View generated passwords")
    print("3. Exit the programme")

while True:
    main_menu()
    choice = get_user_input("Select an option: ")

    if choice == 1:
        password_length = get_user_input("How long should the new password be? ", min_value=5)
        characters_left = password_length

        lowercase_letters = get_user_input("How many lowercase letters should the password be? ", max_value=password_length, non_negative=True)
        characters_left -= lowercase_letters
        uppercase_letters = get_user_input("How many capital letters should the password have? ", max_value=password_length - lowercase_letters, non_negative=True)
        characters_left -= uppercase_letters
        special_characters = get_user_input("How many special characters should the password have? ", max_value=password_length - lowercase_letters - uppercase_letters, non_negative=True)
        characters_left -= special_characters
        digits = get_user_input("How many digits should the password have? ", max_value=password_length - lowercase_letters - uppercase_letters - special_characters, non_negative=True)
        characters_left -= digits

        if characters_left > 0:
            print("Not all characters have been used. The password will be completed in lower case.")
            lowercase_letters += characters_left

        generate_password(password_length, lowercase_letters, uppercase_letters, special_characters, digits)
        print("A new password has been generated.")
    elif choice == 2:
        display_generated_password()
    elif choice == 3:
        print("Thank you for using the programme. Goodbye!")
        sys.exit()
    else:
        print("Incorrect selection. Try again.")
