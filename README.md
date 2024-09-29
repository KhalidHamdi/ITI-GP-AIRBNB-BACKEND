# ITI-GP-Airbnb Backend

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)]
[![Django](https://img.shields.io/badge/django-5.1.1-blue.svg)]
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.14.0-blue.svg)]
[![Channels](https://img.shields.io/badge/Django%20Channels-4.0.0-blue.svg)]

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

Running the Server

