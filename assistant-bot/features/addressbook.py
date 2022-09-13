from features.bot_feature import BotFeature
from addressbook_fields import Record

DATE_FORMAT = "%d.%m.%Y"


class AddressBook(BotFeature):
    """
    A feature that allows users to manage their contacts.
    """

    def __init__(self, save_file: str):
        super().__init__({
            "add": self.add_contact,
            "change": self.change_contact,
            "remove": self.remove_record,
            "show": self.show_all,
            "birthdays": self.check_birthdays,
            "search": self.search_record
        })

        self.save_file = save_file
        self.data = BotFeature.load_data(save_file) or {}

    def name(self):
        return "contacts"

    def add_contact(self):
        name = input("Enter the name: ").strip()
        if self.record_exists(name):
            return ValueError("This name is already in your phonebook. If you want to change the phone number, "
                              "type 'change'.")
        record = Record(name)
        self.add_record(record)

        phones = input("Enter the phone or phones: ").strip().split()
        if phones:
            for phone in phones:
                record.add_phone(phone)

        birthday = input("Enter the birthdate: ").strip()
        if birthday:
            record.add_birthday(birthday)

        email = input("Enter the email: ").strip()
        if email:
            record.add_email(email)

        address = input("Enter the address: ").strip()
        if address:
            record.add_address(address)

        return f"Contact {name} was created successfully!"

    def change_contact(self, *args: str):
        name = " ".join(args)
        if self.record_exists(name):
            contact_to_change = self.data[name]
            while True:
                to_change = input("What do you want to change? Type phone, email or address: ")
                if to_change.lower() not in ["phone", "email", "address"]:
                    print("Unknown command")
                    continue
                elif to_change.lower() == "phone":
                    old_phone = input("Enter a phone to change:")
                    new_phone = input("Enter a new phone: ")
                    contact_to_change.delete_phone(old_phone)
                    contact_to_change.add_phone(new_phone)
                    self.remove_contact(name)
                    self.add_record(contact_to_change)
                elif to_change.lower() == "email":
                    new_email = input("Enter a new email: ")
                    contact_to_change.add_email(new_email)
                elif to_change.lower() == "address":
                    new_address = input("Enter new address here: ")
                    contact_to_change.add_address(new_address)

                to_continue = input("Do you want to change something else in this contact? Enter y or n: ")
                if to_continue.lower() not in ["y", "n"]:
                    print("Enter y or n.")
                    continue
                elif to_continue.lower() == "y":
                    continue
                else:
                    return "The contact was changed successfully!"
        else:
            raise KeyError("Note with this title doesn't exist.")

    def check_birthdays(self, period: str) -> str:

        if not period.isdigit():
            raise ValueError("Enter a number of days.")

        result = ""
        for contact in self.data.values():
            if contact.birthday is None:
                continue
            else:
                days_to_contacts_bd = contact.count_days_to_birthday()
                if int(days_to_contacts_bd) <= int(period):
                    result += str(contact) + "\n"
        if result:
            return result
        else:
            return "No one has birthday in this period."
