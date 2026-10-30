
import os

from flask import Flask, request, render_template
from flaskext.mysql import MySQL


app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_DATABASE_HOST")
app.config["MYSQL_DATABASE_USER"] = os.getenv("MYSQL_DATABASE_USER")
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_DATABASE_PASSWORD")
app.config["MYSQL_DATABASE_DB"] = os.getenv("MYSQL_DATABASE_DB", "phonebook")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_DATABASE_PORT", "3306"))

mysql = MySQL()
mysql.init_app(app)

DEVELOPER_NAME = "Phonebook Application"


def get_connection():
    """Create a database connection."""
    connection = mysql.connect()
    connection.autocommit(True)
    return connection


def init_phonebook_db():
    """Create the phonebook table if it does not exist."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                number VARCHAR(100) NOT NULL,
                PRIMARY KEY (id)
            ) ENGINE=InnoDB
            DEFAULT CHARSET=utf8mb4
            COLLATE=utf8mb4_unicode_ci;
        """)
    finally:
        cursor.close()
        connection.close()


def find_persons(keyword):
    """Find phonebook records matching a name keyword."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            SELECT id, name, number
            FROM phonebook
            WHERE LOWER(name) LIKE %s
        """
        cursor.execute(query, (f"%{keyword.strip().lower()}%",))
        results = cursor.fetchall()

        persons = [
            {
                "id": row[0],
                "name": row[1].strip().title(),
                "number": row[2]
            }
            for row in results
        ]

        if not persons:
            persons = [{"name": "No Result", "number": "No Result"}]

        return persons
    finally:
        cursor.close()
        connection.close()


def insert_person(name, number):
    """Insert a new phonebook record."""
    connection = get_connection()
    cursor = connection.cursor()

    normalized_name = name.strip().lower()

    try:
        cursor.execute(
            "SELECT id, name FROM phonebook WHERE LOWER(name) = %s",
            (normalized_name,)
        )

        existing_person = cursor.fetchone()

        if existing_person is not None:
            return f"Person with name {existing_person[1].title()} already exists."

        cursor.execute(
            "INSERT INTO phonebook (name, number) VALUES (%s, %s)",
            (normalized_name, number)
        )

        return f"Person {name.strip().title()} added to Phonebook successfully."
    finally:
        cursor.close()
        connection.close()


def update_person(name, number):
    """Update an existing phonebook record."""
    connection = get_connection()
    cursor = connection.cursor()

    normalized_name = name.strip().lower()

    try:
        cursor.execute(
            "SELECT id FROM phonebook WHERE LOWER(name) = %s",
            (normalized_name,)
        )

        person = cursor.fetchone()

        if person is None:
            return f"Person with name {name.strip().title()} does not exist."

        cursor.execute(
            "UPDATE phonebook SET number = %s WHERE id = %s",
            (number, person[0])
        )

        return f"Phone record of {name.strip().title()} is updated successfully."
    finally:
        cursor.close()
        connection.close()


def delete_person(name):
    """Delete a phonebook record."""
    connection = get_connection()
    cursor = connection.cursor()

    normalized_name = name.strip().lower()

    try:
        cursor.execute(
            "SELECT id FROM phonebook WHERE LOWER(name) = %s",
            (normalized_name,)
        )

        person = cursor.fetchone()

        if person is None:
            return f"Person with name {name.strip().title()} does not exist, no need to delete."

        cursor.execute(
            "DELETE FROM phonebook WHERE id = %s",
            (person[0],)
        )

        return f"Phone record of {name.strip().title()} is deleted successfully."
    finally:
        cursor.close()
        connection.close()


@app.route("/", methods=["GET", "POST"])
def find_records():
    if request.method == "POST":
        keyword = request.form.get("username", "")
        persons_app = find_persons(keyword)

        return render_template(
            "index.html",
            persons_html=persons_app,
            keyword=keyword,
            show_result=True,
            developer_name=DEVELOPER_NAME
        )

    return render_template(
        "index.html",
        show_result=False,
        developer_name=DEVELOPER_NAME
    )


@app.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        phone_number = request.form.get("phonenumber", "").strip()

        if not name:
            message = "Invalid input: Name cannot be empty."
        elif name.isdecimal():
            message = "Invalid input: Name of person should be text."
        elif not phone_number:
            message = "Invalid input: Phone number cannot be empty."
        elif not phone_number.isdecimal():
            message = "Invalid input: Phone number should be in numeric format."
        else:
            result_app = insert_person(name, phone_number)

            return render_template(
                "add-update.html",
                show_result=True,
                result_html=result_app,
                not_valid=False,
                action_name="save",
                developer_name=DEVELOPER_NAME
            )

        return render_template(
            "add-update.html",
            not_valid=True,
            message=message,
            show_result=False,
            action_name="save",
            developer_name=DEVELOPER_NAME
        )

    return render_template(
        "add-update.html",
        show_result=False,
        not_valid=False,
        action_name="save",
        developer_name=DEVELOPER_NAME
    )


@app.route("/update", methods=["GET", "POST"])
def update_record():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        phone_number = request.form.get("phonenumber", "").strip()

        if not name:
            message = "Invalid input: Name cannot be empty."
        elif not phone_number:
            message = "Invalid input: Phone number cannot be empty."
        elif not phone_number.isdecimal():
            message = "Invalid input: Phone number should be in numeric format."
        else:
            result_app = update_person(name, phone_number)

            return render_template(
                "add-update.html",
                show_result=True,
                result_html=result_app,
                not_valid=False,
                action_name="update",
                developer_name=DEVELOPER_NAME
            )

        return render_template(
            "add-update.html",
            not_valid=True,
            message=message,
            show_result=False,
            action_name="update",
            developer_name=DEVELOPER_NAME
        )

    return render_template(
        "add-update.html",
        show_result=False,
        not_valid=False,
        action_name="update",
        developer_name=DEVELOPER_NAME
    )


@app.route("/delete", methods=["GET", "POST"])
def delete_record():
    if request.method == "POST":
        name = request.form.get("username", "").strip()

        if not name:
            return render_template(
                "delete.html",
                not_valid=True,
                message="Invalid input: Name cannot be empty.",
                show_result=False,
                developer_name=DEVELOPER_NAME
            )

        result_app = delete_person(name)

        return render_template(
            "delete.html",
            show_result=True,
            result_html=result_app,
            not_valid=False,
            developer_name=DEVELOPER_NAME
        )

    return render_template(
        "delete.html",
        show_result=False,
        not_valid=False,
        developer_name=DEVELOPER_NAME
    )


if __name__ == "__main__":
    init_phonebook_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
