from flask import Flask, render_template, request, session
from functools import wraps
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

def before_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("guess"):
            session["guess"] = random.randint(0, 101)
            session["is_correct"] = False

        elif session["is_correct"]:
            session["guess"] = random.randint(0, 101)
            session["is_correct"] = False

        return func(*args, **kwargs)

    return wrapper


@app.get("/")
@before_request
def index():
    return render_template("index.html")


@app.get("/game")
@before_request
def game():
    return render_template("game.html")


@app.get("/guess/<int:number>")
@before_request
def guess(number):
    session["is_correct"] = number == session["guess"]
    return render_template("guess.html", guess=number, correct_guess=session["guess"])
