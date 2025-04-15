# SkillPluss - Online Learning Platform

SkillPluss is a comprehensive online learning platform that connects instructors and students, enabling seamless course creation, enrollment, and learning experiences.

## Features

### For Students
- Browse and search for courses across various categories
- Enroll in free and paid courses
- Access course content including video lessons, text content, and downloadable resources
- Track learning progress
- Rate and review courses
- Receive certificates upon completion

### For Instructors
- Create and manage courses
- Upload course content including videos, text, and resources
- Track student enrollment and progress
- Receive ratings and feedback
- Customize course settings and pricing

### Platform Features
- User authentication and profile management
- Course categorization and filtering
- Responsive design for desktop and mobile devices
- Payment integration for paid courses
- Rating and review system

## Technology Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django Authentication System
- **File Storage**: Django File Storage

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/yourusername/CoursePlatform.git
   cd CoursePlatform
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```
   python manage.py migrate
   ```

5. Create a superuser
   ```
   python manage.py createsuperuser
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

```
CoursePlatform/
├── skillPluss/              # Main project directory
│   ├── courses/             # Courses app
│   │   ├── models.py        # Database models
│   │   ├── views.py         # View functions
│   │   ├── urls.py          # URL patterns
│   │   └── templates/       # HTML templates
│   ├── accounts/            # User accounts app
│   ├── payments/            # Payment processing app
│   └── settings.py          # Project settings
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── requirements.txt         # Project dependencies
└── manage.py                # Django management script
```

## Usage

### For Students
1. Register an account or log in
2. Browse available courses
3. Enroll in courses of interest
4. Access course content and track progress
5. Rate and review completed courses

### For Instructors
1. Register as an instructor
2. Create and publish courses
3. Upload course content and resources
4. Monitor student enrollment and progress
5. Respond to student feedback

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django framework
- Bootstrap for UI components
- All contributors and users of the platform

## Contact

For any questions or support, please contact [arshabh2005@gmai.com).
