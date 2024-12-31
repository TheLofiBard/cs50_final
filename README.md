# D&D 5e Combat Calculator
### Video demo : https://youtu.be/ybQXkqIBd3A
### Description:

This web application will take input from the user inorder to calculate the difficulty rating of a combat encounter for the popular table top roleplaying game, Dungeons and Dragons (D&D). It also comes equiped with a filterable database of monsters that the user and paruse in order to create their combat counter or use for insperation. Below are detailed desciptions of each file and their use for the application.

### app.py

This is the python file for my combat calculator. It utilized the flask framwork and access two databases, ```character_exp_threshold``` and ```monsters.db``` (explained below). The app.before_request is used to empty the session values when the page is reloaded. This is set as its own function and not included in the ```app.route("/")``` in order to not clear flashes that would alert the user of an error before the flash has appeared. 

```party_cr()``` is a function that gets values form the html form, check the validaity of the inputs and then convets them to an intager for use in the ```calculate_party_cr()``` helper function. It then saves the results into a session value and displays the 4 different thresholds for the partys challenge rating (cr). Those thresholds are labeld easy, medium, hard, and deadly and are set by the D&D game designers. 

Next is the ```monster_cr()``` function that also gathers inputs from a form, checks their validaty, and then runs the variables through the ```calculate_monster_cr()``` helper function. This function, however, is using ```request.form.getlist``` because the values for the monster inputs are saved in a list through javascript for the purpose of creating new inputs for monsters with differing exp values. The function then saves the returned value of ```total_exp``` and saves it into a session variable as well.

``` Combined_submit() ``` is a function that exepts both input from the party_cr form and the monster_cr form. If the user has filled out both of the party and monster forms, the function then checks all of their inputs, converts the values to an integer, and then runs ```calculate_party_cr``` and ```calculate_monster_cr```. Once both of those functino have been succesful, ```combined_submit``` will then compare the results and return the ```rating``` variable, which defines the combat encounter as easy, medium, hard, deadly, or impossible. If no inputs where submited, the function will then check to see if the appropriate variabes have been saved as session variables. If all variables exist, the function will compair those values and return ```rating``` and render the template as well. 

Finally we have ```monsters()``` which is a function to filter and populate the monster database for the user. The user can filter the database by minimum cr, maximum cr, armor class, minimum hit points, maximum hit points, type, and name. For min cr, max, cr, armor class, min hp, max hp and type, I created drop down style inputs so the user could select their desierd filter variable. Name is an imput field the user can type into freely. ```mosnters()``` creates the ```monsters``` variable with the value of ``` db.execute("SELECT * FROM monsters") ```. Then it gathers the user input variables and runs them through the helper function ```get_int_param()``` (explained in helpers.py) in order to return the variable as an integer. The function then collects the appropriate variables from ```monsters``` using ```monsters.get(#)```. This is used to get the cr, hit points, and armor class of all monsters. However, they are all strings and need to be converts to integers for them to function with the filter. So each variable is then ran through the helper function, ```extract_numeric_value``` (explained in helpers.py) that returns a float. The function the runs a series of if statements to filter monsters and append them into a list called ```filtered_monsters``` that is rendered in the template.
```
if cr_value is not None and hp_value is not None:
            if (min_cr is None or cr_value >= min_cr) and (max_cr is None or cr_value <= max_cr):
                if (min_hp is None or hp_value >= min_hp) and (max_hp is None or hp_value <= max_hp):
                    if (ac is None or ac_value == ac):
                        if (type is None or type.lower() in monster.get("meta").lower()):
                            if (name is None or name.lower() in monster.get("name").lower()):
                                filtered_monsters.append(monster)
```

### helpers.py

This python file contains functions that are called in ```app.py```. The function it includes are ```calculate_monster_cr()```, ```calculate_party_cr```, ```get_int_param()``` and ```extract_numeric_value()```. 

In ```calculate_party_cr()``` we get two arguments, ```party_size``` and ```party_level```. The function then creates a value for each cr rating calling them ```easy_cr```, ```medium_cr```, ```hard_cr```, and ```deadly_cr```. Each of these variables queries ```character_exp_thresh.db``` to get the exp value for the appropriate rating for ```party_level``` and then multiplies it by the ```party_size```. The function the returns the values for each variable. 

```calculate_monster_cr()``` also takes two arguments, ```monster_counts```, and ```monster_exps```. The function then totals the sum of the exp, using the ```zip``` function to maintain pairs of counts and exps, and totals the sum of monsters. It then goes through a series of if statments to determin what the multiplier for the encoutner should be. These numbers are also provided by the D&D game designers. 
For instance,
```
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
```
The ```total_exp``` variable is then multipled by the appropriate multiplier and then re-assigned to ```total_exp. ``` and returned. 
```
total_exp *= multiplier
    return total_exp
``` 

```extract_numeric_value()``` is used to search the text from ```monsters.db``` and return the appropriate text as a float. This function took a lot of searching as it contains new functions and even a module I was not familiar with. The function takes two arguments, ```text``` and ```patter```. The ```text``` input is the string taken from the appropriate column in ```monters.db```. The ```pattern``` input was also new to me and took some work. Because I needed to retreive a number from each of these strings, this was the code I used.
```
r'(\d+)'
```
This arrgument utilized in the ```re.search``` function would find consecutive digits in the string. Then by running  
```
if match:
        return float(match.group(1))
```
the function would return the 1st group of digits found in the text. This would then turn the string value into a float value. 

The ```get_int_param``` function takes one arument and returns the value as an integer so long as the value ```is.digit```. This was utilized to turn the select option filter values from strings to integers. 

### character_exp_threshold.db

This database is used to calculate the exp thresholds for each of the difficutly levels, easy, medium, hard, and deadly.
```
CREATE TABLE "char_lvl"(
    id INT PRIMARY KEY, 
    easy INT, 
    medium INT, 
    hard INT, 
    deadly INT
    )
```

### monsters.db

This database contains the stat blocks for all D&D monsters from the 5e monster manual. The program utilizes this database for filtering and rendering the monster stat blocks. 
```
CREATE TABLE "monsters" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "meta" TEXT NOT NULL,
    "armor_class" TEXT NOT NULL,
    "hit_points" TEXT NOT NULL,
    "speed" TEXT NOT NULL,
    "str" TEXT NOT NULL,
    "str_mod" TEXT NOT NULL,
    "dex" TEXT NOT NULL,
    "dex_mod" TEXT NOT NULL,
    "con" TEXT NOT NULL,
    "con_mod" TEXT NOT NULL,
    "int" TEXT NOT NULL,
    "int_mod" TEXT NOT NULL,
    "wis" TEXT NOT NULL,
    "wis_mod" TEXT NOT NULL,
    "cha" TEXT NOT NULL,
    "cha_mod" TEXT NOT NULL,
    "saving_throws" TEXT,
    "skills" TEXT,
    "senses" TEXT,
    "languages" TEXT,
    "challenge" TEXT NOT NULL,
    "traits" TEXT,
    "actions" TEXT,
    "legendary_actions" TEXT,
    "img_url" TEXT
)
```


### layout.html

layout.html is the main html file for the wep application. It containes the forms for the party and monster inputs as well as the hidden from for the ```combined_submit()``` inputs. Below the navbar is the jinja template for the flash messagse the user will recieve if there was an error with an input. 

The party cr form has two inputs, a submit button, and below it a div that takes the ```party_cr``` values. 

The monster cr initially has two inputs, a submit button, and below it a div that take the ```monster_cr``` value, ```total_exp```. However, the form also allows the user to add or remove inputs in order to run the calculation utilizing different exp value monsters. To do this I added a javascript function to add a row of inputs when called. 
```
function addMonsterInput() {
            var monsterInputs = document.getElementById('monster_inputs');
            var newInput = document.createElement('div');
            newInput.classList.add('monster_input');
            newInput.innerHTML = `
                <div class="row g-3 mt-2">
                    <div class="col-md-4">
                        <input class="form-control" type="text" name="monster_count[]" placeholder="Number of Monster">
                    </div>                            
                    <div class="col-md-4">
                        <input class="form-control" type="text" name="monster_exp[]" placeholder="Monsters Experience Points">
                    </div>
                </div>
            `;
            monsterInputs.appendChild(newInput);
    }
```
There is also a function to remove a row of inputs incase the user called the ```addMonsnterInput()``` by accident. 

Below the monster cr form is the ```combined_submit``` form. This form is hidden and has its values filled through the javascript funtion ```submitCombinedForm()```. This function grabs the values from the previous to forms and fills them into the hidden form which is then sent to the ```/combined_submit``` route in ```app.py```.  The function also creates the hidden input fields for the additional monster inputs added by the user and appends it in the ```combinedMonsterInputs``` element.
```
monsterInputs.forEach(function(input) {
                var monsterCount = input.querySelector('input[name="monster_count[]"]').value;
                var monsterExp = input.querySelector('input[name="monster_exp[]"]').value;

                var countInput = document.createElement('input');
                countInput.type = 'hidden';
                countInput.name = 'monster_count[]';
                countInput.value = monsterCount;

                var expInput = document.createElement('input');
                expInput.type = 'hidden';
                expInput.name = 'monster_exp[]';
                expInput.value = monsterExp;

                combinedMonsterInputs.appendChild(countInput);
                combinedMonsterInputs.appendChild(expInput);
            });
``` 

### monsters.html

In the ```monsters.html```, we have a form with mostly select inputs that the user can use to filter the ```monsters.db```. This form's values are fed to the ```monsters()``` function in ```app.py```. The html is then rendered using jinja for each of the monsters in the ```filtered_monsters``` list. 
```
{% for monster in monsters %}
<div class="container-fluid my-2 border">
    <ul class="list-unstyled">
        <li><strong>Name:</strong> {{ monster['name'] }}</li>
        <li><strong>Meta:</strong> {{ monster['meta'] }}</li>
        <li><strong>Armor Class:</strong> {{ monster['armor_class'] }}</li>
        <li><strong>Hit Points:</strong> {{ monster['hit_points'] }}</li>
        <li><strong>Speed:</strong> {{ monster['speed'] }}</li>
        <li><strong>STR:</strong> {{ monster['str'] }} {{ monster['str_mod'] }}</li>
        <li><strong>DEX:</strong> {{ monster['dex'] }} {{ monster['dex_mod'] }}</li>
        <li><strong>CON:</strong> {{ monster['con'] }} {{ monster['con_mod'] }}</li>
        <li><strong>INT:</strong> {{ monster['int'] }} {{ monster['int_mod'] }}</li>
        <li><strong>WIS:</strong> {{ monster['wis'] }} {{ monster['wis_mod'] }}</li>
        <li><strong>CHA:</strong> {{ monster['cha'] }} {{ monster['cha_mod'] }}</li>
        <li><strong>Saving Throws:</strong> {{ monster['saving_throws'] }}</li>
        <li><strong>Skills:</strong> {{ monster['skills'] }}</li>
        <li><strong>Senses:</strong> {{ monster['senses'] }}</li>
        <li><strong>Languages:</strong> {{ monster['languages'] }}</li>
        <li><strong>Challenge:</strong> {{ monster['challenge'] }}</li>
        <li><strong>Traits:</strong> {{ monster['traits']|safe }}</li>
        <li><strong>Actions:</strong> {{ monster['actions']|safe }}</li>
        <li><strong>Legendary Actions:</strong> {{ monster['legendary_actions']|safe }}</li>
        <li><img src="{{ monster['img_url'] }}" alt="{{ monster['name'] }}"></li>
    </ul>
</div>
{% endfor %}
```

### extra

As part of this project, I also wrote a python app to read the original JSON file of monster stats into a SQLite database. I did this simply becuase I was more comfortable working with a database and because I am interested in learning more about createing and working with databases in the future. 