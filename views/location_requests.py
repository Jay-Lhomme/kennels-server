import sqlite3
import json
from models import Location
from models import Animal
from models import Employee

LOCATIONS = [
    {"id": 1, "name": "Nashville North", "address": "8422 Johnson Pike"},
    {"id": 2, "name": "Nashville South", "address": "209 Emory Drive"},
]


def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """      
          SELECT
            l.id,
            l.name,
            l.address,
            e.name employee_name,
            e.address employee_address,
            e.location_id employee_location_id,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status,
            a.location_id animal_location_id,
            a.customer_id animal_customer_id
            
        FROM Location l
        JOIN Employee e, Animal a
            ON l.id = e.location_id AND l.id = a.location_id
        """
        )

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a Location instance from the current row
            location = Location(row["id"], row["name"], row["address"])

            # Create a Employee instance from the current row
            employee = Employee(row["id"], row["employee_name"],
                                row["employee_address"], row["employee_location_id"])

            # Create a Animal instance from the current row
            animal = Animal(row["id"],
                            row["animal_name"],
                            row["animal_breed"],
                            row["animal_status"],
                            row["animal_location_id"],
                            row["animal_customer_id"])

            # Create a dictionary representation of the employee without the address
            employee__dict__ = {
                "name": employee.name,
                "address": employee.address
            }
            location.employee = employee__dict__

            # Create a dictionary representation of the animal without the address
            animal__dict__ = {
                "name": animal.name,
                "breed": animal.breed,
                "status": animal.status,
                "customer_id": animal.customer_id
            }
            location.animal = animal__dict__

            locations.append(
                location.__dict__
            )  # see the notes below for an explanation on this line of code.

    return locations


# Function with a single parameter
def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
          SELECT
            l.id,
            l.name,
            l.address,
            e.name employee_name,
            e.address employee_address,
            e.location_id employee_location_id,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status,
            a.location_id animal_location_id,
            a.customer_id animal_customer_id
            
        FROM Location l
        JOIN Employee e, Animal a
            ON l.id = e.location_id AND l.id = a.location_id
        WHERE l.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an location instance from the current row
        location = Location(data["id"], data["name"], data["address"])

        # Create a Employee instance from the current row
        employee = Employee(data["id"],
                            data["employee_name"],
                            data["employee_address"],
                            data["employee_location_id"])

        # Create a Animal instance from the current data
        animal = Animal(data["id"],
                        data["animal_name"],
                        data["animal_breed"],
                        data["animal_status"],
                        data["animal_location_id"],
                        data["animal_customer_id"])

        # Create a dictionary representation of the employee without the address
        employee__dict__ = {
            "name": employee.name,
            "address": employee.address
        }
        location.employee = employee__dict__

        # Create a dictionary representation of the animal without the address
        animal__dict__ = {
            "name": animal.name,
            "breed": animal.breed,
            "status": animal.status,
            "customer_id": animal.customer_id
        }
        location.animal = animal__dict__

        return location.__dict__


def create_location(location):
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the location dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location


def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM location
        WHERE id = ?
        """,
            (id,),
        )


def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Location
            SET
                name = ?,
                address = ?,
        WHERE id = ?
        """,
            (
                new_location["name"],
                new_location["address"],
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
