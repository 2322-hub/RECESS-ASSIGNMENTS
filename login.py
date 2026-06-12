def authenticate(username, password):
	users = {
		"admin": {"password": "admin123", "role": "Admin"},
		"customer": {"password": "customer123", "role": "Customer"},
		"cashier": {"password": "cashier123", "role": "Cashier"},
	}

	user = users.get(username.strip().lower())
	if user is None:
		return None
	if password != user["password"]:
		return None
	return user["role"]


def show_access(role):
	print()
	print(f"Login successful. Role: {role}")

	if role == "Admin":
		print("Access: Manage products, users, reports, and all system features.")
	elif role == "Customer":
		print("Access: Browse products, add items to cart, and place orders.")
	elif role == "Cashier":
		print("Access: Process payments, handle receipts, and confirm transactions.")


def get_discount_rate(subtotal):
	if subtotal >= 500:
		return 0.20
	if subtotal >= 200:
		return 0.10
	if subtotal >= 100:
		return 0.05
	return 0.0


def get_coupon_discount(coupon_code, subtotal):
	coupon_code = coupon_code.strip().upper()

	if coupon_code == "SAVE10":
		return subtotal * 0.10
	if coupon_code == "SAVE20" and subtotal >= 250:
		return subtotal * 0.20
	if coupon_code == "VIP25" and subtotal >= 500:
		return subtotal * 0.25
	return 0.0


def get_tax_rate(location):
	location = location.strip().lower()

	if location == "local":
		return 0.05
	if location == "state":
		return 0.08
	if location == "international":
		return 0.15
	return 0.10


def run_calculator():
	print()
	print("E-Commerce Price Calculator")
	print("-" * 29)

	try:
		subtotal = float(input("Enter subtotal: "))
	except ValueError:
		print("Invalid subtotal. Please enter a number.")
		return

	if subtotal < 0:
		print("Subtotal cannot be negative.")
		return

	coupon_code = input("Enter coupon code (or press Enter to skip): ")
	location = input("Enter location (local, state, international): ")

	discount_rate = get_discount_rate(subtotal)
	base_discount = subtotal * discount_rate
	coupon_discount = get_coupon_discount(coupon_code, subtotal - base_discount)
	tax_rate = get_tax_rate(location)

	discounted_subtotal = subtotal - base_discount - coupon_discount
	tax_amount = discounted_subtotal * tax_rate
	total_price = discounted_subtotal + tax_amount

	print()
	print(f"Subtotal:       ${subtotal:.2f}")
	print(f"Base discount:   ${base_discount:.2f}")
	print(f"Coupon discount: ${coupon_discount:.2f}")
	print(f"Tax rate:        {tax_rate:.0%}")
	print(f"Tax amount:      ${tax_amount:.2f}")
	print(f"Final total:     ${total_price:.2f}")


def main():
	print("E-Commerce System")
	print("-" * 18)

	print("1. Login")
	print("2. Price Calculator")

	choice = input("Choose an option: ").strip()

	if choice == "1":
		username = input("Enter username: ")
		password = input("Enter password: ")

		role = authenticate(username, password)
		if role is None:
			print("Invalid username or password.")
			return

		show_access(role)
	elif choice == "2":
		run_calculator()
	else:
		print("Invalid choice.")


if __name__ == "__main__":
	main()