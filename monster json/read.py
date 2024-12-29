import json
from cs50 import SQL

db = SQL("sqlite:///monsters.db")

data_file = 'srd_5e_monsters.json'

# Load the JSON data
with open(data_file, 'r') as file:
    monsters = json.load(file)

for monster in monsters:
    db.execute("INSERT INTO monsters (name, meta, armor_class, hit_points, speed, str, str_mod, dex, dex_mod, con, con_mod, int, int_mod, wis, wis_mod, cha, cha_mod, saving_throws, skills, senses, languages, challenge, traits, actions, legendary_actions, img_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                monster.get('name'),
                monster.get('meta'),
                monster.get('Armor Class'),
                monster.get('Hit Points'),
                monster.get('Speed'),
                monster.get('STR'),
                monster.get('STR_mod'),
                monster.get('DEX'),
                monster.get('DEX_mod'),
                monster.get('CON'),
                monster.get('CON_mod'),
                monster.get('INT'),
                monster.get('INT_mod'),
                monster.get('WIS'),
                monster.get('WIS_mod'),
                monster.get('CHA'),
                monster.get('CHA_mod'),
                monster.get('Saving Throws'),
                monster.get('Skills'),
                monster.get('Senses'),
                monster.get('Languages'),
                monster.get('Challenge'),
                monster.get('Traits'),
                monster.get('Actions'),
                monster.get('Legendary Actions'),
                monster.get('img_url')
                )
