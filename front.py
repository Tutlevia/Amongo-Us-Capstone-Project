from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/form/add_cca')
def add_form():
    return render_template("add.html")

@app.route('/form/add_activity')
def add_activity():
    return render_template("add.html")

@app.route('/view/student')
def view_student():
    return render_template("view.html")

@app.route('/view/class')
def view_class():
    return render_template("view.html")

@app.route('/view/cca')
def view_cca():
    return render_template("view.html")

@app.route('/view/activity')
def view_activity():
    return render_template("view.html")

@app.route('/edit/membership')
def edit_membership():
    return render_template("edit.html")

@app.route('/edit/participation')
def edit_participation():
    return render_template("edit.html")
