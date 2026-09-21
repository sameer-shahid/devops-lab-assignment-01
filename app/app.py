import os
import re
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devops-lab-assignment-secret-key-fa23")

# In-memory storage for registered students
STUDENTS_DB = [
    {
        "fullName": "Muhammad Ali",
        "studentEmail": "ali@cuilahore.edu.pk",
        "rollNumber": "FA21-BSE-001",
        "age": 22,
        "department": "Software Engineering"
    },
    {
        "fullName": "Fatima Zahra",
        "studentEmail": "fatima@cuilahore.edu.pk",
        "rollNumber": "SP22-BCS-045",
        "age": 21,
        "department": "Computer Science"
    }
]

# Demo credentials
VALID_USERS = {
    "admin": "Admin@123",
    "student": "Student@123",
    "devops": "DevOps@2026"
}

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        # Validation rules
        if not username or not password:
            msg = "Username and password cannot be empty."
            if request.is_json:
                return jsonify({"success": False, "message": msg}), 400
            return render_template("login.html", error=msg)

        if username in VALID_USERS and VALID_USERS[username] == password:
            session["user"] = username
            if request.is_json:
                return jsonify({"success": True, "message": "Login successful", "redirect": "/dashboard"}), 200
            return redirect(url_for("dashboard"))
        else:
            msg = "Invalid username or password. Please try again."
            if request.is_json:
                return jsonify({"success": False, "message": msg}), 401
            return render_template("login.html", error=msg)

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"], students=STUDENTS_DB)

@app.route("/api/register", methods=["POST"])
def register_student():
    if "user" not in session:
        return jsonify({"success": False, "message": "Unauthorized. Please log in."}), 401

    data = request.get_json(silent=True) or request.form
    full_name = data.get("fullName", "").strip()
    student_email = data.get("studentEmail", "").strip()
    roll_number = data.get("rollNumber", "").strip()
    age_str = str(data.get("age", "")).strip()
    password = data.get("password", "").strip()
    department = data.get("department", "").strip()

    # Rule 1: Empty-field validation
    if not full_name or not student_email or not roll_number or not age_str or not password or not department:
        return jsonify({"success": False, "message": "All fields are required. Please complete all fields."}), 400

    # Rule 2: Invalid email validation
    if not re.match(EMAIL_REGEX, student_email):
        return jsonify({"success": False, "message": "Invalid email format. Please enter a valid email address."}), 400

    # Rule 3: Password length validation (minimum 8 characters)
    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters long."}), 400

    # Rule 4: Invalid numeric input validation (Age must be between 16 and 60)
    if not age_str.isdigit():
        return jsonify({"success": False, "message": "Age must be a valid numeric integer."}), 400
    
    age = int(age_str)
    if age < 16 or age > 60:
        return jsonify({"success": False, "message": "Age must be between 16 and 60."}), 400

    # Rule 5: Required dropdown selection validation
    valid_departments = ["Software Engineering", "Computer Science", "Artificial Intelligence", "Cyber Security"]
    if department not in valid_departments:
        return jsonify({"success": False, "message": "Please select a valid academic department from the dropdown."}), 400

    new_student = {
        "fullName": full_name,
        "studentEmail": student_email,
        "rollNumber": roll_number,
        "age": age,
        "department": department
    }
    STUDENTS_DB.append(new_student)

    return jsonify({
        "success": True,
        "message": f"Student '{full_name}' successfully registered!",
        "student": new_student,
        "total": len(STUDENTS_DB)
    }), 201

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify({"success": True, "students": STUDENTS_DB})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Listen on 0.0.0.0 so AWS EC2 public IP can access it
    app.run(host="0.0.0.0", port=port, debug=True)
