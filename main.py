from tkinter import *
from tkinter import messagebox
import pyperclip
from PIL import Image, ImageTk
from password import PassWord
import requests
from password_hash import Hash
import mysql.connector 
from dotenv import load_dotenv
import os

load_dotenv()

db = mysql.connector.connect(
    user = os.getenv("USER"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"),
    database = "password"
)

cursor = db.cursor()
hash = Hash()

def add_delete():
    website = website_entry.get()
    email_username = Email_username_entry.get()
    password = password_entry.get()
    password = hash.pass_encrypt(password)
    
    if website == "" or email_username == "" or password == "":
        messagebox.showwarning(title="Missing required data", message="Please fill up all the required field!!",
                               icon=messagebox.ERROR)
    else:
        ok_cancel = messagebox.askokcancel(title=website, message=f"These are the details entered:\n"
                                                                  f"Email: {email_username}\n"
                                                                  f"Password: {password_entry.get()}\n"
                                                                  f"Is it ok to save?", icon=messagebox.QUESTION)
        if ok_cancel:
            cursor.execute('''INSERT INTO 
                          user(website,username,user_password)
                          VALUES(%s,%s,%s)''',(website,email_username,password))
            db.commit()


def search():
    user_info = {
        "usernames": [],
        "passwords": [],
    }
    message = ""
    site_name = website_entry.get()
    cursor.execute("SELECT * FROM user WHERE website = %s",(site_name,))
    data = cursor.fetchall()

    for i in range(len(data)):
        user_info["usernames"].append(data[i][2])
        user_info["passwords"].append(hash.pass_decrypt(data[i][1]))

    if not user_info["usernames"] or not user_info["passwords"]:
        messagebox.showerror(title="Error!", message="No saved Username or Password found.\n"
                                                     "Please check the website name again")
    else:
        for i in range(len(user_info["passwords"])):
            message += (f"Email/Username: {user_info["usernames"][i]}\nPassword: {user_info["passwords"][i]}\n"
                        f"-------------------------------------------\n")
            pyperclip.copy(user_info["passwords"][i])

        messagebox.showinfo(title=website_entry.get(), message=message)


def create_password():
    new_password = PassWord().password
    password_entry.delete(0, END)
    password_entry.insert(0, f"{new_password}")
    pyperclip.copy(new_password)


window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=40)

image_1 = Image.open("password.png")
resized_image = image_1.resize((200, 200))
pass_image = ImageTk.PhotoImage(resized_image)

canvas = Canvas(width=220, height=240)
canvas.create_image(110, 110, image=pass_image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", font=("Courier New", 12))
website_label.config(padx=10, pady=3)
website_label.grid(row=1, column=0)

website_entry = Entry(width=37)
website_entry.focus()
website_entry.grid(row=1, column=1)

search_button = Button(width=16, text="Search", bg="White", font=("Verdana", 9),
                       command=search)
search_button.grid(row=1, column=2, padx=5)

Email_username_label = Label(text="Email/Username:", font=("Courier New", 12))
Email_username_label.config(padx=20, pady=5)
Email_username_label.grid(row=2, column=0)

Email_username_entry = Entry(width=62)
Email_username_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:", font=("Courier New", 12))
password_label.config(padx=10, pady=5)
password_label.grid(row=3, column=0)

password_entry = Entry(width=37)
password_entry.grid(row=3, column=1, padx=5)

Generate_password_button = Button(width=16, text="Generate Password", bg="White", font=("Verdana", 9),
                                  command=create_password)
Generate_password_button.grid(row=3, column=2, padx=5)

add_button = Button(text="Add", width=46, bg="White", font=("Verdana", 10), command=add_delete)
add_button.grid(row=4, column=1, columnspan=2, pady=5)

window.mainloop()
