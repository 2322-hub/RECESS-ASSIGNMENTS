import tkinter as tk
from tkinter import messagebox


def add(num1, num2):
	return num1 + num2


def subtract(num1, num2):
	return num1 - num2


def multiply(num1, num2):
	return num1 * num2


def divide(num1, num2):
	if num2 == 0:
		raise ZeroDivisionError("Cannot divide by zero.")
	return num1 / num2


def calculate():
	try:
		num1 = float(entry_num1.get())
		num2 = float(entry_num2.get())
		operation = operation_var.get()

		if operation == "Add":
			result = add(num1, num2)
		elif operation == "Subtract":
			result = subtract(num1, num2)
		elif operation == "Multiply":
			result = multiply(num1, num2)
		elif operation == "Divide":
			result = divide(num1, num2)
		else:
			messagebox.showerror("Error", "Please choose an operation.")
			return

		result_var.set(f"Result: {result}")
	except ValueError:
		messagebox.showerror("Input Error", "Please enter valid numbers.")
	except ZeroDivisionError as error:
		messagebox.showerror("Math Error", str(error))


root = tk.Tk()
root.title("Menu-Driven Calculator")
root.geometry("360x260")
root.resizable(False, False)


title_label = tk.Label(root, text="Menu-Driven GUI Calculator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)


frame = tk.Frame(root)
frame.pack(pady=5)


tk.Label(frame, text="Number 1:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_num1 = tk.Entry(frame, width=20)
entry_num1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Number 2:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_num2 = tk.Entry(frame, width=20)
entry_num2.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Operation:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
operation_var = tk.StringVar(value="Add")
operation_menu = tk.OptionMenu(frame, operation_var, "Add", "Subtract", "Multiply", "Divide")
operation_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")


calculate_button = tk.Button(root, text="Calculate", command=calculate, width=15)
calculate_button.pack(pady=10)


result_var = tk.StringVar(value="Result: ")
result_label = tk.Label(root, textvariable=result_var, font=("Arial", 12))
result_label.pack(pady=10)


root.mainloop()
