from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not email or not password:
            flash('Все поля обязательны!', 'error')
            return render_template('register.html')

        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла! Теперь можно войти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            flash('Вы вошли!', 'success')
            return redirect(url_for('diary'))
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('login.html')

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if title and content:
            new_note = Notes(title=title, text=content)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('diary'))
        else:
            flash('Заголовок и текст обязательны!', 'error')

    all_notes = Notes.query.order_by(Notes.id.desc()).all()
    return render_template('diary.html', notes=all_notes)

if __name__ == '__main__':
    app.run(debug=True)