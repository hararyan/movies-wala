from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-wala-harsha.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Todo Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<Todo {self.sno}: {self.title}>"

# Create tables automatically
with app.app_context():
    db.create_all()

# Home route
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

# About route
@app.route("/About")
def pro():
    return render_template('About.html')

# Show route
@app.route("/show")
def shows():
    alltodo = Todo.query.all()
    todos_list = "<br>".join([f"{todo.sno}: {todo.date_created}" for todo in alltodo])
    return todos_list or "No todos found"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
