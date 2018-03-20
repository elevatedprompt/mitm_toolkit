from flask import Flask, render_template, jsonify
import random

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

# Global Variables
botList = {
    'my first host': '111.111.111.111',
    'my second host': '222.222.222.222',
    'my third host': '333.333.333.333'
};

# Routers
@app.route("/")
def index():
    return render_template("index.html")

# Return connected bots
@app.route("/bots")
def get_bot_list():
    return jsonify(botList);

# Connect a new bot (TODO)

# Load
if __name__ == "__main__":
    app.run()

