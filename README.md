# ITI-GP-Airbnb Backend

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)]
[![Django](https://img.shields.io/badge/django-5.1.1-blue.svg)]
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.14.0-blue.svg)]
[![Channels](https://img.shields.io/badge/Django%20Channels-4.0.0-blue.svg)]

## Repository Stats

![GitHub forks](https://img.shields.io/github/forks/KhalidHamdi/ITI-GP-AIRBNB-BACKEND?style=social)
![GitHub issues](https://img.shields.io/github/issues/KhalidHamdi/ITI-GP-AIRBNB-BACKEND)
![GitHub pull requests](https://img.shields.io/github/issues-pr/KhalidHamdi/ITI-GP-AIRBNB-BACKEND)
![GitHub contributors](https://img.shields.io/github/contributors/KhalidHamdi/ITI-GP-AIRBNB-BACKEND)
![GitHub last commit](https://img.shields.io/github/last-commit/KhalidHamdi/ITI-GP-AIRBNB-BACKEND)
![RepoViews](https://komarev.com/ghpvc/?username=KhalidHamdi&color=green)

## Team

This project was developed by a group of 5 talented software engineers studying at ITI:

1. **Ibrahim Saber**
   - [GitHub](https://github.com/ibrahimsaber1)
   - [LinkedIn](https://www.linkedin.com/in/ibrahim1saber/)
   
2. **Khaled Hamdy**
   - [GitHub](https://github.com/KhalidHamdi)
   - [LinkedIn](https://www.linkedin.com/in/khalidhamdii/)
4. **Basmala Salem**
   - GitHub: [https://github.com/basmalasalem](#) 
   - LinkedIn: [https://www.linkedin.com/in/basmalasalem/](#) 

5. **David Emad**
   - [GitHub](https://github.com/davidemad10)
   - [LinkedIn](https://www.linkedin.com/in/davidemad10/)

6. **Michael Emad**
   - GitHub: [https://github.com/michaelemad](#) 
   - LinkedIn: [https://www.linkedin.com/in/michaelemad/](#) 
---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description

ITI-GP-Airbnb Backend is a robust Django-based backend system designed to power an Airbnb-like application. It offers a suite of RESTful APIs for managing user accounts, property listings, reservations, real-time chats, reviews, and more. The backend leverages Django Channels for real-time communication and integrates Cloudinary for efficient media storage.

## Features

- **User Authentication and Registration:** Secure user sign-up and login using Django Allauth and dj-rest-auth.
- **User Profile Management:** Users can view and edit their profiles, including uploading avatar images.
- **Property Listings Management:** CRUD operations for property listings with categorization.
- **Reservations System:** Manage property bookings and reservations.
- **Real-time Chat Functionality:** Enable real-time communication between users using WebSockets.
- **Reviews and Ratings:** Allow users to leave reviews and ratings for properties.
- **Password Reset via Email:** Secure password reset functionality with email confirmations.
- **Comprehensive API Documentation:** Interactive API docs using Swagger (drf-yasg).
- **Media Storage:** Efficient handling of media assets with Cloudinary integration.
- **Security:** Implemented best practices for securing user data and API endpoints.

## Technologies

- **Backend Framework:** Django 5.1.1
- **API Framework:** Django REST Framework
- **Real-time Communication:** Django Channels, Daphne 4.1.2
- **Database:** PostgreSQL (or as configured)
- **Authentication:** Django Allauth, dj-rest-auth
- **Storage:** Cloudinary for media assets
- **API Documentation:** drf-yasg (Swagger UI & ReDoc)
- **Environment Management:** python-decouple
- **Version Control:** Git, GitHub
- **Other Dependencies:** django-filter, channels, cloudinary_storage

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- **Python:** 3.12.x
- **pip:** Python package installer
- **Git:** Version control system
- **Cloudinary Account:** For media storage
- **PostgreSQL:** Database system (optional, depending on your database choice)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/ITI-GP-AIRBNB-BACKEND.git
   cd ITI-GP-AIRBNB-BACKEND
    ```
2.**Create a Virtual Environment**
   ```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3.**Install Dependencies**
   ```bash
pip install -r requirements.txt
   ```
Ensure your requirements.txt includes all necessary packages, such as Django, djangorestframework, channels, cloudinary, etc.

### Configuration

1.**Environment Variables**
Create a .env file in the root directory and configure the following variables:

   ```bash
# .env

SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password_or_app_password

# Other configurations as needed
   ```
-- Notes:

Replace placeholder values (your_secret_key_here, your_db_name, etc.) with your actual configurations.
Ensure that .env is added to your .gitignore to prevent sensitive information from being committed.

3.**Apply Migrations**
   ```bash
python manage.py createsuperuser
   ```
4.**Collect Static Files**
   ```bash
python manage.py collectstatic
   ```

### Running the Server

Start the development server using:
   ```bash
python manage.py runserver
   ```
The server will start at http://127.0.0.1:8000/

## Running the Server

Start the development server using:

```bash
python manage.py runserver
The server will start at http://127.0.0.1:8000/
   ```
API Documentation
API documentation is available via Swagger UI and ReDoc:

Swagger UI:
```bash
http://127.0.0.1:8000/swagger/
  ```
ReDoc:
```bash
http://127.0.0.1:8000/redoc/
  ```
These interfaces provide interactive documentation where you can explore and test API endpoints.

Testing
Run the test suite using:

```bash
python manage.py test
Ensure all tests pass to verify the integrity of the application.
```
## Deployment

For deploying the application to production, consider the following steps:

### Configure Production Settings

- **Set `DEBUG=False` in your `.env` file.**
- **Define `ALLOWED_HOSTS` with your domain names.**
- **Use a secure `SECRET_KEY`.**

### Set Up a Production Server

Use services like **Heroku**, **AWS**, **DigitalOcean**, or others.

### Configure Web Server

- **Use Gunicorn** as the WSGI HTTP server.
- **Use Nginx** as a reverse proxy.

### Set Up HTTPS

Ensure secure communication by setting up SSL certificates.

### Scale as Needed

Monitor and scale resources based on the application's usage.

### Static and Media Files

- **Serve static files** using WhiteNoise or via a CDN.
- **Ensure media files** are served securely, preferably via Cloudinary.

## Contributing

Contributions are welcome! Follow these steps to contribute:

### Fork the Repository

### Create a Feature Branch

```bash
git checkout -b feature/YourFeatureName
```
## Commit Your Changes
```bash
git commit -m "Add some feature"
```

### Push to the Branch
```bash
git push origin feature/YourFeatureName
```
Open a Pull Request
Describe your changes and submit the PR for review.



---

### **Explanation of the README Structure**

1. **Badges:**
   - **License Badge:** Indicates the project is under the MIT License.
   - **Python Badge:** Shows the Python version used.
   - **Django Badge:** Displays the Django version.
   - **Django REST Framework & Channels Badges:** Highlight additional technologies used.

2. **Table of Contents:**
   - Provides easy navigation to different sections of the README.

3. **Project Description:**
   - A brief overview of what the project is about.

4. **Features:**
   - Lists the key functionalities and capabilities of the backend.

5. **Technologies:**
   - Details the technologies and frameworks used in the project.

6. **Getting Started:**
   - **Prerequisites:** Lists what is needed before setting up the project.
   - **Installation:** Step-by-step instructions to set up the project locally.
   - **Configuration:** Guidance on setting environment variables and other configurations.

7. **Running the Server:**
   - Instructions on how to start the development server.

8. **API Documentation:**
   - Links to interactive API documentation generated by Swagger and ReDoc.

9. **Testing:**
   - Commands and instructions to run tests to ensure the application's integrity.

10. **Deployment:**
    - High-level steps and considerations for deploying the application to a production environment.

11. **Contributing:**
    - Guidelines for how others can contribute to the project.

12. **License:**
    - Specifies the project's license, linking to the `LICENSE` file.

13. **Contact:**
    - Provides contact information for the project owner or maintainers.

### **Customization Tips**

- **Repository Links:** Replace `https://github.com/your-username/ITI-GP-AIRBNB-BACKEND.git` with your actual GitHub repository URL.
- **Cloudinary & Database Credentials:** Ensure that you provide accurate details in the `.env` file and avoid committing sensitive information.
- **License:** Ensure that you have a `LICENSE` file in your repository. If not, you can create one based on the [MIT License](https://opensource.org/licenses/MIT) or your preferred license.
- **Testing & Deployment:** Expand these sections based on the specific testing frameworks and deployment strategies you employ.
- **Screenshots & Media:** Consider adding screenshots or media links to showcase your project visually.

### **Final Steps**

1. **Create the `README.md` File:**

   In the root directory of your backend project, create a file named `README.md` and paste the above content into it.

2. **Adjust Placeholders:**

   - Replace `your-username` with your actual GitHub username.
   - Update the repository URL, email, and any other placeholders with your actual information.
   - Ensure that all paths and configurations match your project's structure.

3. **Commit and Push:**

   ```bash
   git add README.md
   git commit -m "Add comprehensive README.md"
   git push origin main  # Replace 'main' with your default branch name if different
   ```
