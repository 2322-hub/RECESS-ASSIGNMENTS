import csv
import json
import logging

logging.basicConfig(
    filename="student_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CSV_FILE = "students.csv"
JSON_FILE = "students.json"


class StudentError(Exception):
    pass


def file_handling_demo():
    print("\n--- File Handling Demo ---")

    with open("demo.txt", "w") as f:
        f.write("Hello\nPython Programming\n")

    with open("demo.txt", "r") as f:
        print("Full content:")
        print(f.read())

    with open("demo.txt", "r") as f:
        print("Line by line:")
        for line in f:
            print(line.strip())

    with open("demo.txt", "a") as f:
        f.write("Appended line\n")

    print("Demo complete")


def add_student():
    try:
        reg = input("Enter Registration Number: ").strip()
        name = input("Enter Name: ").strip()
        age = int(input("Enter Age: "))
        course = input("Enter Course: ").strip()

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([reg, name, age, course])

        extra = {
            "RegistrationNo": reg,
            "Address": input("Enter Address: "),
            "Contact": input("Enter Contact: "),
            "Program": input("Enter Program: ")
        }

        try:
            with open(JSON_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(extra)

        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Student added")
        logging.info(f"Added student {reg}")

    except Exception as e:
        logging.error(str(e))
        print("Error adding student")


def view_students():
    try:
        with open(CSV_FILE, "r") as f:
            print("\nAll Students:")

            for line in f:
                print(line.strip())

        logging.info("Viewed students")

    except FileNotFoundError:
        print("No records found")


def search_student():
    try:
        reg = input("Enter Registration Number: ")
        found = False

        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == reg:
                    print("Found:", row)
                    found = True

        if not found:
            raise StudentError("Student not found")

    except StudentError as e:
        print(e)
        logging.warning(str(e))


def update_student():
    try:
        reg = input("Enter Registration Number: ")
        rows = []
        updated = False

        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == reg:
                    print("Enter new details:")
                    row[1] = input("New Name: ")
                    row[2] = input("New Age: ")
                    row[3] = input("New Course: ")
                    updated = True
                rows.append(row)

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        if not updated:
            raise StudentError("Student not found")

        print("Updated")
        logging.info(f"Updated {reg}")

    except StudentError as e:
        print(e)


def delete_student():
    try:
        reg = input("Enter Registration Number: ")
        rows = []
        deleted = False

        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != reg:
                    rows.append(row)
                else:
                    deleted = True

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        if not deleted:
            raise StudentError("Student not found")

        print("Deleted")
        logging.info(f"Deleted {reg}")

    except StudentError as e:
        print(e)


def menu():
    while True:
        print("\n===== STUDENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. File Handling Demo")
        print("7. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                file_handling_demo()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice")

        except Exception as e:
            logging.error(str(e))
        finally:
            print("Operation complete\n")


if __name__ == "__main__":
    menu()
