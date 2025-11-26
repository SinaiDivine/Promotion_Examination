# Name: MOSES PHIRI
# Student number: 2023053332
# Intake: Jan 2024

📘 ROCKVIEW Library Management System

A simple and user-friendly Library Management System built using KivyMD and Python, with support for adding books, borrowing, returning, searching, and deleting records. All data is stored in a local JSON database.

🚀 Features

Add new books (ID, Title, Author, Year)

View all books in a clean scrollable list

Search books by ID, Title, or Author

Borrow and return books

Delete book records

Data saved automatically using JSON

Smooth UI using KivyMD components

Fully mobile-friendly (Android compatible)

💻 Technologies Used

Python 3

Kivy

KivyMD

JSON for data storage

📂 Project Structure

project/
│── main.py
│── library_records.json
│── README.md

📦 How to Run

1. Install dependencies

pip install kivy kivymd

2. Run the app

python main.py

🗄️ Data Storage (library_records.json)

Your book records are saved in:

library_records.json

Each book record looks like:

{
    "book_id": "214",
    "title": "Python programming",
    "author": "Mr Chilengwe",
    "year_published": 2025,
    "availability": "Available",
    "borrower_name": "",
    "date_borrowed": ""
}

📱 UI Screens

The system comes with 3 main screens:

✔ Book List Screen

View all books

Search books

Borrow/return status visible

✔ Add Book Screen

Add new book entries

Validation for duplicate IDs

✔ Transactions Screen

Borrow book

Return book

Delete book

🧩 Main Code Reference

The main logic includes:

Loading/saving JSON data

Validating inputs

Borrow/return logic

Search engine

Dynamic KivyMD UI updates

👨‍💻 Developer

Powered by Sinai Divine

📝 License

This project is for educational purposes and can be modified freely
