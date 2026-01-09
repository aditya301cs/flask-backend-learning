from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ============================================
# MODEL DEFINITIONS
# ============================================

class User(db.Model):
    """
    User model - represents a user in the system.
    Relationships:
    - One-to-One with Profile (via profile relationship)
    - One-to-Many with Post (via posts relationship)
    - Many-to-Many with Role (via roles relationship through user_roles table)
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    # One-to-One relationship with Profile
    # uselist=False ensures only one profile per user
    profile = db.relationship("Profile", back_populates="user", uselist=False)
    
    # One-to-Many relationship with Post
    # backref="author" allows accessing user from Post via post.author
    posts = db.relationship("Post", backref="author", lazy=True)
    
    # Many-to-Many relationship with Role
    # secondary='user_roles' uses the junction table for many-to-many
    # lazy='dynamic' returns a queryable collection for efficient filtering
    roles = db.relationship('Role', backref='users', secondary='user_roles', lazy='dynamic')

class Profile(db.Model):
    """
    Profile model - represents user profile information.
    One-to-One relationship with User.
    """
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    
    # ForeignKey links to User.id, unique=True enforces one-to-one relationship
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    
    # back_populates links back to User.profile
    user = db.relationship("User", uselist=False, back_populates="profile")

class Post(db.Model):
    """
    Post model - represents blog posts/articles.
    Many-to-One relationship with User (each post belongs to one author).
    """
    __tablename__ = "posts"  # Fixed: lowercase for consistency
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # ForeignKey links to User.id, nullable=False ensures every post has an author
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class Role(db.Model):
    """
    Role model - represents user roles for authorization.
    Many-to-Many relationship with User through user_roles junction table.
    """
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
# ============================================
# MANY-TO-MANY JUNCTION TABLE
# ============================================
# This table creates the many-to-many relationship between User and Role
# Each row represents a user having a specific role
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# Create all tables within application context
with app.app_context():
    # db.drop_all()  # Uncomment to drop and recreate tables
    db.create_all()

# ============================================
# ROUTES
# ============================================

@app.route('/post-add')
def add_post():
    """
    Route to add sample posts for the first user.
    Creates a user if none exists, then adds 3 sample posts.
    """
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
    """
    Route to retrieve all posts with author information.
    Demonstrates accessing related data through backref.
    """
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_data = {
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "author_name": post.author.name  # Accessed via backref
        }
        post_list.append(post_data)
    return jsonify(post_list)

@app.route('/user-add')
def add_user():
    """
    Route to add a new user with profile and roles.
    Demonstrates:
    - Creating related objects in a single statement
    - Adding items to a many-to-many relationship
    """
    new_user = User(name="John Doe")
    # Creating profile with user relationship set
    new_profile = Profile(bio="Software Developer", user=new_user)
    
    # Create roles and associate with user
    roles = [
        Role(name="Admin"),
        Role(name="Editor"),
        Role(name="Viewer")   
    ]

    for role in roles:
        new_user.roles.append(role)  # Add role to user's roles collection

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User and Profile added successfully!"})

@app.route('/users')
def getUsers():
    """
    Route to retrieve all users with their profiles, roles, and posts.
    Demonstrates nested relationship access in both directions.
    """
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            'profile_bio': user.profile.bio if user.profile else None,
            'roles': [],
            'posts': []
        }
        
        # Access posts through one-to-many relationship
        for post in user.posts: 
            user_data['posts'].append({
                'title': post.title,
                'description': post.description
            })
        
        # Access roles through many-to-many relationship
        for role in user.roles:
            user_data['roles'].append({
                'name': role.name
            })
        
        user_list.append(user_data)

    return jsonify({'message': user_list})

@app.route('/roles')    
def getRoles():
    """
    Route to retrieve all roles with their associated users.
    Demonstrates accessing many-to-many relationship from Role side.
    """
    roles = Role.query.all()
    role_list = []
    for role in roles:
        role_data = {
            "id": role.id,
            "name": role.name,
            'users': []
        }
        # Access users through backref on the many-to-many relationship
        for user in role.users:
            role_data['users'].append({
                'name': user.name
            })
        role_list.append(role_data)
    return jsonify(role_list)

@app.route('/profiles')
def getProfile():
    """
    Route to retrieve all profiles with user information.
    Demonstrates accessing the User through Profile's user relationship.
    """
    profiles = Profile.query.all()
    profile_list = []
    for profile in profiles:
        profile_data = {
            "id": profile.id,
            "bio": profile.bio,
            'user_name': profile.user.name  # Access user through relationship
        }
        profile_list.append(profile_data)
    return jsonify(profile_list)

@app.route('/')
def index():
    """Root route - health check endpoint."""
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)

# ============================================
# IMPORTANT LEARNING POINTS
# ============================================
"""
SQLAlchemy Relationship Types:

1. ONE-TO-ONE (User <-> Profile):
   - Use uselist=False on one side of the relationship
   - unique=True on ForeignKey enforces one-to-one constraint
   - Access: user.profile or profile.user

2. ONE-TO-MANY (User <-> Post):
   - Defined on the "one" side (User) with db.relationship()
   - ForeignKey on the "many" side (Post)
   - Use backref to access parent from child: post.author
   - Access: user.posts or post.author

3. MANY-TO-MANY (User <-> Role):
   - Requires a junction/association table (user_roles)
   - Use secondary='table_name' in db.relationship()
   - Access: user.roles or role.users
   - lazy='dynamic' for queryable collections (efficient for large datasets)

Key Concepts:
- back_populates: Explicitly links two relationships bidirectionally
- backref: Automatically creates reverse relationship
- lazy='dynamic': Returns a query object instead of loading all data
- unique=True on ForeignKey: Enforces one-to-one relationship

Best Practices:
- Use __tablename__ for explicit table naming consistency
- Keep relationship names descriptive and consistent
- Use lazy='dynamic' for many-to-many with large datasets
- Always use db.session.commit() to persist changes
- Create tables within app.app_context()
"""
