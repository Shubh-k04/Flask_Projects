#Importing all the required modules
from flask import Flask, flash, url_for, redirect, render_template, request
from utils.task_manager import Task_List

#Create a Flask and Task List Instance
app = Flask(__name__)
task_list = Task_List()

#Set up a secret key
app.config["SECRET_KEY"] = "dattebayo!"

#Create homepage
@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        task_name = request.form["task"]

        if task_name.count(" ") == len(task_name):
            flash("Task Cannot be Empty")
        elif(len(task_name) > 100):
            flash('A Task Cannot Be 100 Or More Characters Long' , category='fail')
        elif('/' in task_name or '?' in task_name or '%' in task_name):
            flash('Task Name Cannot Contain "/" or "?" or "%')
        else:
            return redirect(url_for("add_task", taskname=task_name))

    tasks = task_list.get_task()

    return render_template("__home_page.html", tasks=tasks)

#Create route for adding task to the task list
@app.route("/add/<taskname>")
def add_task(taskname):
    if taskname.count(" ") == len(taskname):
        raise flash("Task Cannot be Empty")
    else:
        try:
            task_list.add_task(taskname)
            flash("Successfully Added The Task", category="success")

        except Exception as e:
            flash(str(e), category="fail")

    return redirect(url_for("home_page"))

#Route for removing tasks
@app.route("/remove/<taskname>")
def remove_task(taskname):
    task_list.remove_task(taskname)

    flash("Successfully Removed The Task", category="success")

    return redirect(url_for("home_page"))

#Route for clearing all tasks
@app.route("/clear")
def clear_all_tasks():
    task_list.remove_all()

    return redirect(url_for("home_page"))
