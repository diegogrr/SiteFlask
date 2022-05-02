from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # function to return a string for each element created
    def __repr__(self):
        return '<Task %r>' % self.id



# Create pages
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        if not task_content:
            msg = 'Please, write your task.'
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html', tasks=tasks, msg=msg)
        else: 
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, msg='')

@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):  
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/contact')
def contacts():
    return render_template('contact.html')

@app.route('/users/<my_user>')
def users(my_user):
    return render_template('users.html', my_user=my_user)

@app.route('/register', methods=['POST'])
def register():
    if not request.form.get('name') or not request.form.get('email'):
        return render_template('failure.html')
    with open('registered.csv', 'a', newline='', encoding='utf-8') as file: # 'a' means 'append'
        writer = csv.writer(file)
        writer.writerow((request.form.get('name'), request.form.get('email')))
    return render_template('success.html')

@app.route('/registered')
def registered():
    with open('registered.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        registered = list(reader)
    return render_template('registered.html', registered=registered)

# Execute the server function
if __name__ == "__main__":
    app.run(debug=True)
