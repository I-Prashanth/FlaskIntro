from flask import Flask, render_template,redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
db = SQLAlchemy(app)

"""Steps to create db --
1- be inside virtualenv
2- start python instance terminal
3- 'from app import db' where app-name of file||db-name of database
4- db.create_all() - to create the database """

class Todo(db.Model):#class initializing all attributes required- id and content
    id = db.Column(db.Integer, primary_key=True)#unique id for each task
    content = db.Column(db.String(200), nullable=False)#content of tasks
    date_created = db.Column(db.DateTime, default=datetime.utcnow)#date when task was created

    def __repr__(self):#access id
        return '<Task %r>' % self.id



@app.route('/', methods=['POST', 'GET'])#app.route is to create a page with items
def index():#the method which will be invoked in that page
    if request.method == 'POST':#method to show the tasks on page
        task_content = request.form['content']#data fetched from form with id content
        new_task = Todo(content=task_content)#more tasks so an instance of class created

        try:#try-catch to add a new task into database db
            db.session.add(new_task)
            db.session.commit()#always commit to save db
            return redirect('/')#redirects to main page after adding new task

        except:
            return "An issue adding task!"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()#show all tasks if we are not adding a new task
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')#to delete using task id
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "A problem occured while deleting task!"

@app.route('/update/<int:id>', methods=['GET','POST'])#to update using task id, we access the data/content and change it
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Could not update the task!"
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)#to run the app - debug mode creates an auto reloading app