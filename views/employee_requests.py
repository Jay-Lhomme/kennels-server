import sqlite3
import json
from models import Employee
from models import Location

EMPLOYEES = [{"id": 1, "name": "Jenna Solis"}]


def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name
            
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id
        """
        )

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database

        for row in dataset:

            # Create an employee instance from the current row
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"]
            )

            # Create a Location instance from the current row
            location = Location(
                row["id"], row["location_name"], row["address"]
            )

            # Create a dictionary representation of the location without the address
            location__dict__ = {
                "id": location.id,
                "name": location.name
            }
            employee.location = location__dict__

            # Add the dictionary representation of the employee to the list
            employees.append(
                employee.__dict__
            )

    return employees


# Function with a single parameter
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(
            data["id"], data["name"], data["address"], data["location_id"]
        )

        return employee.__dict__


def create_employee(employee):
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee


def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM employee
        WHERE id = ?
        """,
            (id,),
        )


def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Employee
            SET
                name = ?,
                address = ?,
                location_id = ?,
        WHERE id = ?
        """,
            (
                new_employee["name"],
                new_employee["address"],
                new_employee["location_id"],
                id,
            ),
        )

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_employee_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """,
            (location_id,),
        )

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"]
            )
            employees.append(employee.__dict__)

    return employees
