# Assignment 1
# Question 10 - Tkinter Assignment Tracker with File Persistence

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os


DATA_FILE = "assignments.json"


# Load saved data
def load_data():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


# Save data to JSON
def save_data():

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    except OSError:
        messagebox.showerror(
            "Error",
            "Could not save data."
        )


# Validate student details
def validate_student():

    enrollment = enrollment_entry.get().strip()
    name = name_entry.get().strip()

    if not enrollment:
        messagebox.showerror(
            "Invalid Input",
            "Enter enrollment number."
        )
        return False

    if not enrollment.isdigit():
        messagebox.showerror(
            "Invalid Input",
            "Enrollment number must contain digits only."
        )
        return False

    if not name:
        messagebox.showerror(
            "Invalid Input",
            "Enter student name."
        )
        return False

    return True


# Add a student
def add_student():

    if not validate_student():
        return

    enrollment = enrollment_entry.get().strip()
    name = name_entry.get().strip()

    for record in records:

        if record["enrollment"] == enrollment:
            messagebox.showwarning(
                "Already Exists",
                "Student already exists."
            )
            return

    records.append(
        {
            "enrollment": enrollment,
            "name": name,
            "assignment": "",
            "status": "Pending",
            "marks": "",
            "remarks": ""
        }
    )

    save_data()
    refresh_table()

    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )


# Add assignment
def add_assignment():

    enrollment = enrollment_entry.get().strip()
    assignment = assignment_entry.get().strip()

    if not enrollment:
        messagebox.showerror(
            "Invalid Input",
            "Enter enrollment number."
        )
        return

    if not assignment:
        messagebox.showerror(
            "Invalid Input",
            "Enter assignment name."
        )
        return

    for record in records:

        if record["enrollment"] == enrollment:

            record["assignment"] = assignment
            record["status"] = "Pending"

            save_data()
            refresh_table()

            messagebox.showinfo(
                "Success",
                "Assignment added successfully."
            )
            return

    messagebox.showerror(
        "Not Found",
        "Student not found."
    )


# Update marks
def update_marks():

    enrollment = enrollment_entry.get().strip()
    assignment = assignment_entry.get().strip()
    marks_text = marks_entry.get().strip()
    remarks = remarks_entry.get().strip()

    if not enrollment:
        messagebox.showerror(
            "Invalid Input",
            "Enter enrollment number."
        )
        return

    if not assignment:
        messagebox.showerror(
            "Invalid Input",
            "Enter assignment name."
        )
        return

    if not marks_text.isdigit():
        messagebox.showerror(
            "Invalid Input",
            "Marks must be a number."
        )
        return

    marks = int(marks_text)

    if marks < 0 or marks > 20:
        messagebox.showerror(
            "Invalid Input",
            "Marks must be between 0 and 20."
        )
        return

    for record in records:

        if (
            record["enrollment"] == enrollment
            and record["assignment"] == assignment
        ):

            record["marks"] = marks
            record["status"] = "Completed"
            record["remarks"] = remarks

            save_data()
            refresh_table()

            messagebox.showinfo(
                "Success",
                "Marks updated successfully."
            )
            return

    messagebox.showerror(
        "Not Found",
        "Student or assignment not found."
    )


# Filter records
def filter_records():

    status = status_var.get()

    if status == "All":
        filtered = records

    else:
        filtered = [
            record
            for record in records
            if record["status"] == status
        ]

    display_records(filtered)


# Display records in table
def display_records(data):

    for item in table.get_children():
        table.delete(item)

    for record in data:

        table.insert(
            "",
            "end",
            values=(
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"]
            )
        )


# Refresh table
def refresh_table():

    filter_records()


# Export CSV report
def export_csv():

    if not records:
        messagebox.showwarning(
            "No Data",
            "There is no data to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[
            ("CSV Files", "*.csv")
        ]
    )

    if not file_path:
        return

    try:

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Enrollment",
                    "Name",
                    "Assignment",
                    "Status",
                    "Marks",
                    "Remarks"
                ]
            )

            for record in records:

                writer.writerow(
                    [
                        record["enrollment"],
                        record["name"],
                        record["assignment"],
                        record["status"],
                        record["marks"],
                        record["remarks"]
                    ]
                )

        messagebox.showinfo(
            "Export Complete",
            "CSV report exported successfully."
        )

    except OSError:

        messagebox.showerror(
            "Error",
            "Could not export CSV file."
        )


# Clear input fields
def clear_fields():

    enrollment_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    assignment_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    remarks_entry.delete(0, tk.END)


# Main window
root = tk.Tk()

root.title(
    "Assignment Tracker"
)

root.geometry(
    "1000x600"
)

root.resizable(
    True,
    True
)


# Store application data
records = load_data()


# Title
title_label = tk.Label(
    root,
    text="Student Assignment Tracker",
    font=("Arial", 20, "bold")
)

title_label.pack(
    pady=10
)


# Input frame
input_frame = tk.Frame(root)

input_frame.pack(
    padx=10,
    pady=5,
    fill="x"
)


# Enrollment
tk.Label(
    input_frame,
    text="Enrollment"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

enrollment_entry = tk.Entry(
    input_frame,
    width=20
)

enrollment_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# Name
tk.Label(
    input_frame,
    text="Name"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)

name_entry = tk.Entry(
    input_frame,
    width=20
)

name_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# Assignment
tk.Label(
    input_frame,
    text="Assignment"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

assignment_entry = tk.Entry(
    input_frame,
    width=20
)

assignment_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# Marks
tk.Label(
    input_frame,
    text="Marks / 20"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)

marks_entry = tk.Entry(
    input_frame,
    width=20
)

marks_entry.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)


# Remarks
tk.Label(
    input_frame,
    text="Remarks"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

remarks_entry = tk.Entry(
    input_frame,
    width=20
)

remarks_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


# Buttons
button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)

tk.Button(
    button_frame,
    text="Add Student",
    command=add_student
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    button_frame,
    text="Add Assignment",
    command=add_assignment
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    button_frame,
    text="Update Marks",
    command=update_marks
).grid(
    row=0,
    column=2,
    padx=5
)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)

tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv
).grid(
    row=0,
    column=4,
    padx=5
)


# Filter
filter_frame = tk.Frame(root)

filter_frame.pack(
    pady=5
)

tk.Label(
    filter_frame,
    text="Filter:"
).pack(
    side="left",
    padx=5
)

status_var = tk.StringVar(
    value="All"
)

status_menu = ttk.Combobox(
    filter_frame,
    textvariable=status_var,
    values=[
        "All",
        "Pending",
        "Completed"
    ],
    state="readonly",
    width=15
)

status_menu.pack(
    side="left",
    padx=5
)

status_menu.bind(
    "<<ComboboxSelected>>",
    lambda event: filter_records()
)


# Table
table_frame = tk.Frame(root)

table_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

columns = (
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Remarks"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=140
    )

table.pack(
    fill="both",
    expand=True
)


# Display saved data
refresh_table()


# Start application
root.mainloop()