# DevOps Lab Assignment 1: Cloud-Based Web Test Automation

**Course:** DevOps for Cloud Computing (CSC418)  
**Institution:** COMSATS University Islamabad, Lahore Campus  
**Student Registration:** SP23-BSE-128  

---

## 🌟 Project Overview

This project implements:
1. **Part B: Cloud Web Application** — A modern, cloud-ready Student Portal built with Python Flask featuring responsive dark mode, glassmorphism UI, authentication, student management, and real-time form validations.
2. **Part C: Selenium Automation Framework** — A modular test automation framework designed using the **Page Object Model (POM)** and **Pytest**, including automated driver management, logging, screenshot capture, CSV data-driven testing, and HTML test report generation.

---

## 📂 Project Structure

```text
sp23-bse-128(lab assignment)/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # Modern glassmorphism UI styling
│   │   └── js/
│   │       └── script.js            # Dynamic validations & AJAX table updates
│   ├── templates/
│   │   ├── login.html               # Authentication page
│   │   └── dashboard.html           # Student registration dashboard & table
│   └── app.py                       # Flask server & REST API
├── selenium-project/
│   ├── pages/
│   │   ├── base_page.py             # Reusable explicit waits & interaction helpers
│   │   ├── login_page.py            # Page Object for Login portal
│   │   └── registration_page.py     # Page Object for Registration dashboard
│   ├── tests/
│   │   ├── conftest.py              # Pytest fixtures, driver management, report hooks
│   │   ├── test_login.py            # Test cases for login authentication
│   │   └── test_registration.py     # Test cases for mandatory validations & form flows
│   ├── test_data/
│   │   └── users.csv                # Dataset for data-driven testing
│   ├── screenshots/                 # Captured test execution & failure screenshots
│   ├── reports/                     # Generated HTML test execution reports
│   ├── logs/                        # Timestamped automation execution logs
│   ├── requirements.txt             # Selenium & Pytest dependencies
│   └── README.md                    # Project documentation & instructions
├── run_app.py                       # Root launcher for the web application
└── requirements.txt                 # Unified requirements
```

---

## 🚀 Step-by-Step Setup & Execution

### 1. Environment Setup (Local or AWS Windows EC2)

1. Open your terminal or Command Prompt / PowerShell.
2. Clone or navigate to the project directory:
   ```bash
   cd "sp23-bse-128(lab assignment)"
   ```
3. Create and activate a Python virtual environment:
   * **Windows:**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### 2. Running the Cloud Web Application

Start the Flask server:
```bash
python run_app.py
```
* The application will run at: `http://127.0.0.1:5000` (or `http://<EC2-PUBLIC-IP>:5000` on AWS).
* **Demo Login Credentials:**
  * Username: `admin` | Password: `Admin@123`
  * Username: `student` | Password: `Student@123`

---

### 3. Executing Selenium Automated Tests

While the web app is running in another terminal window, navigate to the `selenium-project` directory:
```bash
cd selenium-project
```

#### A. Run All Tests with HTML Report (Headless Mode)
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

#### B. Run All Tests with Browser Visible (Recommended for Viva Demonstration)
```bash
pytest tests/ -v --headless=false --html=reports/report.html --self-contained-html
```

#### C. Run a Specific Test File
```bash
# Run Login tests only
pytest tests/test_login.py -v

# Run Registration Form tests only
pytest tests/test_registration.py -v
```

---

## 🧪 Validations & Test Coverage Summary

| Test ID | Test Scenario | Category | Expected Outcome |
|---|---|---|---|
| `TC-LOG-01` | Valid Admin Login | Happy Path | Redirects to `/dashboard`, user badge displays `admin` |
| `TC-LOG-02` | Valid Student Login | Multi-Role | Redirects to `/dashboard`, user badge displays `student` |
| `TC-LOG-03` | Invalid Password | Security | Displays error message: "Invalid username or password" |
| `TC-LOG-04` | Non-Existent User | Security | Displays error message: "Invalid username or password" |
| `TC-LOG-05` | Empty Credentials | Boundary | Displays empty credentials validation message |
| `TC-REG-01` | Valid Student Registration | Functional | Displays success alert banner, increments student table count |
| `TC-REG-02` | Empty Fields Validation | Validation 1 | Displays error message: "All fields are mandatory" |
| `TC-REG-03` | Invalid Email Format | Validation 2 | Rejects malformed email, displays email format error |
| `TC-REG-04` | Short Password (<8 chars) | Validation 3 | Displays error message: "at least 8 characters" |
| `TC-REG-05` | Invalid Numeric Age (<16 or >60) | Validation 4 | Displays error message: "between 16 and 60" |
| `TC-REG-06` | Unselected Department Dropdown | Validation 5 | Displays error message: "select a valid academic department" |
| `TC-REG-07` | Clear Form Button | Reset Flow | Clears all 5 text input fields |
| `TC-REG-08` | Sign Out / Navigation | Navigation | Redirects session from `/dashboard` back to `/login` |
| `TC-REG-09` | CSV Data-Driven Testing | Data-Driven | Executes all valid and invalid scenarios from `users.csv` |

---

## ☁️ AWS Windows Server EC2 Deployment Guide

1. **Provision EC2 Instance:**
   - AMI: *Microsoft Windows Server 2022 Base*
   - Instance Type: `t3.medium` or `t2.micro`
   - Key Pair: Generate and download your `.pem` key.
2. **Security Group Inbound Rules:**
   - **RDP (Port 3389):** Your IP (for remote desktop connection).
   - **HTTP (Port 5000):** Anywhere (`0.0.0.0/0`) or Your IP (for accessing the web app).
3. **Connect to Windows EC2:**
   - Decrypt Administrator password in AWS Console using your `.pem` key.
   - Connect via Microsoft Remote Desktop using Public IP and Administrator credentials.
4. **Setup on Windows Server:**
   - Open PowerShell on the EC2 machine:
     ```powershell
     # Install Google Chrome
     winget install Google.Chrome -e --silent
     # Install Python 3
     winget install Python.Python.3.11 -e --silent
     ```
   - Copy or git clone the project folder onto the EC2 Desktop.
   - Run `pip install -r requirements.txt`.
   - Run `python run_app.py`.
   - Open Chrome on the EC2 desktop and navigate to `http://localhost:5000`.
   - Run tests: `pytest tests/ -v --headless=false`.
