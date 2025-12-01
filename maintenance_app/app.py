from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector # for connect to the mySQL DB
from werkzeug.security import check_password_hash # for hashing the password

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Connect to MySQL -> (XAMPP)
def get_db():
    return mysql.connector.connect(
        host="localhost", # simple 4 now.
        user="root",
        password="",
        database="maintenance_app",
    )

@app.route("/")
def home():
    return redirect(url_for("login"))

# for the login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear() # clear the session.
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
