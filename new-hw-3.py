from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate_format(self):
        return len(str(self.value)) == 10 and str(self.value).isdigit()

class Birthday(Field):
    def validate_format(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if isinstance(phone, Phone) and phone.validate_format():
            self.phones.append(phone)
        else:
            raise ValueError("Invalid phone number format.")

    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday) and birthday.validate_format():
            self.birthday = birthday
        else:
            raise ValueError("Invalid birthday format.")

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone number not found in the record.")

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        else:
            raise ValueError("Phone number not found in the record.")

    def find_phone(self, phone):
        if phone in self.phones:
            return str(phone)
        else:
            raise ValueError("Phone number not found in the record.")

    def __str__(self):
        phone_list = '; '.join(str(p) for p in self.phones)
        birthday_info = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_list}{birthday_info}"

class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value.lower()] = record
        else:
            raise ValueError("Invalid record format.")

    def delete(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            del self.data[name_lower]
        else:
            raise ValueError("Record not found in the address book.")

    def find(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            return self.data[name_lower]
        else:
            raise ValueError("Record not found in the address book.")

    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                if datetime.strptime(record.birthday.value, "%d.%m.%Y").date() <= next_week.date():
                    birthdays.append(str(record))
        return birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input or contact not found."
        except IndexError:
            return "Enter valid input."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"An error occurred: {e}"

    return inner

@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    record = Record(name)
    record.add_phone(Phone(phone))
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    book.find(name).edit_phone(Phone(phone), Phone(args[1]))
    return "Contact updated."

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    return book.find(name)

@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise IndexError
    name, birthday = args
    record = book.find(name)
    record.add_birthday(Birthday(birthday))
    return "Birthday added to the contact."

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    return book.find(name).birthday if book.find(name).birthday else "Birthday not found."

def birthdays(book):
    upcoming_birthdays = book.get_birthdays_per_week()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    return "\n".join(upcoming_birthdays)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    main()
