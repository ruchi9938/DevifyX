# Django Quiz Application

A feature-rich quiz application built with Django that allows users to take quizzes, track their progress, and administrators to manage questions and categories.

## Features

- User Authentication (Login/Register)
- Quiz Categories
- Multiple Choice Questions
- Score Tracking
- User Profiles
- Admin Dashboard
- Maximum Attempts per Question
- Password Reset Functionality

## Prerequisites

- Python 3.x
- Django
- SQLite (default database)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DjangoQuiz
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

### For Users
1. Register a new account or login
2. Browse available quiz categories
3. Select a category to start a quiz
4. Answer questions and submit
5. View your results and score
6. Check your profile for quiz history

### For Administrators
1. Login with admin credentials
2. Access admin dashboard
3. Add/Edit/Delete:
   - Categories
   - Questions
   - User profiles
4. View quiz statistics and user performance

## Project Structure

```
DjangoQuiz/
├── Quiz/
│   ├── templates/
│   │   └── Quiz/
│   │       ├── dashboard.html
│   │       ├── quiz.html
│   │       ├── profile.html
│   │       └── ...
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── manage.py
└── requirements.txt
```

## Models

- User: Django's built-in user model
- UserProfile: Extended user information
- Category: Quiz categories
- QuesModel: Questions and answers
- QuizAttempt: User quiz attempts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please open an issue in the repository. 