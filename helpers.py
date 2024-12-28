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
    total_exp = 0
    for count, exp in zip(monster_counts, monster_exps):
        if count == 1:
            total_exp += exp
        elif count == 2:
            total_exp += exp * 1.5
        elif count >= 3 and count <= 6:
            total_exp += (exp * count) * 2
        elif count >= 7 and count <= 10:
            total_exp += (exp * count) * 2.5
        elif count >= 11 and count <= 14:
            total_exp += (exp * count) * 3
        elif count >= 15:
            total_exp += (exp * count) * 4
        else:
            flash("Please enter a valid number for monster count")
            return None
    return total_exp