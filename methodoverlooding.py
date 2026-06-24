# Pa
class Transaction:
    def process(self, amount):
        print("Processing transaction of", amount)


class Deposit(Transaction):
    def process(self, amount):
        print("Deposited:", amount)

    def details(self, amount, account="Main Account"):
        print(f"Deposit {amount} into {account}")


class Withdrawal(Transaction):
    def process(self, amount):
        print("Withdrawn:", amount)

    def details(self, amount, method="ATM"):
        print(f"Withdraw {amount} using {method}")


class Transfer(Transaction):
    def process(self, amount):
        print("Transferred:", amount)

    def details(self, amount, *accounts):
        if len(accounts) == 2:
            print(f"Transfer {amount} from {accounts[0]} to {accounts[1]}")
        else:
            print(f"Transfer {amount}")


d = Deposit()
d.process(5000)
d.details(5000)
d.details(5000, "Savings")

print("-----")

w = Withdrawal()
w.process(2000)
w.details(2000)
w.details(2000, "Bank Teller")

print("-----")

t = Transfer()
t.process(3000)
t.details(3000)
t.details(3000, "Account A", "Account B")
