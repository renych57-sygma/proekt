
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes_db = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if title and content:
            notes_db[title] = content
            return redirect(url_for('notes'))

    return render_template('notes.html', notes=notes_db)

if __name__ == '__main__':
    app.run(debug=True)