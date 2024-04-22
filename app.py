from flask import Flask, render_template, request, redirect, url_for, flash
from models import Category, Note
from flask_login import LoginManager, login_user, current_user, logout_user
from models import User, db
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    notes = Note.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html', notes=notes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/note/<int:note_id>')
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note=note)


@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category']
        note = Note(title=title, content=content, category_id=category_id)
        db.session.add(note)
        db.session.commit()
        flash('Заметка успешно добавлена!')
        return redirect(url_for('index'))
    categories = Category.query.all()
    return render_template('add.html', categories=categories)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.category_id = request.form['category']
        db.session.commit()
        flash('Заметка успешно обновлена!')
        return redirect(url_for('index'))
    categories = Category.query.all()
    return render_template('edit.html', note=note, categories=categories)


@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
def delete(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        db.session.delete(note)
        db.session.commit()
        flash('Заметка удалена')
        return redirect(url_for('index'))
    return render_template('delete.html', note=note)


if __name__ == '__main__':
    app.run(debug=True)
