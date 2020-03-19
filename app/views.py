from flask import render_template, jsonify, request
from app import app
from app.papybot import PapyBot
import os


@app.route('/')
def home():
    key = os.getenv("GMAPS_API_KEY_PUBLIC")
    return render_template("index.html", key=key)


@app.route('/ajax', methods=["POST"])
def ajax():
    textUser = request.form['textUser']
    papy = PapyBot()
    papyAns = papy.main(textUser)
    return jsonify(papyAns)
   

