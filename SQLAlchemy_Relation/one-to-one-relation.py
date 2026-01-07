from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    profile = db.relationship("Profile", back_populates="user", uselist=False)

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user = db.relationship("User",uselist=False, back_populates="profile")

with app.app_context():
    db.create_all()

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
            'profile_bio': user.profile.bio if user.profile else None
        }
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
    app.run(debug=True)


