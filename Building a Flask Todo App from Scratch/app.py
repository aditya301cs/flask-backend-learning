from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.secret_key = 'key'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('index'))
    
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    if request.method == 'POST':
        title = request.form.get('title')
        todo = db.session.get(Todo, todo_id)
        if todo:
            todo.title = title
            db.session.commit()
            flash('Todo updated successfully!', 'success')
        return redirect(url_for('index'))
    
    edit_todo = db.session.get(Todo, todo_id)
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('index.html', todos=todos, edit_todo=edit_todo)

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = db.session.get(Todo, todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
