# Job Portal – Django (In Progress 🚧)

A role-based Job Portal web application built using **Django**, where **Recruiters** can post jobs and manage applications, and **Jobseekers** can apply for jobs and track their application status.

This project is currently **in progress** and is being actively developed to improve features, UI/UX, and scalability.

---

## 🚀 Features Implemented

### 👤 Authentication & Authorization
- Custom User model with role-based access (`jobseeker`, `recruiter`)
- Signup, Login, Logout
- Role-based route protection
- Secure access control for dashboards and actions

---

### 🧑‍💼 Recruiter Features
- Recruiter dashboard
- Post new jobs
- View list of posted jobs
- View applications for each job
- Download applicant resumes
- Accept / Reject job applications
- Access restricted to recruiter-owned jobs only

---

### 🧑‍🎓 Jobseeker Features
- Jobseeker dashboard
- View all available jobs
- View job details
- Apply for jobs with resume upload
- Prevent duplicate job applications
- View “My Applications” with real-time status (Pending / Accepted / Rejected)

---

### 📂 Application Management
- Separate `applications` app
- Application status management
- Resume upload using Django `FileField`
- Secure file handling with `MEDIA_ROOT` and `MEDIA_URL`

---

## 🏗 Project Structure

jobportal/
├── accounts/
├── jobs/
├── applications/
├── templates/
├── static/
├── media/
├── manage.py
└── README.md

---

## ⚙️ Project Setup (Local Development)

### Prerequisites
- Python 3.10+
- pip
- Virtualenv (recommended)

### Setup Steps

```bash
git clone https://github.com/<your-username>/jobportal.git
cd jobportal

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Create .env file and add:
# SECRET_KEY=your-django-secret-key

python manage.py migrate
python manage.py runserver
