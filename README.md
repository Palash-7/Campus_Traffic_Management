 🚗 Campus Traffic Management System

A Flask-based web application designed for controlling and monitoring vehicle traffic within the Shiv Nadar Institute of Eminence campus. The system utilizes **ANPR** (Automatic Number Plate Recognition), manual data entry, and a secure backend to streamline gate access, monitor errant behavior, and support data-driven campus security operations.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Data Policy](#data-policy)
- [Contributing](#contributing)


---

## Project Overview

This project automates the registration, monitoring, and control of vehicular traffic within the campus, focusing on:

- Improved gate access through **automated ANPR-based control**
- Real-time monitoring via integrated **CCTV**
- Backend management using a **Database Management System (DBMS)**
- Enhanced campus security with reporting of errant driving behavior
- Generation of data reports for analysis and operational insight

---

## ✅ Features

- Automatic Number Plate Recognition (ANPR) integration
- Manual data entry interface for security officers
- Real-time entry/exit logs
- Traffic violation reporting dashboard
- Data analysis capabilities

---

## 🏗️ System Architecture

The system operates via components installed at the main campus gate and the security office. It includes:

- **Frontend** (HTML via Flask's Jinja2)
- **Backend** (Python + Flask)
- **Database** (for storing vehicle and access logs)

---

## 🛠️ Technologies Used

- Python 3
- Flask
- HTML/CSS (via `templates/`)
- Jinja2 templating
- SQLite or other DBMS (assumed)
- ANPR & CCTV integration (conceptual/placeholder)

---

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Palash-7/Campus_Traffic_Management.git
cd Campus_traffic_web

2. Set Up Virtual Environment (Optional)

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install Dependencies

pip install flask

4. Run the App

cd campus_web_traffic
python3 app.py
Visit http://127.0.0.1:5000/ in your browser.

Folder Structure

campus_web_traffic/
├── templates/             # HTML frontend files
├── app.py                 # Main application file
├── static/                
├── db/                   



Data Policy
Data Access Control Policy

Data Encryption Policy

Data Retention and Deletion Policy

Incident Response and Logging Policy

Secure API and Third-Party Integration Policy

Backup and Disaster Recovery Policy

Compliance and Privacy Policy

Contributing
We welcome contributions! Feel free to fork the repository, create new branches, and submit pull requests for review.


Acronyms Used
ANPR: Automatic Number Plate Recognition

CCTV: Closed-Circuit Television

DBMS: Database Management System


