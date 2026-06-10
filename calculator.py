def get_positive_float(prompt):
	while True:
		value = input(prompt).strip()
		try:
			number = float(value)
			if number <= 0:
				print("Please enter a number greater than 0.")
				continue
			return number
		except ValueError:
			print("Please enter a valid number.")


def get_positive_int(prompt):
	while True:
		value = input(prompt).strip()
		try:
			number = int(value)
			if number <= 0:
				print("Please enter a whole number greater than 0.")
				continue
			return number
		except ValueError:
			print("Please enter a valid whole number.")


def get_tip_percentage():
	print("\nChoose a tip percentage:")
	print("1. 10%")
	print("2. 15%")
	print("3. 20%")
	print("4. Custom")

	while True:
		choice = input("Enter your choice (1-4): ").strip()
		if choice == "1":
			return 10
		if choice == "2":
			return 15
		if choice == "3":
			return 20
		if choice == "4":
			custom_tip = get_positive_float("Enter custom tip percentage: ")
			return custom_tip
		print("Please choose 1, 2, 3, or 4.")


def main():
	print("Bill Split Calculator")
	print("-" * 24)

	bill_amount = get_positive_float("Enter the total bill amount: $")
	people = get_positive_int("Enter the number of people: ")
	tip_percentage = get_tip_percentage()

	tip_amount = bill_amount * (tip_percentage / 100)
	total_bill = bill_amount + tip_amount
	amount_per_person = total_bill / people

	print("\nReceipt")
	print("-" * 24)
	print(f"Bill amount:      ${bill_amount:.2f}")
	print(f"Tip percentage:    {tip_percentage:.2f}%")
	print(f"Tip amount:        ${tip_amount:.2f}")
	print(f"Total bill:        ${total_bill:.2f}")
	print(f"Number of people:  {people}")
	print(f"Each person's share: ${amount_per_person:.2f}")


if __name__ == "__main__":
	main()
