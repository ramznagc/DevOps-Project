# DevOps Project – Phonebook Application

A Flask-based phonebook web application maintained as part of my DevOps and cloud engineering portfolio.

The application supports basic contact management and is organized as a standalone application inside this repository.

## Features

- Add new contacts
- Search contacts by name
- Update phone numbers
- Delete contact records
- Store data in a MySQL database
- Configure database connection details through environment variables

## Technology Stack

- Python
- Flask
- MySQL
- PyMySQL
- HTML and Bootstrap
- Git and GitHub

## Repository Structure

```text
DevOps-Project/
└── Phonebook-Application/
    ├── app/
    │   ├── phonebook-app.py
    │   ├── requirements.txt
    │   └── templates/
    ├── images/
    ├── .env.example
    ├── .gitignore
    └── README.md
```

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/ramznagc/DevOps-Project.git
   cd DevOps-Project/Phonebook-Application
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Git Bash on Windows:

   ```bash
   source .venv/Scripts/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

4. Create a local `.env` file using `.env.example` as a reference and provide your own database configuration. Do not commit real credentials.

5. Ensure the MySQL database and required table are available, then start the application:

   ```bash
   python app/phonebook-app.py
   ```

6. Open [http://localhost:5000](http://localhost:5000) in your browser.

For the application-specific details and configuration notes, see [Phonebook-Application/README.md](Phonebook-Application/README.md).

## Security Notes

- Keep database passwords and other credentials out of source control.
- Use the provided environment-file example as a template, not as a place for real secrets.
- Review database permissions and network access before deploying beyond a local development environment.

## Project Purpose

This project demonstrates a Python web application workflow and provides a foundation for practicing application configuration, database integration, and DevOps deployment practices.

## Author

Ramazan Agac

GitHub: [@ramznagc](https://github.com/ramznagc)
