from re import match
import datetime


class Field:
    """
    The base class for the fields of an addressbook.
    """

    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __hash__(self) -> int:
        return self.value.__hash__()

    def __eq__(self, o: object) -> bool:
        return self.value == o

    def __contains__(self, needle):
        return True if needle in self.value else False

    @staticmethod
    def verify_value(value):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.verify_value(value)
        self._value = value


class Name(Field):
    """
    A name of a person in an addressbook.
    """

    @classmethod
    def is_valid(cls, value: str):
        return match(r"\b[A-Za-z-]+", value)

    def verify_value(self, value: str):
        """
        Verifies that name consists only of alphabetical characters. Raises exception if the name contains something
        besides latin letters.
        :param value: a name to check
        """
        if len(value) < 2 or len(value) > 30:
            raise ValueError("Name must be between 2 and 30 characters.")


class Phone(Field):
    """
    A phone number of a person in an address book.
    """

    @classmethod
    def is_valid(cls, value: str):
        return match(r"(\+?\d{12}|\d{10})", value)

    def verify_value(self, value: str):
        """
        Checks if the phone is given in a valid format. Raises exception if the phone doesn't match one of the formats.
        :param value: phone number
        """

        if not Phone.is_valid(value):
            raise ValueError("Invalid phone format. Try +123456789012 or 1234567890.")


class Birthday(Field):
    """
    Person's birthday date.
    """

    def verify_value(self, value: datetime.date):
        """
        Checks if the birthdate is not in the future. Raises exception if the date is in the future.
        :param value: datetime object
        """

        if value > datetime.datetime.now().date():
            raise ValueError("Birthday can't be in future.")


class Email(Field):
    """
    Person's email.
    """

    @classmethod
    def is_valid(cls, value: str):
        return match(r"[a-zA-Z][a-zA-Z_.0-9]+@[a-zA-Z_]+?\.[a-zA-Z]{2,}", value)


class Record:
    """
    A record about a person in an address book. Name field is compulsory, while phones and birthday fields are optional
    and can be omitted.
    """

    def __init__(self, name: str):
        if not name:
            raise ValueError("The record must have a name.")
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone: str) -> None:
        """
        Adds a phone to the record.
        :param phone: a phone number
        """
        if Phone.is_valid(phone):
            phone_object = Phone(phone)
            self.phones.append(phone_object)
        else:
            raise ValueError(f"Phone must be in format +380XXXXXXXXX/380XXXXXXXXX/0XXXXXXXXX")

    def delete_phone(self, phone: str) -> None:
        """
        Deletes a phone from the record. Raises exception if there is no such phone in the record.
        :param phone: a phone number to delete
        """

        phone = self.find_phone(phone)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError("The given phone is not in a list.")

    def find_phone(self, phone: str) -> Phone:
        """
        Finds and returns a phone from the phone list.
        :param phone: phone to search
        :return: an entry in a phone list corresponding to this phone
        """

        for phone_object in self.phones:
            if phone_object.value == phone:
                return phone_object

    def count_days_to_birthday(self) -> str:
        """
        Counts the days left to the birthdate of the given person.
        :return: a message that contains a number of days left or a reminder that a person has their birthday today
        """

        today = datetime.datetime.now().date()
        this_years_birthday = self.birthday.value.replace(year=today.year)

        if today < this_years_birthday:
            difference = this_years_birthday - today
            return difference.days
        if today == this_years_birthday:
            return "0"
        else:
            next_years_birthday = this_years_birthday.replace(year=this_years_birthday.year + 1)
            difference = next_years_birthday - today
            return difference.days

    def add_birthday(self, birthday: str):
        """
        Adds a birthdate to the record.
        :param birthday: datetime object
        """

        self.birthday = Birthday(birthday)

    def add_email(self, email: str):
        if Email.is_valid(email):
            email_object = Email(email)
            self.email = email_object
        else:
            raise ValueError("Your email seems to be invalid.")

    def add_address(self, *args):
        self.address = " ".join(args)

    def __str__(self):
        phones = ", ".join(map(lambda phone: str(phone), self.phones))
        if self.birthday:
            return f"Name: {self.name}, phones: {phones}, birthday: {self.birthday}"
        else:
            return f"Name: {self.name}, phones: {phones}"
