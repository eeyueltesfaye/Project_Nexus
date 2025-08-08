# Project Nexus – Job Board Platform API

A professional, role-based job board API built with Django and Django REST Framework. It allows job seekers to browse and apply for jobs, while recruiters can manage job postings and applications. Admins oversee user roles and platform moderation.

> -  **Live API Base URL**: https://mysite-z2xs.onrender.com  
> -  **Swagger API Docs**: https://mysite-z2xs.onrender.com/api/docs/


## 🚀 Features

- Role-based authentication (Admin, Recruiter, Job Seeker)
- Recruiter role request & admin approval workflow
- Job creation, listing, updating, and deletion
- Job application & save/favorite functionality
- Profile creation with resume upload
- Full test coverage using `pytest`
- Swagger/OpenAPI documentation
- Deployed on Render with PostgreSQL


## 📚 API Endpoints Overview

All endpoints are prefixed with `/api/`

### Auth & User Management
- POST `/api/users/register/` - Register user
- POST `/api/users/login/` - Log in and get access token
- POST `/api/users/logout/` - Log out user
- GET `/api/users/profile/status` - Get current user's profile
- PUT `/api/users/profile/update/` - Update user profile
- GET `/api/users/profile/resume/` - Download user resume

### Recruiter Role Requests
- POST `/api/users/request-role/` - Request recruiter role
- GET `/api/users/role-requests/` - List role requests (Admin only)
- PUT `/api/users/role-requests/<id>/approve/` - Approve request (Admin)
- PUT `/api/users/role-requests/<id>/reject/` - Reject request (Admin)

### Jobs
- GET `/api/jobs/` - List all jobs
- POST `/api/jobs/create/` - Create job (Recruiter)
- GET `/api/jobs/<id>/` - Retrieve a job
- PUT `/api/jobs/<id>/update/` - Update job (Recruiter)
- DELETE `/api/jobs/<id>/delete/` - Delete job (Recruiter)

### Job Applications
- POST `/api/jobs/<id>/apply/` - Apply to a job
- GET `/api/jobs/applications/` - List user applications
- GET `/api/jobs/recruiter-applications/` - List recruiter’s received applications

### Saved Jobs
- POST `/api/jobs/<id>/save/` - Save a job
- GET `/api/jobs/saved/` - List saved jobs
- DELETE `/api/jobs/saved/<id>/delete/` - Remove saved job

### Categories
- GET `/api/categories/` - List all categories
- POST `/api/categories/create/` - Create category (Admin)
- PUT `/api/categories/<id>/update/` - Update category (Admin)
- DELETE `/api/categories/<id>/delete/` - Delete category (Admin)

---

## 🛠 Tech Stack

- Python 3.10+
- Django & Django REST Framework
- PostgreSQL (Render DB)
- JWT Authentication (SimpleJWT)
- Swagger Docs (`drf_yasg`)
- Pytest for testing
- Render for deployment


## ⚙️ Local Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL (or use SQLite for testing)
- Git

### Installation

```bash
# Clone the repo
git https://github.com/eeyueltesfaye/Project_Nexus
cd project-nexus

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env)
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

---

## 🚀 Deployment (Render)

This project uses `render.yaml` for one-click deployment via Render.

### Deploy steps:

- Push your project to GitHub
- Connect to Render as a Blueprint deployment
- Render detects the `render.yaml` and provisions:
  - PostgreSQL database
  - Web service
  - Environment variables

---

##  API Documentation

Interactive Swagger docs available at:

- [https://mysite-z2xs.onrender.com/api/docs/](https://mysite-z2xs.onrender.com/api/docs/)


## 🤝 Contributing

- Fork this repo
- Create a new feature branch
- Commit changes with clear messages
- Push and open a pull request

Tests are encouraged for all new features.


## 📄 License

Feel free to use and modify with attribution.

## 👤 Author

**Eyuel Tesfaye**  
Backend Developer | DevOps Intern  
📍 Addis Ababa, Ethiopia  
GitHub: [@eeyueltesfaye](https://github.com/eeyueltesfaye)
