import argparse
import os
import csv
from pass_generator import password_gen

file_name = "Password manager.csv"

parser = argparse.ArgumentParser(description="Password manager. You can create a new password [new] or view a list of all created passwords [list]. For additional help, enter [new -h], [new --help] or [list -h], [list --help].")

subparser = parser.add_subparsers(dest= "command", help="subparser help")
parser_new = subparser.add_parser("new", help="create a new password: [new] [--title] [--login]")
parser_new.add_argument("--title", help="to create a title name of a password", action="store")
parser_new.add_argument("--login", help="to create a login name of a password", action="store")
parser_new.add_argument("-l", "--letters", help="include uppercase letters in the password (included by default)", default=True, action="store")
parser_new.add_argument("-s", "--symbols", help="include symbols in the password", default=False, action="store")
parser_new.add_argument("-n", "--numbers", help="include numbers in the password", default=False, action="store")
parser_new.add_argument("-d", "--duplicates", help="include duplicates in the password (duplicates included by default)", default=False, action="store")
parser_new.add_argument("-p", "--pass_length", help="set a password length (number)", default=8, type=int, action="store")

parser_list = subparser.add_parser("list", help="list created password(s): [list] or [list] [--title]")
parser_list.add_argument("--title", help="view the exact password by its title name", action="store")

args = parser.parse_args()


def main():
    if args.command == "list":
        if not args.title:
            show_pass_list()
        else:
            show_exact_pass()
    elif args.command == "new":
        # arg_checker(args.title, args.login)
        new_pass()
    else:
        print("Enter [-h] to see all the command options for the program")


# Functions for the 'list' option: show_pass_list(), show_exact_pass(), duplicate_login_checker_list()


def show_pass_list():
    try:
        csv_obj = open(file_name, "r")
        csv_list = csv_obj.readlines()
        titles_list = []
        for password in range(len(csv_list)):
            title_name = csv_list[password].split(",")[0]
            titles_list.append(title_name)
        print(f"Your current list of titles: {titles_list}")
    except FileNotFoundError:
        return print("Please be advised that no file is yet created. Create a new password [new] to view the existing titles.")


def show_exact_pass():
    try:
        csv_obj = open(file_name, "r")
        csv_list = csv_obj.readlines()
        user_pass_title = args.title
        message = "Sorry, mentioned title is not in the list. Please try again."

        for password in range(len(csv_list)):
            # title = csv_list[password].split(",")         # each set
            title_name = csv_list[password].split(",")[0]   # individual title name

            if title_name.lower().strip() == user_pass_title.lower().strip():
                message_function = duplicate_login_checker_list(user_pass_title, csv_list)
                message_return = f"""title: {message_function[0]}
login: {message_function[1]}
password: {message_function[2]}"""
                return print(message_return)
        return print(message)
    except FileNotFoundError:
        return print("Please be advised that no file is yet created. Create a new password [new] to view the existing titles.")


def duplicate_login_checker_list(user_title, csv_list):
    user_title_list = []
    counter = 0
    for password in range(len(csv_list)):
        title_name = csv_list[password].split(",")[0]   # individual title name
        if title_name.lower().strip() == user_title.lower().strip():
            counter += 1
    if counter == 1:
        for password in range(len(csv_list)):
            title = csv_list[password].split(",")
            if title[0].lower().strip() == user_title.lower().strip():
                return title
    elif counter > 1:
        print("There are several titles with mentioned title name.")

    for password in range(len(csv_list)):
        title = csv_list[password].split(",")
        if user_title.lower().strip() == title[0].lower().strip():
            user_title_list.append(title)

    for number in range(len(user_title_list)):
        print(f"{str(number + 1)}. {user_title_list[number][0]}")

    while True:
        user_number = input(f"Please specify the number of the title [1-{len(user_title_list)}]: ")
        if user_number.lower().strip() == "e":
            return exit()
        elif int(user_number) < 1 or int(user_number) > len(user_title_list):
            print(f"Please enter a number from 1 to {len(user_title_list)}, or press [e] to exit")
        else:
            user_pass = user_title_list[int(user_number) - 1]
            return user_pass


# Functions for the 'new' option: arg_checker(), decision_maker(), new_pass(), duplicate_titles_checker_new(), decision_maker_2()


def arg_checker(command_1, command_2):

    def decision_maker(user_decision):
        if user_decision.lower().strip() == "y" or user_decision.lower().strip() == "yes":
            return
        elif user_decision.lower().strip() == "n" or user_decision.lower().strip() == "no":
            return exit()

    if not command_1 or not command_2:
        decision = input("Please be advised that your password does not have 'title' and/or 'login'. Do you still want to proceed? [y/n]: ")
        decision_maker(decision)
        return 1


def new_pass():
    title = args.title
    login = args.login

    if arg_checker(args.title, args.login):
        empty_name = "Empty"
        if not title and not login:
            title = login = empty_name
        elif not title:
            title = empty_name
        elif not login:
            login = empty_name

    password = password_gen(letters=args.letters, symbols=args.symbols, numbers=args.numbers, duplicates=args.duplicates, pass_length=args.pass_length)

    if os.path.isfile(file_name):
        csv_obj = open(file_name, "a", newline="")
    else:
        csv_obj = open(file_name, "w", newline="")

    csv.writer(csv_obj).writerow([title, login, password])
    csv_obj.close()
    message = f"Great, you have just created a new password for {title}."
    return print(message)


def duplicate_titles_checker_new(title):

    def decision_maker_2(user_decision):
        if user_decision.lower().strip() == "y":
            return
        elif user_decision.lower().strip() == "n":
            return exit()

    csv_obj = open(file_name, "r")
    csv_list = csv_obj.readlines()
    for password in range(len(csv_list)):
        title_name = csv_list[password].split(",")[0]   # individual title name
        if title_name == title:
            decision = input(f"Title '{title}' is already in the list. Do you want to save both passwords [y], or exit [n]?: ")
            decision_maker_2(decision)
            return

main()
