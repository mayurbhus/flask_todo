from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#App configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

#Database modeling
class Todo_model(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(300), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

#All routes
@app.route("/", methods = ['GET', 'POST'])
def todo_details():

    #After cliking submit what should happen?
    if request.method == 'POST':
        title_from_req = request.form['title_in_form']
        title_to_add = Todo_model(title = title_from_req)
        db.session.add(title_to_add)
        db.session.commit()

    #What to be shown before and after cliking submit.
    all_todos = Todo_model.query.all()
    return render_template('home.html', todos = all_todos)

@app.route("/delete/<int:sno>") #Delete request with sno of title to be deleted.
def delete_task(sno):
    title_to_delete = Todo_model.query.filter_by(sno=sno).first()
    db.session.delete(title_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])#Update request with sno of title to be updated.
def update_task(sno):

    #What should happen after cliking update.
    if request.method == "POST":
        updated_title = request.form['title']
        title_to_update = Todo_model.query.filter_by(sno=sno).first()
        title_to_update.title = updated_title
        db.session.add(title_to_update)
        db.session.commit()
        return redirect("/")
    
    #What should be shown before cliking on update.
    todo = Todo_model.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)


if __name__ == "__main__":
    app.run(debug = True)