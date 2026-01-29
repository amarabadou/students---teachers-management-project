import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

def login_teacher():
    email = email_entry.get()
    password = password_entry.get()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="", # username
            password="", # your DB password
            database="" # youe DB name
        )
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM teachers WHERE email=%s AND password=%s",
            (email, password)
        )
        result = cursor.fetchone()

        if result:
            root.destroy()
            subprocess.Popen([sys.executable, "TeacherPannel.py"])
        else:
            messagebox.showerror("Error", "Incorrect email or password!")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


root = tk.Tk()
root.title("Teacher Login")
root.geometry("900x600")
root.resizable(False, False)
root.configure(bg="#34495E")

tk.Label(
    root,
    text="Teacher Login",
    font=("Arial", 28, "bold"),
    bg="#34495E",
    fg="white"
).pack(pady=40)

tk.Label(
    root,
    text="Email:",
    font=("Arial", 18),
    bg="#34495E",
    fg="white"
).pack(pady=10)

email_entry = tk.Entry(root, font=("Arial", 16), width=30)
email_entry.pack(pady=5)

tk.Label(
    root,
    text="Password:",
    font=("Arial", 18),
    bg="#34495E",
    fg="white"
).pack(pady=10)

password_entry = tk.Entry(root, font=("Arial", 16), show="*", width=30)
password_entry.pack(pady=5)

tk.Button(
    root,
    text="Login",
    font=("Arial", 18, "bold"),
    bg="#2ECC71",
    fg="white",
    width=25,
    height=2,
    command=login_teacher
).pack(pady=30)

root.mainloop()