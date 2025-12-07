# 🛡️ SalmaGuard Auth System

![Project Banner](static/images/wallpaper.jpg)

> A modern, secure, and fully responsive Authentication System built with Python Flask. Featuring a premium Glassmorphism UI, Dark Mode, and a dynamic user dashboard.

---

## 🌟 Key Features

* **🔐 Secure Authentication:** Robust Login & Registration system with password hashing (Werkzeug).
* **🎨 Glassmorphism UI:** Stunning visual design using modern CSS backdrop-filters.
* **🌓 Dark/Light Mode:** Toggle themes instantly with local preference saving.
* **📊 User Dashboard:** Dynamic dashboard showing real-time stats, last login, and activity logs.
* **📸 Profile Management:** Users can upload profile pictures or get an auto-generated letter avatar.
* **💪 Password Strength Meter:** Real-time visual feedback on password complexity.
* **👁️ UX Enhancements:** Show/Hide password toggles and auto-dismissing alerts.
* **📱 Fully Responsive:** Works perfectly on desktops, tablets, and mobile devices.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Flask
* **Database:** SQLite3 (Built-in)
* **Frontend:** HTML5, CSS3 (Custom Variables), JavaScript (Vanilla)
* **Security:** Werkzeug Security, CSRF Protection logic

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### Prerequisites

* Python 3.8 or higher installed.
* Git installed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/SalmaGuard-Auth.git](https://github.com/YOUR_USERNAME/SalmaGuard-Auth.git)
    cd SalmaGuard-Auth
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment:**
    * Ensure you have a folder named `static/images` and `static/profile_pics`.
    * Ensure `wallpaper.jpg` exists in `static/images`.

5.  **Run the Application:**
    ```bash
    python app.py
    ```

6.  **Open in Browser:**
    Go to `http://127.0.0.1:5000`

---

## 📂 Project Structure

```text
SalmaGuard-Auth/
├── app.py                 # Application Entry Point
├── database.db            # Auto-generated SQLite Database
├── requirements.txt       # Project Dependencies
├── static/
│   ├── theme.css          # Main Styling
│   ├── script.js          # UI Logic
│   ├── images/            # Assets
│   └── profile_pics/      # User Uploads
└── templates/
    ├── base.html          # Layout Skeleton
    ├── login.html         # Login Page
    ├── register.html      # Signup Page
    └── dashboard.html     # User Dashboard