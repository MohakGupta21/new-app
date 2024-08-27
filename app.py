from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import psycopg2

app = Flask(__name__)
# 'Host=localhost;Database=efcore;Username=postgres;Password=api123'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:api123@localhost:5432/todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
# print(db)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        new_todo = Todo(title=request.form['title'],desc=request.form['desc'])
        db.session.add(new_todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = db.get_or_404(Todo,sno)
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')

@app.route('/item',methods=['POST'])
def search():
    title = request.form['search']
    todo = Todo.query.filter_by(title=title).one_or_404()
    return render_template('item.html',todo=todo)
    # return f"{allTodo}"

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title=request.form['title']
        todo.desc=request.form['desc']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    return render_template('update.html',todo=todo)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)

    
