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


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks_to_do = mongo.db.tasks_to_do.find()
    return render_template("tasks.html", tasks_to_do=tasks_to_do)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # change to 'False' before submitting/finishing project


# other option below:
# if __name__ == "__main__":  # pragma: no cover
#     app.run(debug=True)
