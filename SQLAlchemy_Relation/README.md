# Flask One-to-One Relationship Demo App

This project demonstrates a **One-to-One relationship** using **Flask** and **Flask-SQLAlchemy**.  
It is a beginner-friendly backend application that shows how two database tables (`User` and `Profile`) are linked where **each user has exactly one profile**.

The app exposes simple REST-style endpoints that can be accessed directly from a web browser.

---

## 🚀 Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite (local database)

---

## 📌 Project Objective

- Understand **One-to-One relationships** in SQLAlchemy
- Learn how to define:
  - `db.relationship()`
  - `db.ForeignKey()`
  - `uselist=False`
  - `unique=True`
- Practice API creation and data retrieval using Flask
- Access and test APIs directly on the web browser

---

## 🧩 Database Design (One-to-One)

### User Table
- `id` (Primary Key)
- `name`

### Profile Table
- `id` (Primary Key)
- `bio`
- `user_id` (Foreign Key → users.id, UNIQUE)

### Relationship Rule
- One **User** → One **Profile**
- One **Profile** → One **User**

This is enforced using:
- `uselist=False` in `db.relationship`
- `unique=True` in `ForeignKey`

---

## ▶️ How to Run the Project

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy
3. Run the app:
    ```bash
   python one-to-one-relation.py
4. Server will start at:
    ```bash
    http://127.0.0.1:5000
    
##  Available Web Endpoints

1. 1️⃣ Home Endpoint

    ```bash
    http://127.0.0.1:5000/

    ```bash
    http://127.0.0.1:5000/user-add

2. 2️⃣ Add User with Profile

    ```bash
    http://127.0.0.1:5001/user-add
    
    ```bash
    {
    "message": "User and Profile added successfully!"
    }

3. 3️⃣ Get All Users with Profiles

    ```bash
    http://127.0.0.1:5000/users
    
    ```bash
    {
        "message": [
            {
            "id": 1,
            "name": "John Doe",
            "profile_bio": "Software Developer"
            }
        ]
    }

4. 4️⃣ Get All Profiles with User Names

    ```bash
    http://127.0.0.1:5000/profiles
    
    ```bash
    [
        {
            "id": 1,
            "bio": "Software Developer",
            "user_name": "John Doe"
        }
    ]
