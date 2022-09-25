import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
CORS(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# prism.js
@app.route("/code_snippet")
def code_snippet_func():

    code_snippets = mongo.db.code_snippets.find()
    return render_template("code_snippets.html", code_snippet_func=code_snippets)

@app.route("/code_snippet", methods=["GET", "POST"])
def added_code_func():
    if request.method == "POST":
        print("(python) request.form.get(\"language\")==> ", request.form.get("language"))
        print("(javascript) request.form.get(\"language\")==> ", request.form.get("language"))

        # for python
        if request.form.get("language") == "python":
            print("(python) request.form.get(\"language\")==> ", request.form.get("language"))
            added_code = {
                "language": request.form.get("language"),
                "code": request.form.get("addedCode"),
            }
            mongo.db.code_snippets.insert_one(added_code)
            flash("Python code Successfully Added")

        # for javascript        
        elif request.form.get("language") == "javascript":
            print("(javascript) request.form.get(\"language\")==> ", request.form.get("language"))
            if request.form.get("language") == "javascript":
                added_code = {
                    "language": request.form.get("language"),
                    "code": request.form.get("addedCode"),
                }
            mongo.db.code_snippets.insert_one(added_code)
            flash("JavaScript code Successfully Added")
    else:
        flash("Code did not get added")

    return redirect(url_for("code_snippet_func"))    


# @app.route("/code_snippet", methods=["GET", "POST"])
# def added_python_code_func():
    # if request.method == "POST":
    #     added_code = {
    #         "language": "python",
    #         "code": request.form.get("addedPythonCode"),
    #     }
    #     mongo.db.code_snippets.insert_one(added_code)
    #     flash("Python code Successfully Added")
    # else:
    #     flash("Python code was not submitted!")

    # return redirect(url_for("code_snippet_func"))


# @app.route("/code_snippet", methods=["GET", "POST"])
# def added_javascript_code_func():
    # if request.method == "POST":
    #     added_code = {
    #         "language": "javascript",
    #         "code": request.form.get("addedJavaScriptCode"),
    #     }
    #     mongo.db.code_snippets.insert_one(added_code)
    #     flash("Javascript code Successfully Added")
    # else:
    #     flash("Javascript code was not submitted!")

    # return redirect(url_for("code_snippet_func"))


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks_to_do = list(mongo.db.tasks_to_do.find())
    return render_template("tasks.html", tasks_to_do=tasks_to_do)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username is already in mongodb
        # 'documented_users' is from mongodb collection
        existing_user = mongo.db.documented_users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))

        }

        # 'documented_users' is from mongodb collection
        mongo.db.documented_users.insert_one(register)

        # put newly created user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return render_template("profile.html", username=session["user"])

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username on form already exists in mongodb
        existing_user = mongo.db.documented_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensures hashed password stored in mongodb, matches what user entered
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}!".format(request.form.get("username")))
                return render_template("profile.html", username=session["user"])
            else:
                # invalid password match
                flash("Incorrect username and/or password")
                return redirect(url_for("login"))
        else:
            # username does not exist
            flash("Incorrect username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile():
    # grab current session user's username from mongodb
    username = mongo.db.documented_users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have logged out!")
    session.pop("user")
    # session.clear() ==> another way instead of 'session.pop("user")'
    return redirect(url_for("login"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        # is_critical = "on" if request.form.get("is_critical") else "off"
        task = {
            "category_title": request.form.get("category_title"),
            "task_title": request.form.get("task_title"),
            "task_info": request.form.get("task_info"),
            "deadline": request.form.get("deadline"),
            # "is_critical": is_critical,
            "created_by": session["user"]
        }
        mongo.db.tasks_to_do.insert_one(task)
        flash("Task Successfully Added")
        return redirect(url_for("get_tasks"))

    groupings = mongo.db.groupings.find().sort("category_title", 1)
    return render_template("add_task.html", groupings=groupings)


@app.route("/edit_task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == "POST":
        # is_critical = "on" if request.form.get("is_critical") else "off"
        submit = {
            "category_title": request.form.get("category_title"),
            "task_title": request.form.get("task_title"),
            "task_info": request.form.get("task_info"),
            "deadline": request.form.get("deadline"),
            # "is_critical": is_critical,
            "created_by": session["user"]
        }
        mongo.db.tasks_to_do.replace_one(
            {"_id": ObjectId(task_id)}, submit, True)
        flash("Task Successfully Updated")

    task = mongo.db.tasks_to_do.find_one({"_id": ObjectId(task_id)})

    groupings = mongo.db.groupings.find().sort("category_title", 1)
    return render_template("edit_task.html", task=task, groupings=groupings)


@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    # is not working...
    mongo.db.tasks_to_do.deleteOne({"_id": ObjectId(task_id)})
    flash("Task Successfully Deleted")
    return redirect(url_for("get_tasks"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # change to 'False' before submitting/finishing project
