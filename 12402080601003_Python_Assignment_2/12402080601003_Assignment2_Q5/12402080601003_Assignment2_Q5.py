# Assignment 2
# Question 5 - Tkinter Contact Manager with MySQL Backend

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re


# Change this to your MySQL root password
DB_PASSWORD = "#$%niketp2811"


def create_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS college")
    cursor.close()
    connection.close()


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD,
        database="college"
    )


def setup_database():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            phone VARCHAR(20),
            category VARCHAR(50),
            notes TEXT
        )
    """)

    # MySQL does not support CREATE INDEX IF NOT EXISTS.
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.statistics
        WHERE table_schema = 'college'
          AND table_name = 'Contact'
          AND index_name = 'idx_contact_name'
    """)

    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "CREATE INDEX idx_contact_name ON Contact(name)"
        )

    connection.commit()
    cursor.close()
    connection.close()


def valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None


def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    category_combo.set("Personal")
    notes_entry.delete("1.0", tk.END)


def refresh_contacts(search_text=""):
    for item in contact_table.get_children():
        contact_table.delete(item)

    connection = connect_db()
    cursor = connection.cursor()

    try:
        query = """
            SELECT id, name, email, phone, category, notes
            FROM Contact
            WHERE name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
            ORDER BY name
        """

        value = "%" + search_text + "%"
        cursor.execute(query, (value, value, value))

        for row in cursor.fetchall():
            contact_table.insert("", tk.END, values=row)

    finally:
        cursor.close()
        connection.close()


def add_contact():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_combo.get()
    notes = notes_entry.get("1.0", tk.END).strip()

    if not name or not email:
        messagebox.showerror(
            "Error", "Name and email are required."
        )
        return

    if not valid_email(email):
        messagebox.showerror(
            "Error", "Enter a valid email address."
        )
        return

    connection = None
    cursor = None

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Contact
                (name, email, phone, category, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, category, notes))

        connection.commit()
        refresh_contacts()
        clear_fields()

        messagebox.showinfo(
            "Success", "Contact added successfully."
        )

    except mysql.connector.IntegrityError:
        messagebox.showerror(
            "Error", "Email already exists."
        )

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def update_contact():
    selected = contact_table.selection()

    if not selected:
        messagebox.showerror(
            "Error", "Select a contact first."
        )
        return

    contact_id = contact_table.item(selected[0])["values"][0]
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_combo.get()
    notes = notes_entry.get("1.0", tk.END).strip()

    if not name or not email or not valid_email(email):
        messagebox.showerror(
            "Error", "Enter a valid name and email."
        )
        return

    connection = None
    cursor = None

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Contact
            SET name=%s, email=%s, phone=%s,
                category=%s, notes=%s
            WHERE id=%s
        """, (name, email, phone, category, notes, contact_id))

        connection.commit()
        refresh_contacts()

        messagebox.showinfo(
            "Success", "Contact updated successfully."
        )

    except mysql.connector.IntegrityError:
        messagebox.showerror(
            "Error", "Email already belongs to another contact."
        )

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_contact():
    selected = contact_table.selection()

    if not selected:
        messagebox.showerror(
            "Error", "Select a contact first."
        )
        return

    contact_id = contact_table.item(selected[0])["values"][0]

    if not messagebox.askyesno(
        "Confirm", "Delete this contact?"
    ):
        return

    connection = None
    cursor = None

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM Contact WHERE id=%s",
            (contact_id,)
        )

        connection.commit()
        refresh_contacts()
        clear_fields()

        messagebox.showinfo(
            "Success", "Contact deleted successfully."
        )

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def search_contacts():
    try:
        refresh_contacts(search_entry.get().strip())
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))


def select_contact(event):
    selected = contact_table.selection()

    if not selected:
        return

    values = contact_table.item(selected[0])["values"]

    clear_fields()

    name_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    phone_entry.insert(0, values[3] or "")
    category_combo.set(values[4] or "Personal")
    notes_entry.insert("1.0", values[5] or "")


def main():
    global root
    global name_entry, email_entry, phone_entry
    global category_combo, notes_entry, search_entry
    global contact_table

    try:
        create_database()
        setup_database()

    except mysql.connector.Error as error:
        error_root = tk.Tk()
        error_root.withdraw()
        messagebox.showerror(
            "MySQL Connection Error",
            "Could not initialize the database.\n\n"
            + str(error)
        )
        error_root.destroy()
        return

    root = tk.Tk()
    root.title("Contact Manager")
    root.geometry("950x600")

    form = ttk.LabelFrame(
        root, text="Contact Details", padding=10
    )
    form.pack(fill="x", padx=10, pady=10)

    ttk.Label(form, text="Name").grid(
        row=0, column=0, sticky="w"
    )
    name_entry = ttk.Entry(form, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form, text="Email").grid(
        row=0, column=2, sticky="w"
    )
    email_entry = ttk.Entry(form, width=30)
    email_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(form, text="Phone").grid(
        row=1, column=0, sticky="w"
    )
    phone_entry = ttk.Entry(form, width=30)
    phone_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form, text="Category").grid(
        row=1, column=2, sticky="w"
    )
    category_combo = ttk.Combobox(
        form,
        values=["Personal", "Faculty", "Friend", "Work"],
        state="readonly",
        width=27
    )
    category_combo.grid(row=1, column=3, padx=5, pady=5)
    category_combo.set("Personal")

    ttk.Label(form, text="Notes").grid(
        row=2, column=0, sticky="nw"
    )
    notes_entry = tk.Text(form, width=65, height=3)
    notes_entry.grid(
        row=2, column=1, columnspan=3, padx=5, pady=5
    )

    buttons = ttk.Frame(root)
    buttons.pack(pady=5)

    ttk.Button(
        buttons, text="Add", command=add_contact
    ).pack(side="left", padx=5)

    ttk.Button(
        buttons, text="Update", command=update_contact
    ).pack(side="left", padx=5)

    ttk.Button(
        buttons, text="Delete", command=delete_contact
    ).pack(side="left", padx=5)

    ttk.Button(
        buttons, text="Clear", command=clear_fields
    ).pack(side="left", padx=5)

    search_frame = ttk.Frame(root)
    search_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(
        search_frame, text="Search name/email/phone:"
    ).pack(side="left")

    search_entry = ttk.Entry(search_frame, width=35)
    search_entry.pack(side="left", padx=5)

    ttk.Button(
        search_frame, text="Search", command=search_contacts
    ).pack(side="left")

    ttk.Button(
        search_frame,
        text="Show All",
        command=lambda: refresh_contacts()
    ).pack(side="left", padx=5)

    columns = (
        "ID", "Name", "Email", "Phone", "Category", "Notes"
    )

    contact_table = ttk.Treeview(
        root, columns=columns, show="headings"
    )

    for column in columns:
        contact_table.heading(column, text=column)

    contact_table.column("ID", width=45)
    contact_table.column("Name", width=130)
    contact_table.column("Email", width=190)
    contact_table.column("Phone", width=110)
    contact_table.column("Category", width=100)
    contact_table.column("Notes", width=220)

    contact_table.pack(
        fill="both", expand=True, padx=10, pady=10
    )

    contact_table.bind(
        "<<TreeviewSelect>>", select_contact
    )

    try:
        refresh_contacts()
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))

    root.mainloop()


if __name__ == "__main__":
    main()
