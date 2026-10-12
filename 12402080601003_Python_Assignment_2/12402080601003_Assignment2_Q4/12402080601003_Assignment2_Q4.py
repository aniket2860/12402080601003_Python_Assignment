# Assignment 2
# Question 4 - SQL Join Query Builder and Validator

import re
import json
import mysql.connector


ALLOWED_COLUMNS = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.course_name",
    "registration.course_id": "r.course_id"
}


def main():
    connection = None
    cursor = None

    try:
        host = input("Host: ")
        user = input("Username: ")
        password = input("Password: ")
        database = input("Database: ")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        config = json.loads(input("Query JSON: "))

        columns = config.get("columns", [])
        filters = config.get("where", {})
        order = config.get("order", "student.spi DESC")
        limit = config.get("limit", 10)

        if not columns or not isinstance(columns, list):
            raise ValueError("Invalid columns")

        selected = []

        for column in columns:
            if column not in ALLOWED_COLUMNS:
                raise ValueError("Invalid column: " + str(column))
            selected.append(ALLOWED_COLUMNS[column])

        if not isinstance(limit, int) or not 1 <= limit <= 1000:
            raise ValueError("Invalid limit")

        order_parts = order.split()

        if len(order_parts) != 2:
            raise ValueError("Invalid ORDER BY")

        order_column, direction = order_parts
        direction = direction.upper()

        if order_column not in ALLOWED_COLUMNS:
            raise ValueError("Invalid order column")

        if direction not in ("ASC", "DESC"):
            raise ValueError("Invalid sort direction")

        conditions = []
        parameters = []

        for column, value in filters.items():
            if column not in ALLOWED_COLUMNS:
                raise ValueError("Invalid filter column")

            if isinstance(value, dict):
                for operator, filter_value in value.items():
                    if operator not in ("=", ">", "<", ">=", "<=", "LIKE"):
                        raise ValueError("Invalid operator")

                    conditions.append(
                        ALLOWED_COLUMNS[column] + " " + operator + " %s"
                    )
                    parameters.append(filter_value)
            else:
                conditions.append(ALLOWED_COLUMNS[column] + " = %s")
                parameters.append(value)

        query = (
            "SELECT " + ", ".join(selected) +
            " FROM Student s " +
            "JOIN CourseRegistration r ON s.student_id = r.student_id " +
            "JOIN Course c ON r.course_id = c.course_id"
        )

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += (
            " ORDER BY " + ALLOWED_COLUMNS[order_column] +
            " " + direction +
            " LIMIT %s"
        )
        parameters.append(limit)

        print("SQL_OK")
        print(query)
        print("Parameters:", parameters)

        cursor.execute(query, parameters)

        for row in cursor.fetchall():
            print(*row)

    except (ValueError, KeyError, json.JSONDecodeError) as error:
        print("INVALID:", error)

    except mysql.connector.Error as error:
        print("DATABASE_ERROR:", error)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()