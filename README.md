# 🛡️ SalmaGuard - Flask Authentication System

A modern, secure authentication platform built with Flask and SQLite featuring user management, activity tracking, and a premium glassmorphism UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## ✨ Features

### Core Functionality
- 🔐 **Secure Authentication** - Password hashing (PBKDF2-SHA256), session management
- 👤 **User Profiles** - Profile picture upload, username/email editing
- 📊 **Statistics Dashboard** - Real-time session tracking, action counting
- 📝 **Activity Logging** - Automatic tracking of all user actions
- 🔍 **Live Search** - Filter activity feed without page reload
- ⚡ **Quick Actions** - One-click access to common operations
- 🗑️ **Account Management** - Secure account deletion with confirmation

### UI/UX Design
- 🎨 **Glassmorphism Design** - Modern, frosted-glass aesthetic
- 🌓 **Dark/Light Theme** - Toggle with localStorage persistence
- 📱 **Fully Responsive** - Optimized for mobile, tablet, desktop
- ✨ **Smooth Animations** - Professional transitions and effects
- 💪 **Password Strength** - Real-time validation feedback

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone repository
git clone https://github.com/salmaelsharkwy/Salma-Flask-SQLiteProject.git
cd Salma-Flask-SQLiteProject

2. Create virtual environment
python -m venv venv

3. Activate virtual environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Run application
python app.py


### Access Application
Open browser: [**http://127.0.0.1:5000**](http://127.0.0.1:5000)

---

## 📁 Project Structure

Salma-Flask-SQLiteProject/
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── database.db # SQLite database (auto-generated)
├── static/
│ ├── theme.css # Glassmorphism styling
│ ├── script.js # Client-side functionality
│ ├── images/ # Background images
│ └── profile_pics/ # User uploads
└── templates/
├── base.html # Master template
├── login.html # Login page
├── register.html # Registration page
├── dashboard.html # User dashboard
├── profile.html # Profile & activity tracking
└── forgot_password.html


## 💻 Technology Stack

**Backend**
- Flask 3.0.0 - Web framework
- SQLite3 - Database
- Werkzeug 3.0.1 - Security utilities

**Frontend**
- HTML5, CSS3, JavaScript
- Font Awesome icons
- Google Fonts (Outfit)



## 🚀 Future Enhancements

- [ ] Email verification system
- [ ] Password reset functionality
- [ ] Two-factor authentication (2FA)
- [ ] Export activity data (CSV/JSON)
- [ ] Advanced analytics dashboard
- [ ] RESTful API endpoints

---

## 📝 Development Notes

**Total Development Effort**: 40+ hours  
**Lines of Code**: ~1,500 lines  
**Files Created**: 10+ templates and modules  

**Major Challenges Solved**:
1. Real-time session time calculation
2. Live search without backend queries
3. Unique profile picture naming
4. Database integrity with constraints

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature-name`)
5. Open Pull Request


## 👤 Author

**Salma Elsharkwy**  
GitHub: [@salmaelsharkwy](https://github.com/salmaelsharkwy)

---

## 📞 Support

- 🐛 **Report Bugs**: [Open an issue](https://github.com/salmaelsharkwy/Salma-Flask-SQLiteProject/issues)
- 💡 **Feature Requests**: [Submit a request](https://github.com/salmaelsharkwy/Salma-Flask-SQLiteProject/issues/new)
- 📧 **Contact**: Open an issue for questions


<div align="center">

**⭐ Star this repository if you found it helpful!**

Built with ❤️ using Flask & Python

</div>