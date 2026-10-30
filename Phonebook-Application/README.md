
# Phonebook Application

A web-based phonebook application built with Python and Flask. It allows users to add, search, update, and delete contact records.

## Features

- Add new contacts
- Search contacts by username
- Update existing phone numbers
- Delete contacts
- Store contact information in a MySQL database
- Configure database settings using environment variables
- Use parameterized SQL queries

## Technologies

- Python
- Flask
- MySQL
- Flask-MySQL
- PyMySQL
- HTML
- Bootstrap

## Project Structure

```text
Phonebook-Application/
├── app/
│   ├── phonebook-app.py
│   ├── requirements.txt
│   └── templates/
│       ├── index.html
│       ├── add-update.html
│       └── delete.html
├── images/
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate to the application directory:

   ```bash
   cd Phonebook-Application
   ```

3. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Git Bash:

   ```bash
   source .venv/Scripts/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

5. Create a `.env` file based on `.env.example` and enter your local MySQL connection settings.

6. Make sure your MySQL database and required table are configured before starting the application.

## Run the Application

```bash
python app/phonebook-app.py
```

Open the following address in your browser:

```text
http://localhost:5000
```

## Security Notes

- Database credentials are provided through environment variables.
- The `.env` file is excluded from Git.
- SQL queries use parameterized statements to reduce SQL injection risk.

## Project Status

This project is being prepared as part of a DevOps portfolio.
