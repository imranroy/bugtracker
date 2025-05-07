# 🐞 Bug Tracker Web Application

A role-based bug tracking system built with Django. It supports Managers, Developers, and QA roles, allowing seamless project management, issue reporting, and status tracking.

## 🚀 Features

- ✅ Role-based access: Manager, Developer, QA
- 🛠️ Project creation and assignment
- 🧑‍💻 Developer can pick projects and update bug statuses
- 🔍 QA can review projects and raise issues
- 📊 Dashboard for each role with real-time project/bug tracking
- 💾 SQLite database for development
- 🔐 Secure authentication using Django's built-in system


## 🧰 Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Tools:** Git, Postman, Swagger (for API docs), VS Code

## 📂 Project Structure

```bash
bugtracker/
├── tracker/             # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── urls.py
├── bugtracker/          # Project settings
│   ├── settings.py
│   └── urls.py
├── static/              # Static files (CSS/JS)
├── db.sqlite3           # SQLite DB
└── README.md
#######################################################################################################################
# Clone the repository
git clone https://github.com/imranroy/bugtracker.git
cd bugtracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
##########################################################################################################################
| Role      | Capabilities                                      |
| --------- | ------------------------------------------------- |
| Manager   | Create projects, assign developers, view all bugs |
| Developer | Pick project, mark bugs as resolved               |
| QA        | Pick project, raise issues, view bug status       |
