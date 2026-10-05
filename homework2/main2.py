from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    site_name = "Flaskflask"
    app_description = "Second flask app"
    return render_template("index.html", site_name=site_name, app_description=app_description)
if __name__ == "__main__":
    app.run(debug=True)