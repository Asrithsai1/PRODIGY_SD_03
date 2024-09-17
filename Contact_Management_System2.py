import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

CONTACTS_FILE = 'contacts.txt'

# Function to load contacts from the file
def load_contacts():
    contacts = {}
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            for line in file:
                name, phone, email = line.strip().split(',')
                contacts[name] = {'phone': phone, 'email': email}
    return contacts

# Function to save contacts to the file
def save_contacts():
    with open(CONTACTS_FILE, 'w') as file:
        for name, info in contacts.items():
            file.write(f"{name},{info['phone']},{info['email']}\n")

# Function to clear input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Function to validate inputs
def validate_inputs(name, phone, email):
    if name == "" or not phone.isdigit() or len(phone) != 10 or "@" not in email:
        return False
    return True

# Function to add a new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if not validate_inputs(name, phone, email):
        messagebox.showerror("Invalid Input", "Please enter valid details.")
        return

    if name in contacts:
        messagebox.showerror("Duplicate Contact", "A contact with this name already exists.")
    else:
        contacts[name] = {'phone': phone, 'email': email}
        save_contacts()
        update_contact_list()
        messagebox.showinfo("Success", f"Contact '{name}' added successfully.")
        clear_entries()

# Function to update the contact list display
def update_contact_list():
    for widget in contact_frame.winfo_children():
        widget.destroy()

    for name, info in contacts.items():
        card = tk.Frame(contact_frame, bg='#ffffff', padx=10, pady=10, relief='solid', bd=1)
        card.pack(pady=5, fill=tk.X)

        name_label = tk.Label(card, text=f"{name}", font=("Helvetica", 14, "bold"), bg='#ffffff')
        name_label.grid(row=0, column=0, padx=10, sticky="w")

        phone_label = tk.Label(card, text=f"Phone: {info['phone']}", bg='#ffffff')
        phone_label.grid(row=1, column=0, padx=10, sticky="w")

        email_label = tk.Label(card, text=f"Email: {info['email']}", bg='#ffffff')
        email_label.grid(row=2, column=0, padx=10, sticky="w")

        view_btn = tk.Button(card, text="View", command=lambda n=name: view_contact(n), bg='#00b0ff', fg='white')
        view_btn.grid(row=0, column=1, padx=10)

        edit_btn = tk.Button(card, text="Edit", command=lambda n=name: edit_contact(n), bg='#ff9800', fg='white')
        edit_btn.grid(row=0, column=2, padx=10)

        delete_btn = tk.Button(card, text="Delete", command=lambda n=name: delete_contact(n), bg='#f44336', fg='white')
        delete_btn.grid(row=0, column=3, padx=10)

# Function to view a contact
def view_contact(name):
    contact = contacts[name]
    messagebox.showinfo("Contact Info", f"Name: {name}\nPhone: {contact['phone']}\nEmail: {contact['email']}")

# Function to edit a contact
def edit_contact(name):
    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Contact")
    edit_window.geometry("300x200")
    contact = contacts[name]

    tk.Label(edit_window, text="Edit Contact", font=("Helvetica", 16, "bold")).pack(pady=10)

    name_label = tk.Label(edit_window, text="Name:")
    name_label.pack()
    name_entry_edit = tk.Entry(edit_window)
    name_entry_edit.pack()
    name_entry_edit.insert(0, name)

    phone_label = tk.Label(edit_window, text="Phone:")
    phone_label.pack()
    phone_entry_edit = tk.Entry(edit_window)
    phone_entry_edit.pack()
    phone_entry_edit.insert(0, contact['phone'])

    email_label = tk.Label(edit_window, text="Email:")
    email_label.pack()
    email_entry_edit = tk.Entry(edit_window)
    email_entry_edit.pack()
    email_entry_edit.insert(0, contact['email'])

    def save_edit():
        new_name = name_entry_edit.get().strip()
        new_phone = phone_entry_edit.get().strip()
        new_email = email_entry_edit.get().strip()

        if not validate_inputs(new_name, new_phone, new_email):
            messagebox.showerror("Invalid Input", "Please enter valid details.")
            return

        del contacts[name]  # Delete old contact
        contacts[new_name] = {'phone': new_phone, 'email': new_email}  # Add updated contact
        save_contacts()
        update_contact_list()
        edit_window.destroy()

    save_btn = tk.Button(edit_window, text="Save Changes", command=save_edit, bg='#4caf50', fg='white')
    save_btn.pack(pady=10)

# Function to delete a contact
def delete_contact(name):
    if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete '{name}'?"):
        del contacts[name]
        save_contacts()
        update_contact_list()

# Initial setup
contacts = load_contacts()

# Create the main window
window = tk.Tk()
window.title("Interactive Contact Management")
window.geometry("500x600")
window.config(bg='#e0f7fa')

# Title label
title_label = tk.Label(window, text="Contact Management", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#004d40')
title_label.pack(pady=10)

# Input frame
input_frame = tk.Frame(window, bg='#e0f7fa')
input_frame.pack(pady=10)

# Name input
name_label = tk.Label(input_frame, text="Name", font=("Helvetica", 12), bg='#e0f7fa', fg='#004d40')
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=25, bg='#ffffff')
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Phone input
phone_label = tk.Label(input_frame, text="Phone", font=("Helvetica", 12), bg='#e0f7fa', fg='#004d40')
phone_label.grid(row=1, column=0, padx=10, pady=5)
phone_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=25, bg='#ffffff')
phone_entry.grid(row=1, column=1, padx=10, pady=5)

# Email input
email_label = tk.Label(input_frame, text="Email", font=("Helvetica", 12), bg='#e0f7fa', fg='#004d40')
email_label.grid(row=2, column=0, padx=10, pady=5)
email_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=25, bg='#ffffff')
email_entry.grid(row=2, column=1, padx=10, pady=5)

# Add Contact button
add_button = tk.Button(window, text="Add Contact", font=("Helvetica", 12), command=add_contact, bg='#4caf50', fg='white')
add_button.pack(pady=10)

# Contact list frame
contact_frame = tk.Frame(window, bg='#e0f7fa')
contact_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Update the contact list when starting the application
update_contact_list()

# Start the Tkinter event loop
window.mainloop()
