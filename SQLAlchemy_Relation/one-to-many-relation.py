from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    profile = db.relationship("Profile", back_populates="user", uselist=False)
    posts = db.relationship("Post", backref="author", lazy=True)

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user = db.relationship("User",uselist=False, back_populates="profile")


class Post(db.Model):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/post-add')
def add_post():
    user = User.query.first()
    if not user:
        user = User(name="John Doe")
        db.session.add(user)
        db.session.commit()

    posts = [
        Post(title="First Post", description="This is the first post", user_id=user.id),
        Post(title="Second Post", description="This is the second post", user_id=user.id),
        Post(title="Third Post", description="This is the third post", user_id=user.id)
    ]

    for post in posts:  
        db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Posts added successfully!"})

@app.route('/posts')
def get_posts():
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_data = {
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "author_name": post.author.name
        }
        post_list.append(post_data)
    return jsonify(post_list)

@app.route('/user-add')
def add_user():
    new_user = User(name="John Doe")
    new_profile = Profile(bio="Software Developer", user=new_user)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User and Profile added successfully!"})

@app.route('/users')
def getUsers():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            'profile_bio': user.profile.bio if user.profile else None,
            'posts': []
        }
        for post in user.posts: 
            user_data['posts'].append({
                'title': post.title,
                'description': post.description
            })
        user_list.append(user_data)
    return jsonify({'message':user_list})

@app.route('/profiles')
def getProfile():
    profiles = User.query.all()
    profile_list = []
    for profile in profiles:
        profile_data = {
            "id": profile.id,
            "bio": profile.bio,
            'user_name': profile.user.name
        }
        profile_list.append(profile_data)
    return jsonify(profile_list)

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)


"""
# Flask SQLAlchemy Relationship Demo  
### One-to-One + One-to-Many Relationships
This project demonstrates how to implement **both One-to-One and One-to-Many relationships** using **Flask** and **Flask-SQLAlchemy** in a single backend application.
It is designed as a learning and interview-ready reference project showing how relational database concepts are mapped using ORM and exposed through web APIs.
---
## 🚀 Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- SQLite (local database)
---
## 🎯 Project Objective
- Understand **One-to-One** and **One-to-Many** relationships
- Learn how to use:
  - `db.relationship()`
  - `db.ForeignKey()`
  - `uselist=False`
  - `backref` and `back_populates`
- Practice API development using Flask
- Access and test APIs directly from the browser
- Build a portfolio-ready backend project
---
## 🧩 Database Design
### 1️⃣ User Table
- `id` (Primary Key)
- `name`
### 2️⃣ Profile Table (One-to-One with User)
- `id` (Primary Key)
- `bio`
- `user_id` (Foreign Key → users.id, UNIQUE)
**Relationship Rule**
- One **User** → One **Profile**
- One **Profile** → One **User**
---
### 3️⃣ Post Table (One-to-Many with User)
- `id` (Primary Key)
- `title`
- `description`
- `user_id` (Foreign Key → users.id)
**Relationship Rule**
- One **User** → Many **Posts**
- Each **Post** → One **User**
---
## 🔗 Relationship Mapping Summary
| Relationship Type | Mapping |
|------------------|--------|
| One-to-One | User ↔ Profile |
| One-to-Many | User → Posts |
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
1. Home Endpoint
    ```bash
    http://127.0.0.1:5000/
    ```
    Purpose:
    Verifies that the Flask server is running
    Response:
    ```bash
    {
    "message": "Hello, World!"
    }
    ```
2. Add User with Profile
    ```bash
    http://127.0.0.1:5001/user-add
    ```
    ```bash
    {
    "message": "User and Profile added successfully!"
    }
    ```
3. Get All Users with Profiles
    ```bash
    http://127.0.0.1:5000/users
    ```
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
    ```
4. Get All Profiles with User Names
    ```bash
    http://127.0.0.1:5000/profiles
    ```
    ```bash
    [
        {
            "id": 1,
            "bio": "Software Developer",
            "user_name": "John Doe"
        }
    ]
    ```
5. Add Post
    ```bash
    http://127.0.0.1:5001/post-add
    ```
6. Get All Posts with Author Names
    ```bash
    http://127.0.0.1:5001/posts
    ```
    ```bash
        [
    {
        "id": 1,
        "title": "First Post",
        "description": "This is the first post",
        "author_name": "John Doe"
    }
    ]
    ```
"""					
