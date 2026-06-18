class ContactManager:
    def __init__(self):
        self.contacts = []

    def _is_valid_phone(self, phone):
        return all(c in "0123456789-" for c in phone)

    def _is_valid_email(self, email):
        return "@" in email and "." in email

    def add_contact(self, name, phone, email=""):
        if not self._is_valid_phone(phone):
            print("❌ Invalid phone number. Use digits and hyphens only.")
            return

        if email and not self._is_valid_email(email):
            print("❌ Invalid email format.")
            return

        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email
        })
        print("✅ Contact added successfully.")

    def view_contact(self, name):
        results = [c for c in self.contacts if c["name"].lower() == name.lower()]
        self._display(results)

    def update_contact(self, name, new_phone=None, new_email=None):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():

                if new_phone:
                    if not self._is_valid_phone(new_phone):
                        print("❌ Invalid phone number.")
                        return
                    contact["phone"] = new_phone

                if new_email:
                    if not self._is_valid_email(new_email):
                        print("❌ Invalid email.")
                        return
                    contact["email"] = new_email

                print("✅ Contact updated.")
                return

        print("❌ Contact not found.")

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                self.contacts.remove(contact)
                print("✅ Contact deleted.")
                return
        print("❌ Contact not found.")

    def list_all_contacts(self):
        self._display(self.contacts)

    def search_contacts(self, keyword):
        keyword = keyword.lower()

        results = [
            c for c in self.contacts
            if keyword in c["name"].lower()
            or keyword in c["phone"].lower()
            or keyword in c["email"].lower()
        ]

        self._display(results)

   
    def _display(self, contacts):
        if not contacts:
            print("📭 No contacts found.")
            return

        print("\n📇 Contacts:")
        print("-" * 40)
        for i, c in enumerate(contacts, 1):
            print(f"{i}. Name : {c['name']}")
            print(f"   Phone: {c['phone']}")
            print(f"   Email: {c['email']}")
            print("-" * 40)

def main():
    manager = ContactManager()

    while True:
        print("\n=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        try:
            choice = int(input("Choose an option (1-7): "))
        except ValueError:
            print("❌ Enter a valid number.")
            continue

        if choice == 1:
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            email = input("Enter email (optional): ")
            manager.add_contact(name, phone, email)

        elif choice == 2:
            name = input("Enter name to view: ")
            manager.view_contact(name)

        elif choice == 3:
            name = input("Enter name to update: ")
            phone = input("New phone (blank to skip): ")
            email = input("New email (blank to skip): ")

            manager.update_contact(
                name,
                new_phone=phone if phone else None,
                new_email=email if email else None
            )

        elif choice == 4:
            name = input("Enter name to delete: ")
            manager.delete_contact(name)

        elif choice == 5:
            keyword = input("Enter search keyword: ")
            manager.search_contacts(keyword)

        elif choice == 6:
            manager.list_all_contacts()

        elif choice == 7:
            print("👋 Exiting program.")
            break

        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()