from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super-secret-key-change-in-production"

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "customer": {"password": "customer123", "role": "Customer"},
    "cashier": {"password": "cashier123", "role": "Cashier"},
}


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        user = USERS.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], role=session["role"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        role = request.form.get("role", "").strip()

        if not username or not password or not role:
            return render_template("register.html", error="All fields are required.")
        if len(password) < 4:
            return render_template("register.html", error="Password must be at least 4 characters.")
        if password != confirm:
            return render_template("register.html", error="Passwords do not match.")
        if USERS.get(username):
            return render_template("register.html", error="Username already exists.")

        USERS[username] = {"password": password, "role": role}
        return render_template("register.html", success="Account created! You can now login.")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
