"""Module providing a function """
import pickle
from collections import UserDict
from datetime import datetime
from class_file import AddressBook,Record

def decorator(func):
    """Decorator"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "Enter the correct command"
        except ValueError:
            return "Enter correct command"
        except IndexError:
            return "Enter the correct command, name and phone number"
        except NameError as e:
            return f"{e}"
        except FileNotFoundError:
            global book
            book = AddressBook()
            with open('Data.bin', 'wb') as file:
                pickle.dump(book, file)
                return "Create Data"
        except Exception as e:
            return f"{e}"
    return wrapper

@decorator
def start():
    """Load data"""
    with open('Data.bin', 'rb') as file:
        global book
        book = pickle.load(file)
    return "Bot start"

def save():
    """Save data"""
    global book
    with open('Data.bin', 'wb') as file:
        pickle.dump(book, file)

def command_hello():
    """Function Hello"""
    return "How can I help you?"

def command_add_record(name,phone):
    """Adding a contact to the Address Book"""
    new_record = Record(name)
    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added successfully"

def command_find_record(name):
    """Find a contact in the Address Book"""
    if book.find(name):
        return book.find(name)

def command_delete_record(name):
    """Deleting a contact in the Address Book"""
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"

def command_update_phone(name,phone):
    """Adding a phone number"""
    if book.find(name):
        new_phone = book.find(name)
        new_phone.add_phone(phone)
        return new_phone

def command_remove_phone(name, phone):
    """Deleting a phone number"""
    if book.find(name):
        record = book.find(name)
        record.remove_phone(phone)
        return record

def command_edit_phone(name,phone_one,phone_two):
    """Changing the phone number"""
    if book.find(name):
        record = book.find(name)
        record.edit_phone(phone_one,phone_two)
        return record

def command_show_all():
    """Function show all phone number"""
    for contact in book.values():
        print(contact)

def command_good_bye():
    """Function close bot"""
    global ACTIVE_BOT
    ACTIVE_BOT = False
    return "Good Bye!"

def command_find_all(value):
    """Keyword search function """
    return book.iterator(value)

def get_command(command):
    """Function command bot"""
    return command_list[command]

command_list = {
        "hello": command_hello,
        "add" : command_add_record,
        "find": command_find_record,
        "delete": command_delete_record,

        "update" : command_update_phone,
        "remove": command_remove_phone,
        "edit": command_edit_phone,

        "show all": command_show_all,
        "good bye": command_good_bye,
        "close": command_good_bye,
        "exit": command_good_bye,
        "all": command_find_all,
    }

ACTIVE_BOT = False
book = None

@decorator
def command_parser(user_input):
    """Сommand parser"""
    if user_input in ["show all", "hello", "good bye", "close", "exit"]:
        return get_command(user_input)()
    else:
        user_input = user_input.split()
        if user_input[0] in ["phone", "delete", "find", "all"]:
            return get_command(user_input[0])(user_input[1])
        elif user_input[0] in ["remove", "update", "add"]:
            return get_command(user_input[0])(user_input[1],(user_input[2]))
        elif user_input[0] in ["edit"]:
            return get_command(user_input[0])(user_input[1],(user_input[2]),(user_input[3]))
        else:
            raise ValueError()

def main():
    """Bot"""
    print(start())
    global ACTIVE_BOT
    ACTIVE_BOT = True
    while ACTIVE_BOT:
        user_input = input("Enter the command: ").lower().strip()
        print(command_parser(user_input))
        save()

main()
#The file ends
