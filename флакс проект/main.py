from flask import Flask, render_template
import os
app = Flask(__name__)
print("Search paths for templates:", app.template_folder)
print("Current working directory:", os.getcwd())
@app.route('/')
def index():
    site_name = "Мой Flask-сайт"
    app_description = "имба-приложение на фласке"
    return render_template("index.html", site_name=site_name, app_description=app_description)
if __name__ == "__main__":
    app.run(debug=True)