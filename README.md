# Pharmacy Inventory System

A web-based Pharmacy Inventory System developed using Python, Flask, SQLite, HTML, and CSS. This application helps pharmacy staff manage medicines, monitor stock levels, and identify expired medicines through a simple dashboard.

## Project Preview

The system provides a dashboard where users can view inventory statistics and access different medicine management features.

## Features

- Add new medicines to the inventory
- View all available medicines
- Search medicines by name
- Edit existing medicine details
- Delete medicines from the inventory
- Track medicine quantity
- Identify low-stock medicines
- Identify expired medicines
- Display total medicine count on the dashboard
- Store medicine details using SQLite database
- Responsive and user-friendly interface

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2 Templates
- Git and GitHub

## Medicine Details Stored

Each medicine record contains:

- Medicine ID
- Medicine Name
- Category
- Manufacturer
- Batch Number
- Quantity
- Price
- Expiry Date

## Project Structure

```text
pharmacy-inventory-system/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   ├── add_medicine.html
│   ├── medicines.html
│   ├── edit_medicine.html
│   ├── low_stock.html
│   └── expired.html
│
└── static/
    └── css/
        └── style.css
