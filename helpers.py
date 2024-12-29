from flask import Flask, flash
from cs50 import SQL

db = SQL("sqlite:///character_exp_thresh.db")

def calculate_party_cr(party_size, party_level):
    easy_cr = db.execute("SELECT easy FROM char_lvl WHERE id = ?", party_level)[0]['easy'] * party_size
    medium_cr = db.execute("SELECT medium FROM char_lvl WHERE id = ?", party_level)[0]['medium'] * party_size
    hard_cr = db.execute("SELECT hard FROM char_lvl WHERE id = ?", party_level)[0]['hard'] * party_size
    deadly_cr = db.execute("SELECT deadly FROM char_lvl WHERE id = ?", party_level)[0]['deadly'] * party_size
    return easy_cr, medium_cr, hard_cr, deadly_cr

def calculate_monster_cr(monster_counts, monster_exps):
    total_exp = sum(count * exp for count, exp in zip(monster_counts, monster_exps))
    total_monsters = sum(monster_counts)

    if total_monsters == 1:
        multiplier = 1
    elif total_monsters == 2:
        multiplier = 1.5
    elif 3 <= total_monsters <= 6:
        multiplier = 2
    elif 7 <= total_monsters <= 10:
        multiplier = 2.5
    elif 11 <= total_monsters <= 14:
        multiplier = 3
    elif total_monsters >= 15:
        multiplier = 4
    else:
        flash("Please enter a valid number for monster count")
        return None

    total_exp *= multiplier
    return total_exp