from flask import Flask, render_template, abort, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
import secrets
from flask import Flask, render_template,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, select
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from forms import LogInForm, SignUpForm

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
Bootstrap(app)

app.config['SECRET_KEY'] = 'asditjfks£0234ivn£$osdmgn£Isldmmf'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    tasks = db.relationship('Task', back_populates='todo', cascade='all, delete-orphan')



class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    ticked: Mapped[bool] = mapped_column(Boolean, nullable=False)

    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    todo = db.relationship('Todo', back_populates='tasks')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))





@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
with app.app_context():
    db.create_all()

def clear_guest():
    user = User.query.filter_by(email="NA").first()
    if user:
        for todo in user.todos:
            db.session.delete(todo)
        db.session.delete(user)
        db.session.commit()


@app.route('/')
def home():
    return render_template('homepage.html', logged_in = current_user.is_authenticated)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', logged_in = current_user.is_authenticated)

@app.route('/about')
def about():
    return render_template('about.html', logged_in = current_user.is_authenticated)

@app.route('/login', methods=["POST", "GET"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        clear_guest()
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('todo', todo_name="Todo1"))
        else:
            flash('Invalid email or password.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", "danger")
    return render_template('login.html', form = form, logged_in = current_user.is_authenticated)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login', logged_in = current_user.is_authenticated))
        clear_guest()
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('todo', todo_name="Todo1"))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field.capitalize()}: {error}", "danger")

    return render_template('signup.html', form = form, logged_in = current_user.is_authenticated)

@app.route('/todo/<todo_name>')
def todo(todo_name):
    if not current_user.is_authenticated:
        user = User.query.filter_by(email="NA").first()
        if not user:
            user = User(email="NA", password="NA")
            db.session.add(user)
            db.session.commit()
    else:
        user = current_user

    todos = user.todos

    if not todos:
        count = len(user.todos)
        new_todo = Todo(
            name=f"Todo{count+1}",
            user_id=user.id
        )
        db.session.add(new_todo)
        db.session.commit()
        todos = user.todos

    selected_todo = next((todo for todo in todos if todo.name == todo_name), None)
    if not selected_todo:
        abort(404)

    data = {
        task.id: (task.title, task.description, task.ticked)
        for task in selected_todo.tasks
    }

    return render_template('todo.html', name=todo_name, data=data, logged_in=current_user.is_authenticated)




@app.route('/todo/<todo_name>/add-todo', methods=["POST"])
def add_todo(todo_name):
    if not current_user.is_authenticated:
        user = User.query.filter_by(email="NA").first()
        print("Not authenti")
    else:
        user = current_user
    title = request.form.get('title')
    description = request.form.get('description')

    todo = next((t for t in user.todos if t.name == todo_name), None)
    if not todo:
        abort(404)
    new_task = Task(
        title=title,
        description=description,
        ticked=False,
        todo=todo,
        user=user
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('todo', todo_name=todo_name, logged_in = current_user.is_authenticated))


@app.route("/<todo_name>/check-tick", methods=["POST"])
def check_tick(todo_name):
    json = request.get_json()
    checked_ids = json['checked_ids']
    ids = db.session.query(Task.id).all()
    for unchecked_id in [id_tuple[0] for id_tuple in ids]:
        if unchecked_id not in checked_ids:
            task = db.session.execute(
                select(Task).where(Task.id == unchecked_id)
            ).scalar_one_or_none()
            task.ticked = False
            db.session.commit()
    for checked_id in checked_ids:
        task = db.session.execute(
            select(Task).where(Task.id == checked_id)
        ).scalar_one_or_none()
        task.ticked = True
        db.session.commit()
    return redirect(url_for('todo', todo_name=todo_name, logged_in = current_user.is_authenticated))

@app.route("/<todo_name>/delete-todo/<todo_id>")
def delete_todo(todo_name, todo_id):
    task = db.session.get(Task, todo_id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('todo', todo_name=todo_name, logged_in = current_user.is_authenticated))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    clear_guest()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home', logged_in = current_user.is_authenticated))



if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
try:
    logout()
except:
    pass