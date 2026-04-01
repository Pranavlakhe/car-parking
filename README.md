# Car Parking Management System

A web-based car parking management system built with Flask and MySQL.

## Features

- User Registration and Login
- Parking Spot Booking
- Secure Password Handling
- Session Management
- Flash Messages for User Feedback

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

## Setup Instructions

1. Clone or download the project to your local machine.

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Open MySQL Workbench or MySQL command line
   - Import and run the `database.sql` file to create the necessary database and tables

4. Configure the MySQL connection in `app.py`:
   - Update the following configuration if needed:
     ```python
     app.config['MYSQL_HOST'] = 'localhost'
     app.config['MYSQL_USER'] = 'root'
     app.config['MYSQL_PASSWORD'] = ''
     app.config['MYSQL_DB'] = 'car_parking'
     ```

5. Run the Flask application:
   ```bash
   python app.py
   ```

6. Access the website:
   - Open your web browser
   - Navigate to `http://localhost:5000`

## Project Structure

```
car parking/
├── app.py                 # Flask application
├── database.sql           # Database schema
├── requirements.txt       # Python dependencies
├── static/               # Static files (CSS, images)
└── templates/            # HTML templates
    ├── home.html
    ├── registration.html
    ├── login.html
    ├── form.html
    └── ...
```

## Usage

1. Register a new account with your car number and details
2. Login with your credentials
3. Book a parking spot by filling out the parking form
4. View your booking status

## Security Features

- Passwords are hashed before storage
- Session-based authentication
- Form validation and sanitization
- CSRF protection

## Note

This is a basic implementation and can be extended with additional features such as:
- Payment integration
- Admin dashboard
- Booking history
- Email notifications
- QR code generation for parking spots