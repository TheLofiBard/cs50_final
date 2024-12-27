import os
import json

from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)

data_file = 'srd_5e_monsters.json'

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    # Get numbers from user
    if request.method == 'POST':
        party_size = request.form.get("party_size")
        party_level = request.form.get("party_level")
    else: 
        return render_template("layout.html")

@app.route("/monsters", methods=['GET'])
def monsters():
    monsters = read_json(data_file)
    return render_template("monsters.html", monsters=monsters)