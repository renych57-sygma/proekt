from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'

db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

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
            pass 

    all_notes = Notes.query.order_by(Notes.id.desc()).all()
    
    return render_template('diary.html', notes=all_notes)

if __name__ == '__main__':
    app.run(debug=True)