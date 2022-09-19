import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
CORS(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
# print("mongo ==> ", mongo)
# print("mongo.db ==> ", mongo.db)


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks_to_do = mongo.db.tasks_to_do.find()
    # print("tasks ==> ", tasks_to_do)
    return render_template("tasks.html", tasks_to_do=tasks_to_do)


# if __name__ == "__main__":
#     app.run(host=os.environ.get("IP"),
#             port=int(os.environ.get("PORT")),
#             debug=True)  # change to 'False' before submitting/finishing project

# ignored in testing
if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
