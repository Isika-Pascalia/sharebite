# 🍽️ ShareBite - Food Donation Platform

![ShareBite Logo](https://img.shields.io/badge/ShareBite-Food%20Donation%20Platform-green?style=for-the-badge&logo=utensils)

**ShareBite** is a beginner-friendly web application that connects food donors with people in need, helping reduce food waste while building stronger communities. Built with Flask, MySQL, and modern web technologies.

## 🎓 Learning Project

This project was built as part of learning Flask web development and demonstrates:
- Full-stack web development with Python Flask
- Database design and MySQL integration
- User authentication and password security
- Responsive web design principles
- JavaScript DOM manipulation and AJAX
- Modern UI/UX design patterns

## 🌟 Features

### Core Functionality
- **🏠 Homepage**: Beautiful card-based display of available food donations
- **👤 User Authentication**: Secure registration and login system
- **🎁 Food Donation**: Easy form to post surplus food for sharing
- **✋ Claim System**: One-click claiming with real-time updates
- **🔍 Live Search**: Filter donations by food name or location instantly
- **📱 Responsive Design**: Works perfectly on all devices

### Technical Features
- **🔒 Secure Authentication**: Password hashing with Werkzeug
- **🛡️ SQL Injection Protection**: Parameterized database queries
- **⚡ Real-time Updates**: AJAX-powered claiming without page reloads
- **📊 Database Relations**: Proper foreign key relationships
- **🎨 Modern UI**: Glass-morphism effects and smooth animations

## 📊 Project Status

**Current Status**: ✅ Fully Functional Local Development Version
- All core features implemented and tested
- Ready for local deployment
- Suitable for portfolio demonstration
- Built following best practices for Flask development

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- MySQL Server 5.7+
- Windows/macOS/Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Isika-Pascalia/sharebite.git
   cd sharebite
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL**
   - Update `config.py` with your MySQL credentials
   ```python
   DB_USER = 'your_mysql_username'
   DB_PASSWORD = 'your_mysql_password'
   ```

5. **Initialize database**
   ```bash
   python config.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
sharebite/
├── app.py                 # Main Flask application
├── config.py             # Database configuration
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── static/
│   ├── css/
│   │   └── style.css    # Responsive CSS styling
│   └── js/
│       └── script.js    # Interactive JavaScript
└── templates/
    ├── base.html        # Base template layout
    ├── index.html       # Homepage template
    ├── login.html       # Login page template
    ├── register.html    # Registration template
    └── donate.html      # Food donation form
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MySQL with mysql-connector-python
- **Security**: Werkzeug for password hashing
- **Session Management**: Flask sessions

### Frontend
- **Structure**: HTML5 semantic markup
- **Styling**: CSS3 with Flexbox and Grid
- **Interactivity**: Vanilla JavaScript (ES6+)
- **Design**: Mobile-first responsive design

### Database Schema
- **users**: User authentication and profiles
- **food_donations**: Food listings with donor information
- **Relationships**: Foreign key constraints for data integrity

## 🎯 Usage

### For Food Donors
1. **Register/Login** to your account
2. **Click "Donate Food"** in the navigation
3. **Fill out the form** with food details, quantity, and pickup location
4. **Submit** to make your donation available to the community

### For Food Recipients
1. **Browse available donations** on the homepage
2. **Search or filter** by food name or location
3. **Register/Login** to claim food items
4. **Click "Claim"** on any available item
5. **Contact the donor** using provided contact information

### For Everyone
- **Real-time search** without page reloads
- **Mobile-friendly interface** for on-the-go access
- **Secure authentication** protects user data

## 🔧 Configuration

### Database Settings
Update `config.py` with your MySQL configuration:

```python
class Config:
    DB_HOST = 'localhost'          # MySQL server host
    DB_USER = 'root'               # MySQL username
    DB_PASSWORD = 'your_password'  # MySQL password
    DB_NAME = 'sharebite_db'       # Database name
    SECRET_KEY = 'your-secret-key' # Flask session key
```

### Environment Variables (Production)
For production deployment, use environment variables:

```bash
export DB_PASSWORD=your_secure_password
export SECRET_KEY=your_secret_key
```

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for visual customizations
- Update CSS variables for color schemes
- Responsive breakpoints are pre-configured

### Features
- Add new routes in `app.py`
- Create corresponding templates in `templates/`
- Extend database schema in `config.py`

## 🔒 Security Features

- **Password Hashing**: All passwords securely hashed with Werkzeug
- **SQL Injection Protection**: Parameterized queries throughout
- **Session Management**: Secure user sessions with Flask
- **Input Validation**: Both frontend and backend validation
- **CSRF Protection**: Ready for CSRF token implementation

## 🚀 Production Deployment

### Preparation
1. Set strong `SECRET_KEY` in production
2. Use environment variables for sensitive data
3. Configure proper MySQL user permissions
4. Enable HTTPS for secure connections

### Recommended Hosting
- **Backend**: Heroku, DigitalOcean, or AWS
- **Database**: MySQL on cloud providers
- **Static Files**: CDN for better performance

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

### Development Guidelines
- Follow PEP 8 for Python code
- Write descriptive commit messages
- Test all features before submitting
- Update documentation for new features

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
Error connecting to MySQL: Access denied for user 'root'@'localhost'
```
- Verify MySQL credentials in `config.py`
- Ensure MySQL service is running
- Check user permissions

**Template Not Found**
- Verify `templates/` folder structure
- Check file names match exactly
- Ensure Flask can find template directory

**CSS/JS Not Loading**
- Verify `static/` folder structure
- Check file paths in HTML templates
- Clear browser cache

**Port Already in Use**
```bash
OSError: [Errno 98] Address already in use
```
- Kill existing Flask processes
- Use different port: `app.run(port=5001)`

## 💻 Development Skills Demonstrated

This project showcases:
- **Backend Development**: Flask framework, routing, and templating
- **Database Management**: MySQL schema design and queries
- **Frontend Development**: HTML5, CSS3, and JavaScript
- **Security Implementation**: Authentication and data protection
- **Responsive Design**: Mobile-first CSS approach
- **Version Control**: Git workflow and project structure
- **Documentation**: Comprehensive README and code comments

## 👥 Author

- **Pascalia Isika** - Full Stack Development - [Isika-Pascalia](https://github.com/Isika-Pascalia)

## 📞 Contact & Support

- **GitHub**: [@Isika-Pascalia](https://github.com/Isika-Pascalia)
- **Issues**: Report bugs or request features via GitHub Issues

## 🔮 Future Enhancements

- [ ] Email notifications for claimed items
- [ ] User profiles and donation history
- [ ] Food categories and dietary filters
- [ ] Geolocation-based matching
- [ ] Mobile app development
- [ ] Admin dashboard for moderation
- [ ] Integration with food safety guidelines
- [ ] Multi-language support

## 🙏 Acknowledgments

- Flask community for excellent documentation
- MySQL for reliable database management
- Web development tutorials and resources
- Open source community for inspiration

---

**Built with ❤️ as a learning project to combat food waste**

*ShareBite - Reducing food waste, one meal at a time.*

**Project completed as part of Flask web development learning journey.**