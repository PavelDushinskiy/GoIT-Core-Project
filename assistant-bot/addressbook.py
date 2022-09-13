from typing import List, Any
from collections import UserDict
from datetime import datetime, timedelta
from features.bot_feature import BotFeature
import re
import pickle


NAME_REGEX = re.compile(r'^[\wа-яА-ЯєЄїЇ,. ]{2,30}$')
PHONE_REGEX = re.compile(r'\+\d{3}\(\d{2}\)\d{3}-\d{1,2}-\d{2,3}')
EMAIL_REGEX = re.compile(r'[a-zA-Z]\w+@[a-zA-Z]+\.[a-z]{2,}')
BIRTHDAY_REGEX = re.compile(r'(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])\.(?:0?[1-9]|1[0-2])\.(?:19[0-9][0-9]|20[01][0-9])(?!\d)')
DATE_FORMAT = "%d.%m.%Y"

def _now():
    return datetime.today()


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, name: str):
        if not re.match(NAME_REGEX, name):
            raise ValueError('Name can contain letters, numbers and must be between 2 and 30 characters')
        self._value = name


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = f"Redefined: {value}"


class Email(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = f"Redefined: {value}"


class Birthday(Field):
    @property
    def value(self) -> datetime.date:
        return self._value

    @value.setter
    def value(self, value):
        self._value = datetime.strptime(value, DATE_FORMAT)

    def __repr__(self):
        return datetime.strftime(self._value, DATE_FORMAT)


class Address(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = f"Redefined: {value}"


class Record:
    def __init__(self, name: str,
                 phone: Phone,
                 email: Email | None,
                 birthday: Birthday | None,
                 address: Address | None):
        self.name = Name(name)
        self.phones: list[Phone] = [phone] if phone is not None else []
        self.birthday = Birthday(birthday)
        self.address = Address(address)
        self.email = Email(email)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            self.phones.remove(old_phone)
            self.phones.append(new_phone)
        except ValueError:
            return f"{old_phone} does not exist"

    def find_phone(self, to_find: str):
        for phone in self.phones:
            if phone.value == to_find:
                return phone
        return None

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"{phone} does not exist"

    def add_email(self, email: Email):
        self.email = email

    def change_email(self, new_email: Email):
        self.email = new_email

    def find_email(self, to_find: str):
        for phone in self.phones:
            if phone.value == to_find:
                return phone
        return None

    def delete_email(self, email: Email):
        try:
            del self.email
        except ValueError:
            return f"{self.email} does not exist"

    def match_pattern(self, pattern):
        if re.search(pattern, self.name.value):
            return True
        for phone in self.phones:
            if re.search(pattern, phone.value):
                return True
        return False

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def add_address(self, address: Address):
        self.address = address

    def change_address(self, new_address: Address):
        self.address = new_address


class AddressBook(BotFeature, UserDict):
    """
    A feature that allows users to manage their contacts.
    """
    __book_name = "address_book.bin"

    def __init__(self, file_path: str):
        super().__init__({
            "add": self.add,
            "change": self.change,
            "remove": self.remove,
            "show": self.show,
            "birthdays": self.check_birthdays,
            "search": self.search
        })

        # TODO: Implement deserialization

    def __enter__(self):
            self.__restore()
            # print(f"Restoring the address book from {file_path}")
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
            self.__save()

    def __save(self):
        try:
            with open(self.__book_name, "wb+") as file:
                pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)
                print("Book saved!")
        except Exception:
            print("Some problems!")
            raise

    def __restore(self):
        try:
            with open(self.__book_name, "rb+") as file:
                book = pickle.load(file)
                self.data.update(book)
        except Exception:
            print("Book is not restored!")
            raise

    def name(self):
        return "contacts"

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def add(self, *args: List[str]) -> str:
        field, name = args[0], args[1]
        if len(*args) == 2:
            if name not in self.data.keys():
                self.add_record(Record(name))
                return f"New contact added"
            else:
                raise ValueError("This name is already in your addressbook.")
        else:
            match field:
                case "phone":
                    name, phone = args[1], args[2]
                    if not re.match(PHONE_REGEX, phone[0]):
                        raise ValueError('Number must be in international format, for example +380(67)012-34-56')
                    else:
                        record = Record(name)
                        record.add_phone(Phone(phone))
                        return f"Phone for {name} added"
                case "email":
                    name, email = args[1], args[2]
                    if not re.match(EMAIL_REGEX, email[0]):
                        raise ValueError('It does not look like an email address')
                    else:
                        record = Record(name)
                        record.add_email(Email(email))
                        return f"Email for {name} added"
                case "birthday":
                    name, birthday = args[1], args[2]
                    if not re.match(BIRTHDAY_REGEX, birthday[0]):
                        raise ValueError('Birthday must be in format DD.MM.YYYY')
                    elif datetime.strptime(birthday[0], DATE_FORMAT).date() > _now():
                        raise ValueError('Birthday can not be in the future')
                    else:
                        record = Record(name)
                        record.add_birthday(Birthday(birthday))
                        return f"Birthday for {name} added"
                case "address":
                    name, address = args[1], args[2]
                    record = Record(name)
                    record.add_address(Address(address))
                    return f"Address for {name} added"

    def change(self, *args: List[str]) -> str:
        field, name, value = args[0], args[1], args[2]
        match field:
            case "phone":
                if not re.match(PHONE_REGEX, value[0]):
                    raise ValueError('Number must be in international format, for example +380(67)012-34-56')
                else:
                    new_phone = args[3]
                    record = Record(name)
                    record.change_phone(Phone(value), Phone(new_phone))
                    return f"Phone for {name} changed"
            case "email":
                if not re.match(EMAIL_REGEX, value[0]):
                    raise ValueError('It does not look like an email address')
                else:
                    record = Record(name)
                    record.change_email(Email(value))
                    return f"Email for {name} changed"
            case "address":
                record = Record(name)
                record.change_address(Address(value))
                return f"Address for {name} changed"

    def remove(self, *args: List[str]) -> str:
        name = args[0]
        if name is not self.data.keys():
            raise ValueError("There is no such contact. Try again...")
        else:
            self.data.pop(name)
            return f"Contact {name} removed"

    def show(self, *args: List[str]) -> str:
        print(args)
        raise NotImplementedError("This method is not implemented yet")

    def check_birthdays(self, num_of_days: int) -> str | list[tuple[Any, Any]]:
        list_birthdays = []
        start_date: datetime.date = _now().date()
        end_date: datetime.date = start_date + timedelta(days=num_of_days)
        for record in self.data.values():
            if start_date <= record.birthday <= end_date:
                list_birthdays.append((record.name, record.birthday))
        if len(list_birthdays):
            return f"Unfortunately, there is no birthday in the next {num_of_days} days."
        else:
            return list_birthdays

    def search(self, *args: List[str]) -> str:
        needle = args[0]
        result = list(filter(lambda found_value: needle[0] in str(found_value), self.data.values()))
        if result:
            return "\n".join([str(r) for r in result])
        else:
            return "Unfortunately, I couldn't find any text that matched your query."




