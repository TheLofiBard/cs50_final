# Description: This file contains the main application logic for the D&D Combat Calculator. 
# It is responsible for handling all user input and output, as well as rendering the appropriate HTML templates. 
# It also contains the logic for calculating the CR of a party and monsters, as well as the total experience points for a given encounter.

from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL

from helpers import calculate_party_cr, calculate_monster_cr, extract_numeric_value, get_int_param

app = Flask(__name__)
app.secret_key = 'dnd_combat_calculator'


db = SQL("sqlite:///character_exp_thresh.db")
monsters_db = SQL("sqlite:///monsters.db")

# clear saved session data on home page load
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

# render layout.html
@app.route('/', methods=['GET'])
def index():

    return render_template("layout.html")

# collect party size and level then calculate party cr
@app.route('/party_cr', methods=['POST'])
def party_cr():
    
    # check for post method
    if request.method == 'POST':

        # get party size and level
        party_size = (request.form['party_size'])
        party_level = (request.form['party_level'])
        
        # check for party size and level inputs
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
        
        # run calculate_party_cr function
        else:
            easy_cr, medium_cr, hard_cr, deadly_cr = calculate_party_cr(party_size, party_level)

            # save values into session[]
            session["easy_cr"] = easy_cr
            session["medium_cr"] = medium_cr
            session["hard_cr"] = hard_cr
            session["deadly_cr"] = deadly_cr


            return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=easy_cr, medium_cr=medium_cr, hard_cr=hard_cr, deadly_cr=deadly_cr)
                    
    else:
        return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))

@app.route("/monsters_cr", methods=['POST'])
def monsters_cr():

    # check for post method
    if request.method == "POST":

        # get monster count and exp lists
        monster_counts = request.form.getlist('monster_count[]')
        monster_exps = request.form.getlist('monster_exp[]')
        
        # check for monster count and exp
        if not monster_counts or not monster_exps:
            flash("Please enter both monster count and monster exp")
            return redirect("/")
        
        # convert values to interger after validation
        try:
            monster_counts = [int(count) for count in monster_counts]
            monster_exps = [int(exp) for exp in monster_exps]
        except ValueError:
            flash("Please enter valid numbers for monster count and monster exp")
            return redirect("/")

        # check for positive numbers
        if any(count <= 0 for count in monster_counts) or any(exp <= 0 for exp in monster_exps):
            flash("Please enter positive numbers for monster count and monster exp")
            return redirect("/")
        
        # calculate total monster exp with calculate_monster_cr function
        total_exp = calculate_monster_cr(monster_counts, monster_exps)
        if total_exp is None:
            return redirect("/")
        
        # save total_exp into session[]
        session["total_exp"] = total_exp
            
        return render_template("layout.html", total_exp=total_exp, easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))

@app.route('/combined_submit', methods=['POST'])
def combined_submit():

    # check for post method
    if request.method == 'POST':

        # check for party size, party level, monster count, and monster exp
        if request.form.get('party_size') and request.form.get('party_level') and request.form.getlist('monster_count[]') and request.form.getlist('monster_exp[]'):

            # save into variables
            party_size = request.form.get('party_size')
            party_level = request.form.get('party_level')
            monster_counts = request.form.getlist('monster_count[]')
            monster_exps = request.form.getlist('monster_exp[]')
            
            # convert values to integers after validation
            try:
                party_size = int(party_size)
                party_level = int(party_level)
                monster_counts = [int(count) for count in monster_counts]
                monster_exps = [int(exp) for exp in monster_exps]
            except ValueError:
                flash("Please enter valid numbers for all inputs")
                return redirect("/")
            
            # check for positive numbers
            if party_size <= 0 or party_level <= 0 or any(count <= 0 for count in monster_counts) or any(exp <= 0 for exp in monster_exps):
                flash("Please enter positive numbers for all inputs")
                return redirect("/")

            # run calculate_part_cr and calculate_monster_cr functions
            easy_cr, medium_cr, hard_cr, deadly_cr = calculate_party_cr(party_size, party_level)
            total_exp = calculate_monster_cr(monster_counts, monster_exps)

            # check for successful total_exp calculation
            if not total_exp:
                flash("Please enter a valid number for monster count and monster exp")
                return redirect("/")
            
            # check for successful easy_cr, medium_cr, hard_cr, and deadly_cr calculation
            elif not easy_cr or not medium_cr or not hard_cr or not deadly_cr:
                flash("Please enter a valid number for party size and party level")
                return redirect("/")
            
            # compare total_ex to cr ratings and save into rating
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

        # check if session[] values are present
        elif session.get("total_exp") and session.get("easy_cr") and session.get("medium_cr") and session.get("hard_cr") and session.get("deadly_cr"):

            # compare session saved value for total_exp and session saved values for cr ratings
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
         
        # flash error message    
        else: 
            flash("Please enter valid numbers for party size, party level, monster count, and monster exp")
            return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))
    # flash error message 
    else:
        flash("Please enter valid numbers for party size, party level, monster count, and monster exp")
        return render_template("layout.html", total_exp=session.get("total_exp"), easy_cr=session.get("easy_cr"), medium_cr=session.get("medium_cr"), hard_cr=session.get("hard_cr"), deadly_cr=session.get("deadly_cr"))

@app.route("/monsters", methods=['GET'])
def monsters():
    # Get all monsters from the database
    monsters = monsters_db.execute("SELECT * FROM monsters")

    # Get query values and run them through get_int_param
    min_cr = get_int_param("min_cr")
    max_cr = get_int_param("max_cr")
    min_hp = get_int_param("min_hp")
    max_hp = get_int_param("max_hp")
    ac = get_int_param("armor_class")
    type = request.args.get("type")
    name = request.args.get("name")

    # create filtered_monsters list
    filtered_monsters = []

    # Filter mosnters based on query parameters
    for monster in monsters:
        # get strings from db
        cr_string = monster.get("challenge")
        hp_string = monster.get("hit_points")
        ac_string = monster.get("armor_class")

        # get numeric values from strings
        cr_value = extract_numeric_value(cr_string, r'(\d+)')
        hp_value = extract_numeric_value(hp_string, r'(\d+)')
        ac_value = extract_numeric_value(ac_string, r'(\d+)')

        if cr_value is not None and hp_value is not None:
            if (min_cr is None or cr_value >= min_cr) and (max_cr is None or cr_value <= max_cr):
                if (min_hp is None or hp_value >= min_hp) and (max_hp is None or hp_value <= max_hp):
                    if (ac is None or ac_value == ac):
                        if (type is None or type.lower() in monster.get("meta").lower()):
                            if (name is None or name.lower() in monster.get("name").lower()):
                                filtered_monsters.append(monster)

    # render monsters.html with filtters
    return render_template("monsters.html", monsters=filtered_monsters)
