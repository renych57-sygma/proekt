from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.secret_key = 'lol' 

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if Users.query.filter_by(username=username).first():
            flash('Такой пользователь уже существует!', 'danger')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = Users(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    cards = Card.query.all()
    return render_template('index.html', cards=cards)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/card/<int:id>')
@login_required
def card(id):
    card_item = Card.query.get_or_404(id)
    return render_template('card.html', card=card_item)

@app.route('/create')
@login_required
def create():
    return render_template('create.html')

@app.route('/form_create', methods=['POST'])
@login_required
def form_create():
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    text = request.form.get('text')

    if not title or not subtitle or not text:
        flash('Заполните все поля!', 'danger')
        return redirect(url_for('create'))

    new_card = Card(title=title, subtitle=subtitle, text=text)
    db.session.add(new_card)
    db.session.commit()

    flash('Карточка создана!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)