from flask import Flask, render_template, request, jsonify
from chat import agent
import os


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return agent(input)


if __name__ == '__main__':
    os.makedirs("Memory", exist_ok=True)
    app.run()
