import os
import json

from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL

from helpers import calculate_party_cr, calculate_monster_cr

app = Flask(__name__)
app.secret_key = 'dnd_combat_calculator'


db = SQL("sqlite:///character_exp_thresh.db")

data_file = 'srd_5e_monsters.json'

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

@app.before_request
def clear_session_on_home():
    if request.endpoint == 'index':
        session.pop('party_size', None)
        session.pop('party_level', None)
        session.pop('easy_cr', None)
        session.pop('medium_cr', None)
        session.pop('hard_cr', None)
        session.pop('deadly_cr', None)
        session.pop('total_exp', None)

@app.route('/', methods=['GET'])
def index():

    return render_template("layout.html")

@app.route('/party_cr', methods=['POST'])
def party_cr():
    
    if request.method == 'POST':

        party_size = (request.form['party_size'])
        party_level = (request.form['party_level'])
        
        # check for party size and level
        if not party_size or not party_level:
            flash("Please enter both party size and party level")
            return redirect("/")
        
        # check for input type
        elif not party_size.isdigit() or not party_level.isdigit():
            flash("Please enter valid numbers for party size and party level")
            return redirect("/")
        
         # Convert to integers after validation
        party_size = int(party_size)
        party_level = int(party_level)

        # check for positive numbers 
        if not party_size > 0 or not party_level > 0:
            flash("Please enter positive numbers for party size and party level")
            return redirect("/")
        
        else:
            easy_cr, medium_cr, hard_cr, deadly_cr = calculate_party_cr(party_size, party_level)

            session["easy_cr"] = easy_cr
            session["medium_cr"] = medium_cr
            session["hard_cr"] = hard_cr
            session["deadly_cr"] = deadly_cr


            return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=easy_cr, medium_cr=medium_cr, hard_cr=hard_cr, deadly_cr=deadly_cr)
                    
    else:
        return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))

@app.route("/monsters_cr", methods=['POST'])
def monsters_cr():
    if request.method == "POST":
        monster_counts = request.form.getlist('monster_count[]')
        monster_exps = request.form.getlist('monster_exp[]')
        
        # check for monster count and exp
        if not monster_counts or not monster_exps:
            flash("Please enter both monster count and monster exp")
            return redirect("/")
        
        try:
            monster_counts = [int(count) for count in monster_counts]
            monster_exps = [int(exp) for exp in monster_exps]
        except ValueError:
            flash("Please enter valid numbers for monster count and monster exp")
            return redirect("/")

        if any(count <= 0 for count in monster_counts) or any(exp <= 0 for exp in monster_exps):
            flash("Please enter positive numbers for monster count and monster exp")
            return redirect("/")
        
        total_exp = calculate_monster_cr(monster_counts, monster_exps)
        if total_exp is None:
            return redirect("/")
        
        session["total_exp"] = total_exp
            
        return render_template("layout.html", total_exp=total_exp, easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))

@app.route('/combined_submit', methods=['POST'])
def combined_submit():
    if request.method == 'POST':

       
        if request.form.get('party_size') and request.form.get('party_level') and request.form.get('monster_count') and request.form.get('monster_exp'):

            party_size = request.form.get('party_size')
            party_level = request.form.get('party_level')
            monster_counts = request.form.getlist('monster_count[]')
            monster_exps = request.form.getlist('monster_exp[]')

            try:
                party_size = int(party_size)
                party_level = int(party_level)
                monster_counts = [int(count) for count in monster_counts]
                monster_exps = [int(exp) for exp in monster_exps]
            except ValueError:
                flash("Please enter valid numbers for all inputs")
                return redirect("/")
            
            if party_size <= 0 or party_level <= 0 or any(count <= 0 for count in monster_counts) or any(exp <= 0 for exp in monster_exps):
                flash("Please enter positive numbers for all inputs")
                return redirect("/")

            # run calculate_part_cr and calculate_monster_cr functions
            easy_cr, medium_cr, hard_cr, deadly_cr = calculate_party_cr(party_size, party_level)
            total_exp = sum(calculate_monster_cr(count, exp) for count, exp in zip(monster_counts, monster_exps))

            if not total_exp:
                flash("Please enter a valid number for monster count and monster exp")
                return redirect("/")
            
            elif not easy_cr or not medium_cr or not hard_cr or not deadly_cr:
                flash("Please enter a valid number for party size and party level")
                return redirect("/")
            
            elif not session.get("total_exp") or not session.get("easy_cr") or not session.get("medium_cr") or not session.get("hard_cr") or not session.get("deadly_cr"):
                flash("Please enter valid numbers for party size, party level, monster count, and monster exp")
                return redirect("/")
            
            if total_exp <= easy_cr:
                rating = "Easy"
                
            elif total_exp <= medium_cr:
                rating = "Medium"
                    
            elif total_exp <= hard_cr:
                rating = "Hard"

            elif total_exp <= deadly_cr:
                rating = "Deadly"

            elif total_exp > deadly_cr:
                rating = "Impossible"

            else:
                rating = "Unknown"

            # pass values to layout.html
            return render_template("layout.html", rating=rating, total_exp=total_exp, easy_cr=easy_cr, medium_cr=medium_cr, hard_cr=hard_cr, deadly_cr=deadly_cr)    

        elif session.get("total_exp") and session.get("easy_cr") and session.get("medium_cr") and session.get("hard_cr") and session.get("deadly_cr"):

            if session.get("total_exp") <= session.get("easy_cr"):
                rating = "Easy"

            elif session.get("total_exp") <= session.get("medium_cr"):
                rating = "Medium"
    
            elif session.get("total_exp") <= session.get("hard_cr"):
                rating = "Hard"
    
            elif session.get("total_exp") <= session.get("deadly_cr"):
                rating = "Deadly"
            
            elif session.get("total_exp") > session.get("deadly_cr"):
                rating = "Impossible"

            else:
                rating = "Unknown"
    

            return render_template("layout.html", rating=rating, total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))        
        else: 
            flash("Please enter valid numbers for party size, party level, monster count, and monster exp")
            return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))
        
    else:
        flash("Please enter valid numbers for party size, party level, monster count, and monster exp")
        return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))

@app.route("/monsters", methods=['GET'])
def monsters():
    monsters = read_json(data_file)
    return render_template("monsters.html", monsters=monsters)

if __name__ == '__main__':
    app.run(debug=True)