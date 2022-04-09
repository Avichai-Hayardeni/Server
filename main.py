from flask import Flask, request
import DataBaseLibrary as DB
from datetime import datetime
from random import randint


list_of_words = ["teeny", "voracious", "fragile", "anxious", "merciful", "flow", "pizzas"]

db = DB.Database("test.db")
db.clear_user_list()
db.clear_message_list()
for i in range(5):
    db.add_user("joe", datetime.now(), datetime.now())
for i in range(20):
    db.add_message(datetime.now(), 0, randint(1, 5), 0, list_of_words[randint(0, 6)])


app = Flask(__name__)


@app.route("/get_messages")
def get_messages():
    user_id = request.args.get("user_id")
    thing = db.get_pending_messages(user_id)
    print(thing)
    return thing


@app.route("/send_message", methods=["POST"])
def send_message():
    date = request.form.get("date")
    author_id = request.form.get("author_id")
    addressee_id = request.form.get("addressee_id")
    type = request.form.get("type")
    message = request.form.get("data")
    print(date, author_id, addressee_id, type, message)
    return "Thanks"


@app.route("/contact")
def contact():
    keys = request.args.keys()
    for key in keys:
        print(request.args.get(key))
    return "Message received. Thank you."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
