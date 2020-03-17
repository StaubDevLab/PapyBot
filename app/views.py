from flask import render_template, jsonify, request
from app import app
from app.papybot import PapyBot


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/ajax', methods=["POST"])
def ajax():
    textUser = request.form['textUser']
    papy = PapyBot()
    papyAns = papy.main(textUser)
    return jsonify(papyAns)
   

