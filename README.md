# ICARIS - Integrated Compliance Assessment & Risk-Management Information System 





![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

ICARIS is a comprehensive Governance, Risk, and Compliance (GRC) management platform designed to help organizations track, monitor, and manage their security posture, compliance obligations, and risk landscape. Built with Django and modern web technologies, ICARIS provides an intuitive interface for security teams, compliance officers, and executives.

## ✨ Features

### 🎯 Core Modules

- **Executive Dashboard** - Real-time metrics and visualizations for compliance score, open items, and risk distribution
- **PO&AMs (Plans of Action & Milestones)** - Track and manage security action items and remediation tasks
- **ConMons (Continuous Monitoring)** - Interactive risk register with 5x5 heat matrix visualization
- **Artifacts** - Centralized document management for system artifacts and evidence

### 🔐 Key Capabilities

- ✅ Risk assessment and tracking with likelihood/impact scoring
- ✅ Compliance framework management (GDPR, SOX, NIST, etc.)
- ✅ Audit planning and findings documentation
- ✅ Issue/task assignment and due date tracking
- ✅ Real-time dashboards with Chart.js visualizations
- ✅ Role-based access control
- ✅ Department-based filtering and organization

## 🚀 Technology Stack

- **Backend:** Django 4.2
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite (development) / PostgreSQL (production-ready)
- **Visualization:** Chart.js
- **Icons:** Font Awesome 6
- **Styling:** Custom CSS with modern design principles

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/icaris-grc-dashboard.git
   cd icaris-grc-dashboard
```

2. **Create and activate virtual environment**
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

4. **Run migrations**
```bash
   python manage.py makemigrations
   python manage.py migrate
```

5. **Create superuser account**
```bash
   python manage.py createsuperuser
```

6. **Load sample data (optional)**
```bash
   python create_sample_data.py
```

7. **Run the development server**
```bash
   python manage.py runserver
```

8. **Access the application**
   - Dashboard: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📊 Database Models

### Core Models

- **Department** - Organizational units
- **Risk** - Risk register entries with severity, likelihood, and impact scoring
- **ComplianceFramework** - Regulatory frameworks (GDPR, SOX, NIST, etc.)
- **ComplianceControl** - Individual controls mapped to frameworks
- **Audit** - Audit scheduling, findings, and recommendations
- **Issue** - Action items and PO&AMs with priority and status tracking

## 🎨 Screenshots

### Executive Dashboard
![Dashboard](screenshots/dashboard.png)

### Risk Heat Matrix
![Risk Register](screenshots/risk-register.png)

### PO&AMs Management
![POAMs](screenshots/poams.png)

## 🔒 Security Features

- User authentication and session management
- CSRF protection
- SQL injection prevention via Django ORM
- XSS protection
- Secure password hashing
- Login required decorators for protected views

## 📚 Project Structure
```
icaris-grc-dashboard/
├── grc_project/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── grc_dashboard/            # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── forms.py              # Django forms
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin configuration
│   └── templates/            # HTML templates
│       ├── grc_dashboard/
│       │   ├── dashboard.html
│       │   ├── risk_register.html
│       │   └── issue_tracking.html
│       └── registration/
│           └── login.html
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── create_sample_data.py     # Sample data generator
```

## 🛠️ Configuration

### Settings

Key configuration options in `grc_project/settings.py`:
```python
# Authentication
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 📝 Usage Examples

### Creating a Risk Entry

1. Navigate to ConMons (Risk Register)
2. Click "Add New Risk"
3. Fill in required fields:
   - Title and description
   - Department
   - Severity level
   - Likelihood (1-5)
   - Impact (1-5)
   - Mitigation plan
4. Save to add to risk matrix

### Adding a PO&AM

1. Navigate to PO&AMs
2. Click "Add PO&AM"
3. Enter action item details
4. Assign to user
5. Set priority and due date
6. Track status through completion

## 🚧 Roadmap

- [ ] File upload for artifact storage
- [ ] Advanced reporting and export (PDF, Excel)
- [ ] Email notifications for overdue items
- [ ] API endpoints for integration
- [ ] Multi-tenant support
- [ ] Advanced analytics and trending
- [ ] Mobile responsive optimization
- [ ] Offline mode for air-gapped environments

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines for Python code.

## 🤝 Contributing

This is a capstone project for educational purposes. Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Timothy Terrance**
- GitHub: [@YourUsername](https://github.com/CodeMagicianEquinox)

## 🙏 Acknowledgments

- Built as a capstone project for the Full Stack Development Immersive Program at San Diego Global Knowledge University
- Inspired by enterprise GRC platforms like ServiceNow
- Chart.js for data visualization
- Font Awesome for iconography
- Django community for excellent documentation

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

**Note:** This system is designed for educational and demonstration purposes. For production use in a regulated environment, additional security hardening, compliance validation, and professional security assessment is recommended.

Just replace:
